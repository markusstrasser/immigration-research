# Hispanic/Mexican-origin test scores by generation — RESULT

**September 17 executed replacement:** The [primary-table and public-data check](../frontier_execution_2026_09_17/nlsy/RESULT.md) now verifies Duncan Table 8's original percentile-point coefficients, rejects the fixed SD conversion below, and reproduces the official NLS AFQT mean/SE benchmark. Public self-ID/family-history G2/G3/G4+ means are 34.85/39.94/40.10 percentiles; direct intervals and missing-grandparent sensitivity do not support a universal fourth-generation reversal. Public and restricted-ancestry samples differ. Historical text is preserved below.

**September 17 availability qualification:** official NLSY97 guides document respondent-reported and transcript SAT/ACT scores. “No SAT/ACT by generation” can describe the absence of a verified published table found in this lane, not absence of potentially joinable variables. No new valid generation estimate or revalidation of the AFQT SD conversion is supplied by this correction. See [new-data audit §5](../../../research/immigration-new-datasets-and-conclusions-2026-09-17.md), ladder111.

**September 17 scale/inference clarification:** the AFQT SD magnitudes in the historical verdict below are unvalidated approximations obtained by multiplying percentile-point coefficients by a common factor; they must not be quoted as directly reproduced standardized test-score effects. A mean percentile contrast alone does not recover an original-score standardized mean contrast. Preserve source-scale coefficients at their existing verification status pending a primary-table/scale check; no replacement SD estimate is supplied here. The later claim that SES/language-adjusted gaps are necessarily lower bounds on raw gaps is withdrawn: adjustment can move a contrast in either direction. [SOURCE: this lane's explicit conversion paragraph and adjusted-gap discussion; mathematical inference; [research frontier](../../../research/immigration-research-question-frontier-2026-09-17.md).]

**Verdict:** Best estimates, Hispanic/Mexican-origin vs non-Hispanic white, in SD. **Age 16-17 cognitive test (NLSY97 AFQT, ancestry-defined generations, the single best source): 2nd generation −0.70, 3rd generation −0.48 to −0.50, 4th+ generation −0.72.** At school entry (ECLS-K math): Mexican 2nd gen −1.10, Mexican 3rd+ −0.46, both flat after 1st grade. At grade 8 (NC administrative): Hispanic 2nd gen −0.69 reading, 3rd gen −0.2 to −0.3. The generational trend is **monotone improvement through the 3rd generation and then reversal at the 4th+**, which is why CPS/ACS "3rd+" pooling produces the apparent third-generation stall. The 2nd→3rd cognitive gain is about 0.20 SD; a deficit of roughly half an SD persists in the 3rd generation even with zero ethnic attrition. No SAT or ACT score by generation exists in any public source. Splitting the white reference into Jewish and non-Jewish moves every gap by about 0.01 SD and should not be done.

Model self-report: claude-opus-5[1m] (Opus 5, 1M context), researcher agent, dispatched 2026-09-16.

Provenance tags: [DATA] [INFERENCE] [SOURCE: url] [UNVERIFIED] used inline throughout.

## Scope
Hispanic (ideally Mexican-origin) standardized test scores, 2nd and 3rd+ generation vs non-Hispanic white, in SD units; datasets carrying BOTH test score and parental nativity. NCES longitudinal (NELS:88, ELS:2002, HSLS:09, ECLS-K 1998/2011), NLSY79/97 AFQT, Add Health PVT, NAEP proxies, SAT/ACT-by-generation, Jewish/white reference split.

## Findings

See Blocks 1-4 below. Summary table in Block 5.

---
### Block 1 (appended turn 4) — ECLS-K:1998 and NC administrative data

**Reardon & Galindo 2009, AERJ 46(3):853-891, DOI 10.3102/0002831209333184** [SOURCE: https://journals.sagepub.com/doi/10.3102/0002831209333184] — ECLS-K kindergarten class of 1998-99, N=8,911 (math analytic), gaps vs **third-generation non-Hispanic white** students. Sample sizes: Mexican 2nd gen 662 (math) / 308 (reading); Mexican 3rd+ gen 295 / 284; white 3rd gen 5,119.

MATH, fall kindergarten, SD vs 3rd-gen NH white [DATA]:
| Group | Fall-K math gap | Spring 1st grade | 5th grade |
|---|---|---|---|
| Mexican 1st gen | −1.10 | ≈ −0.75 | ≈ −0.8 (stable) |
| Mexican 2nd gen | −1.10 | ≈ −0.75 | ≈ −0.8 (stable) |
| Mexican 3rd+ gen | **−0.46** | — | little change after 1st grade |
| All Hispanic (pooled) | −0.77 to −0.92 (depending on assumed reliability r=1.0 to 0.7) | | −0.50 to −0.61 by spring 5th |

READING (only for students proficient in oral English at fall-K, so 1st gen omitted; selection on the order of 29% of all Hispanics, 77% of 1st gen excluded): all-Hispanic gap −0.29 to −0.52 across waves; **2nd-gen Mexican gap larger than 3rd-gen**, same shape as math, magnitudes about half.

Origin heterogeneity at K entry (math): Mexican and Central American ≈ −1.0 SD; Cuban, Puerto Rican, South American ≈ −0.5 SD. By 5th grade Mexican-origin still 0.25-0.50 SD below Cuban and Puerto Rican. [DATA]

**Generational reading:** the 2nd→3rd+ drop in the gap is LARGE at school entry (−1.10 → −0.46 math, i.e. about 0.64 SD of convergence in one generation) and then flat. This is the cleanest published 2nd-vs-3rd+ Mexican test-score contrast in a national sample. [INFERENCE]

**Hull (IZA DP 9307), "The Academic Progress of Hispanic Immigrants"** [SOURCE: https://docs.iza.org/dp9307.pdf] — North Carolina administrative panel, grades 3-8, end-of-grade tests, generation imputed. Continuous-enrollee estimates [DATA]:
- 1st-gen Hispanic reading: −1.00 SD (3rd grade) → −0.54 SD (8th), ≈ +0.08 SD/yr
- 2nd-gen Hispanic reading: ends 8th grade at **−0.69 SD** (gains 0.06 over the span)
- 3rd-gen Hispanic: **≈ −0.2 SD reading, −0.3 SD math**, flat
- math gaps ≈ 0.1 SD smaller than reading for 1st/2nd gen
- black-white reference in same data: ≈ −0.8 SD both subjects
Also cites Reardon & Galindo's NAEP-comparable figure: Hispanic-white gap ≈ 0.75 SD in 4th and 8th grade NAEP. [SOURCE: dp9307 p.2]

[GAP] Need: NLSY79/97 AFQT by Hispanic generation (Duncan-Hotz-Trejo ch.7 — NLSY79 does NOT identify Hispanic subgroups per the chapter text, so AFQT-by-Mexican-generation may not exist there); Add Health PVT; NAEP 2022/2024 ELL split; ELS:2002/HSLS:09 SAT merge; Jewish/white split.

---
### Block 2 (turn 6) — NLSY97 AFQT by Mexican generation: THE key result

**Duncan, Grogger, León & Trejo (2020), "New evidence of generational progress for Mexican Americans," Labour Economics 62:101771** [SOURCE: https://doi.org/10.1016/j.labeco.2019.101771; open PDFs: https://docs.iza.org/dp12704.pdf, https://www.nber.org/system/files/working_papers/w24067/w24067.pdf]

NLSY97, round 17 (2015-16), birth cohorts 1980-84, ages 30-36. **Unique feature: grandparents' countries of birth**, so the 3rd generation is defined by ancestry (no ethnic attrition) AND separated from the 4th+. >1,000 Mexican-origin respondents, ≥150 per generation cell. ASVAB/CAT-ASVAB taken in round 1 (1997) by 79.3% of the sample; dependent variable = AFQT percentile within three-month age group.

**Table 8, col (1): AFQT percentile-point deficit vs 4th+-generation non-Hispanic whites** (controls: sex, age at test) [DATA]:

| Mexican-American generation | AFQT deficit (percentile points) | ≈ SD equivalent |
|---|---|---|
| 1.5 gen (Mexico-born) | −31.8 | ≈ −0.89 |
| **2nd gen** | **−25.0** | **≈ −0.70** |
| **3rd gen (grandparent-defined)** | **−17.7** | **≈ −0.48 to −0.50** |
| 4th+ gen | −25.6 | ≈ −0.72 |
| 3rd+ pooled (cols 3-4, mimicking CPS/ACS) | between 3rd and 4th+, ≈ −22 | ≈ −0.62 |

SD conversion anchor: Richwine (CIS, 2018), replicating the same NLSY97 cells, states explicitly that a **17.1-percentile gap = about 0.48 SD** for the third-generation cross-section and **0.55 SD** for the ethnic (self-ID) sample [SOURCE: https://cis.org/Report/Grandchildren-LowSkill-Immigrants-Have-Lagging-Education-and-Earnings, n.8]. Scaling the other rows at ≈0.028 SD per percentile point is mine, and percentile→SD is nonlinear away from the middle, so treat the 1.5-gen figure as the least reliable. [INFERENCE]

**Reading.** Cognitive scores replicate the education pattern exactly: monotone improvement 1.5 → 2nd → 3rd, then a *reversal* at 4th+. The apparent "third-generation stall" in CPS/ACS is produced by pooling the genuinely-improving 3rd generation with a negatively selected 4th+ group. The 2nd→3rd AFQT gain is 7.3 percentile points (≈0.20 SD); pooling erases most of it. Richwine's counterpoint from the same data: even with zero ethnic attrition the 3rd-generation deficit stays statistically significant at ≈0.48-0.55 SD, with wide CIs from n≈128-155. Both readings are from the same cells. [FRAMING-SENSITIVE]

Sample sizes (Table 2): 1.5 gen 197, 2nd gen 412, 3rd gen 155, 4th+ gen 276.

Companion education numbers (years of schooling, same table): 11.85 / 12.97 / 13.54 / 12.79; HS diploma 61.5 / 76.2 / 84.3 / 68.3%; BA 8.6 / 13.5 / 19.7 / 21.2%. White 4th+ HS 86.2%.

**Duncan, Hotz & Trejo 2006 (NRC, "Hispanics and the Future of America" ch. 7)** [SOURCE: https://www.ncbi.nlm.nih.gov/books/NBK19908/] uses NLSY79 but states in text: "The information available in the NLSY79 does not permit identification of the Hispanic subgroups." It reports schooling/employment/earnings by Hispanic nativity (US-born vs foreign-born), **not AFQT by Mexican generation**. [VERIFIED NEGATIVE — do not cite ch.7 for an AFQT-by-generation number.]

[GAP] Still: Add Health PVT, NAEP 2022/24 ELL split, ELS:2002/HSLS:09 SAT-merge, Jewish/white reference split.

---
### Block 3 (turn 8) — NELS:88 / HS&B / ELS:2002 / HSLS:09

**Glick & White (2003), "The academic trajectories of immigrant youths," Demography 40(4):759-783** [SOURCE: https://doi.org/10.1353/dem.2003.0034] — HS&B sophomores (1980, N=12,810) and NELS:88 sophomores (1990). Outcome: NCES standardized math and reading tests (so coefficients ARE in SD units). Reference = 3rd-or-higher generation.

Math, generation coefficients vs 3rd+ gen [DATA]:
| | 1980 (HS&B) Model 1 / Model 4 | 1990 (NELS) Model 1 / Model 4 |
|---|---|---|
| Recent immigrants | −0.06 / −0.02 | +0.08 / +0.30*** |
| Preschool immigrants (1.5 gen) | −0.13* / −0.12* | +0.14** / +0.30*** |
| **2nd generation** | **−0.10** / −0.07* | **+0.08** / +0.20*** |

Ethnicity coefficients in the full model (net of SES, generation, language, family structure, grade retention), vs non-Hispanic white [DATA]:
| Group | 1980 math | 1990 math |
|---|---|---|
| Black | −0.51 | −0.45 |
| **Mexican** | **−0.34** | **−0.38** |
| Puerto Rican | −0.38 | −0.49 |
| Other Hispanic | −0.38 | −0.32 |
| Asian | +0.09 | +0.07 |

Reading shows the same shape with the immigrant advantage attenuated. **Key structural point: once SES and language are controlled, generation per se contributes little and the ethnic coefficient carries the gap.** These are *adjusted* gaps, not raw ones, so they are a lower bound on the raw Mexican-white SD gap at 10th grade. [INFERENCE]

**ELS:2002** — carries student and parent birthplace (3-category generation is standard in the literature, e.g. Potochnick's ELS:2002 analyses). NCES standardized test scores are mean 50, SD 10, so coefficients divide by 10 for SD. NCES's own published ELS:2002 OLS on 12th-grade IRT math scores gives Hispanic −0.3 to −0.6 raw *points* on an 81-item scale net of coursetaking, i.e. small once course sequence is held [SOURCE: https://nces.ed.gov/pubs2008/els_hsmath/tables/table_8.asp] — that specification conditions away most of the gap and is NOT a generation breakdown. **[GAP] No published ELS:2002 Hispanic-white gap BY GENERATION in SD units located this epoch.**

**HSLS:09** — the parent questionnaire collects "the parents' race and ethnicity, immigration status, language use," "the student's place of birth, immigration to the United States and grade placement upon arrival," and ELL history [SOURCE: https://nces.ed.gov/statprog/handbook/hsls09.asp]. So generation IS constructible. Assessment = adaptive algebraic-reasoning test, reported as quintile, proficiency probability, and IRT number-correct (0-118 scale). Liu & White (2017, PMC6226253) use HSLS 2009-2012 and find first-generation youth have HIGHER 11th-grade scores than 2nd/3rd-generation natives conditional on 9th-grade scores and family controls — a conditional-on-baseline result, not a raw gap. [GAP] no raw Hispanic-by-generation SD gap published from HSLS located.

---
### Block 4 (turn 11) — NAEP proxy, Add Health, the Jewish/white split, and runnable analyses

**NAEP (no nativity item; ELL and home-language are the proxies)** [SOURCE: https://nces.ed.gov/programs/coe/indicator/cnc; https://www.nationsreportcard.gov/mathematics/nation/groups/]
| Contrast | Year | Scale points |
|---|---|---|
| White−Hispanic, grade 4 math | 2022 | 21 (18 in 2019, 20 in 2011) |
| non-EL − EL, grade 4 math | 2022 | 23 (216 vs 239) |
| non-EL − EL, grade 8 math | 2022 | 36 (241 vs 277; was 42 in 2019, 46 in 1996) |
| non-EL − EL, grade 12 math | 2019 | 41 (111 vs 152) |
| White−Black, grade 4 math | 2022 | 29 |

2024 direction: grade-4 math rose for Black, Hispanic and white students; grade-8 math fell for Hispanic students, economically disadvantaged students, students with disabilities and English learners; grade-4 and grade-8 reading fell for many groups [SOURCE: https://www.nationsreportcard.gov/reports/mathematics/2024/g4_8/supporting-files/summary-of-results.pdf]. NCES does not publish a 2024 white−Hispanic gap number in the page text retrieved; the 2022 figure is the last one stated in scale points here. [GAP]

SD conversion: NAEP student-level SDs run roughly 30-32 (grade 4 math), 36-38 (grade 8 math), 35-37 (reading), so 21 points ≈ 0.65-0.70 SD at grade 4 math, and the grade-8 non-EL/EL gap of 36 points ≈ 0.95 SD. **The SDs are not verified from an NCES table in this epoch** — treat the conversions as [UNVERIFIED] and pull the published SDs from the NAEP Data Explorer before citing them. The EL/non-EL split is a *language* contrast, not a generation contrast; it mixes 1st-generation and 2nd-generation children and excludes the 3rd+, so it cannot answer the generational question. [INFERENCE]

**Add Health AHPVT (abridged PPVT-R, age-standardized, Waves I and III; public-use N≈6,500)** [SOURCE: https://doi.org/10.15139/s3/11900] — the instrument and generation variables exist, and Add Health also carries religion. Guo, Lin & Harris (2019, bioRxiv 544411) use PVT percentile rank with immigration status adjusted but **report no raw Hispanic-by-generation gap**. The only compilation found that reports Add Health, NLSY97 and HSLS:09 aptitude d-values by generation side by side is an unrefereed meta-analysis on the Human Varieties blog (2014) [SOURCE: https://humanvarieties.org/2014/06/25/u-s-ethnicrace-differences-in-aptitude-by-generation-an-exploratory-meta-analysis/], reporting **Hispanic-vs-3rd+-white d = 1.04 (1st gen), 0.71 (2nd gen), 0.57 (3rd+ gen)** and same-generation H/W d = 0.76 / 0.67 / 0.57. **Grade: C — self-published, not peer-reviewed, author pseudonymous.** Cite only as convergent, never as the source: the 2nd-gen 0.71 and 3rd+ 0.57 sit almost exactly on the NLSY97 AFQT numbers (0.70 and 0.62 pooled) derived independently above, which is the reason to note it at all. [FRAMING-SENSITIVE]

**Is "white" Jewish-inclusive, and does any published generational estimate split it? No.** Every dataset above codes Jews as white by race; none of ECLS-K, NELS:88, ELS:2002, HSLS:09, NAEP or the NLSYs' published Hispanic-generation analyses splits the white reference by religion. [VERIFIED NEGATIVE]

Datasets that WOULD allow the split: **GSS** (religion + Wordsum), **NLSY97** (religion at round 1 + ASVAB), **NLSY79**, **Add Health** (religion Waves I-IV + AHPVT), **Project Talent**, **WLS**, **MIDUS**, **ABCD**. Published Jewish-vs-gentile-white estimates [DATA]:
| Source | Sample | Jewish advantage |
|---|---|---|
| Lynn 2004, Pers. Indiv. Diff. 36:201-207, GSS 1990-96 Wordsum | 150 vs 5,300 | 7.5 IQ pts (7.32 vs 6.28; ≈0.50 SD) |
| Lynn & Kanazawa 2008, PAID 44:801-808, GSS 1972-2004 | 433 vs 17,335 | **d = 0.604** (9.06 IQ pts) |
| Dunkel et al. 2019, WLS Henmon-Nelson IQ | 53 Jews vs 2,603 Catholics / 2,027 Lutherans | 109.7 vs 101.4 (≈0.57 SD) |
| Jensen 2024 (blog, C-grade) recomputing NLSY79/97 ASVAB factor scores | n=109 / n=99 | 110 / 107.1 |
| Mazur (BJPA statistical portrait), GSS with matched controls | 254 vs 1,359 college grads | **8.1 vs 8.0 — no gap** once white, college-educated, large-metro, coastal controls are matched |

**Why it does not matter for the Hispanic question.** Jews are about 2% of US non-Hispanic whites. At the largest credible advantage (d ≈ 0.60) removing them shifts the white mean by about 0.02 × 0.60 ≈ **0.012 SD**. Every Hispanic-white gap above would move by roughly one hundredth of an SD — two orders of magnitude below the effects in play, and inside the standard errors of every estimate in this file. Mazur's matched-control result implies the adjustment is smaller still. Do not adjust for it. [INFERENCE]

## Ethnic-attrition caveat (applies to every 3rd+ row above)
Duncan & Trejo: self-identified 3rd+-generation Mexican Americans are a *selected* subset. About 17-30% of people with Mexican-born grandparents do not identify as Mexican, and the leavers are positively selected on education, intermarriage and outcomes. So self-ID 3rd+ figures (ECLS-K, NELS, ELS, CPS) are **biased downward**. Two corrections point opposite ways: (a) Duncan-Grogger-León-Trejo's ancestry-based NLSY97 3rd generation scores 7.3 AFQT percentile points BETTER than the self-ID-style pooled 3rd+, which supports "attrition manufactures the stall"; (b) Richwine, on the same cells, finds the ethnic-sample-vs-cross-section difference small and the 3rd-generation deficit still ≈0.48-0.55 SD with no attrition at all. The repo's own mechanisms memo already warns not to cite attrition as "the stagnation is an artefact" — the only explicit correction computed anywhere is about 0.1 years of schooling. A second, separable artefact is 3rd-vs-4th+ pooling, which the NLSY97 shows is the larger of the two.

## Four runnable analyses on public files
1. **NLSY97 public use (nlsinfo.org Investigator, free)** — pull `ASVAB_MATH_VERBAL_SCORE_PCT` (round 1 CAT-ASVAB, N=7,093 with all four subtests), respondent/parent/grandparent country of birth (`KEY_BDATE`, `CV_CITIZENSHIP`, round-5 birthplace items, grandparent-birthplace items), race/ethnicity, and religion (round 1). Reproduce Duncan et al. Table 8 in **SD units rather than percentiles** (the paper never publishes SDs), and, as the same extract, compute the Jewish/non-Jewish white reference split. Highest value per hour of work.
2. **ECLS-K:2011 public file (nces.ed.gov/ecls)** — replicate Reardon & Galindo on the 2010-11 kindergarten cohort. Parent birthplace and Hispanic origin are on the public file; the 1998 → 2011 comparison tests whether the −1.10 / −0.46 SD generational structure survived two decades of changed Mexican migration. No published replication located. [GAP → build]
3. **HSLS:09 public-use (NCES DataLab or the PUF)** — build the 3-category generation from the parent questionnaire items (parent immigration status, student place of birth, ELL history), regress the standardized algebraic-reasoning IRT score on generation × Hispanic origin. Produces the first raw HSLS Hispanic-by-generation SD gap; also the only NCES file with a plausible SAT/ACT merge path.
4. **ELS:2002 public-use** — same construction on the 10th-grade standardized math/reading (mean 50, SD 10, so coefficients ÷ 10 = SD), plus the College Board SAT merge in the restricted file. The public file alone answers the 2nd-vs-3rd+ question at age 16; the SAT number needs a restricted-use licence, which is the one item here that cannot be done on public data.

## Remaining gaps
- [GAP] NAEP student-level SDs not verified from an NCES source; the 2024 white−Hispanic scale-point gap not retrieved.
- [GAP] No peer-reviewed Add Health AHPVT gap by Hispanic generation located.
- [GAP] No SAT or ACT score by immigrant generation exists in any public source found. ELS:2002 restricted-use (College Board merge) is the only identified path; Texas ERC was not probed this epoch.
- [GAP] ECLS-K:2011 generational replication of Reardon & Galindo appears not to exist.

---
### Block 5 (turn 12) — master table: dataset × generation × gap

All gaps in SD, negative = below the non-Hispanic white reference. "Mex" = Mexican-origin, "Hisp" = all Hispanic.

| Dataset | Cohort / age | Instrument | 1st / 1.5 gen | 2nd gen | 3rd gen | 3rd+ or 4th+ | Source |
|---|---|---|---|---|---|---|---|
| **NLSY97** (Mex, ancestry-defined) | b.1980-84, tested age 12-17 | AFQT pct (CAT-ASVAB) | −0.89 (−31.8 pct) | **−0.70** (−25.0) | **−0.48/−0.50** (−17.7) | 4th+ −0.72 (−25.6); pooled 3rd+ ≈ −0.62 | Duncan, Grogger, León & Trejo 2020 Labour Econ 62:101771, Table 8 |
| NLSY97 (Mex, self-ID 3rd gen) | same | AFQT | | | −0.55 | | Richwine, CIS 2018, n.8 |
| **ECLS-K:1998** (Mex) | fall kindergarten | IRT math | −1.10 | **−1.10** | | **−0.46** | Reardon & Galindo 2009 AERJ 46(3), Fig. 5 |
| ECLS-K:1998 (Mex) | spring grade 1 → grade 5 | IRT math | −0.75 → ≈−0.8 | −0.75 → ≈−0.8 | | little change | ibid. |
| ECLS-K:1998 (Hisp pooled) | fall K → spring gr 5 | IRT math | −0.77 → −0.50 (r=1.0) | | | | ibid. Table 2 |
| ECLS-K:1998 (Hisp pooled) | fall K → spring gr 5 | IRT reading (English-proficient only) | −0.51 → −0.38 | | | | ibid. Table 2 |
| **NC admin panel** (Hisp) | grade 3 → 8 | state EOG reading | −1.00 → −0.54 | **−0.69** at gr 8 | | **−0.2** flat | Hull, IZA DP 9307 |
| NC admin panel (Hisp) | grade 3 → 8 | state EOG math | ≈0.1 smaller than reading | ≈−0.59 | | **−0.3** flat | ibid. |
| **NELS:88** (Mex) | grade 10, 1990 | NCES std math, *adjusted* | +0.30 gen effect | +0.20 gen effect | | Mexican ethnicity −0.38 | Glick & White 2003 Demography 40(4), Tables 3-4 |
| **HS&B** (Mex) | grade 10, 1980 | NCES std math, *adjusted* | −0.02 | −0.07 | | Mexican ethnicity −0.34 | ibid. |
| Meta-compilation (Hisp), **C-grade** | mixed | mixed aptitude | −1.04 | −0.71 | | −0.57 | Human Varieties 2014 (unrefereed) |
| **NAEP** (Hisp, no nativity) | grade 4, 2022 | math scale | — | — | — | pooled −21 pts ≈ −0.65/−0.70 SD [UNVERIFIED conversion] | NCES COE indicator cnc |
| NAEP EL proxy | grade 8, 2022 | math scale | EL−non-EL = −36 pts ≈ −0.95 SD | | | | ibid. |
| **ELS:2002 / HSLS:09** | grade 10 / grade 9-11 | NCES std math / algebra IRT | **no published raw gap by generation** | | | | [GAP] — buildable, see analyses 3-4 |
| **Add Health** | grades 7-12 | AHPVT | **no published raw gap by generation** | | | | [GAP] |

**Convergence check.** Three independent designs put the Mexican/Hispanic 2nd generation at −0.69 to −1.10 SD depending on age (largest at school entry, shrinking to about −0.70 by adolescence) and the 3rd/3rd+ at −0.20 to −0.57 SD. The adolescent NLSY97 value (−0.70 for the 2nd generation) and the NC grade-8 value (−0.69 reading) agree to a hundredth of an SD from completely different data. That is the number to carry. [INFERENCE]

**One caution on ECLS-K vs the rest.** The ECLS-K reading gaps are estimated only on students proficient in oral English at kindergarten entry, which excludes 29% of Hispanic students and 77% of the 1st generation, so every ECLS-K reading figure is a floor. The math test was administered in Spanish to Spanish-proficient non-English-proficient students, which removes the obvious language bias but means the math score and the reading score are not measured on the same population.
