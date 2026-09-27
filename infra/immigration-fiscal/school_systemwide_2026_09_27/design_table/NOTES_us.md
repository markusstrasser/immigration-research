claude-opus-5-5

**Verdict:** All nine US achievement designs the repo cites (within school, family or student; scores re-centred within grade-year or wave) are blind to a statewide shift; the between-state/metro designs (Hunt, Borgschulte, Betts–Fairlie) measure credentials, earnings or enrollment, and no between-state NAEP study of immigrant/EL share and native achievement was found.

# US design table: can the peer-effect designs see a statewide shift? (checkpoint notes)

Scope: US immigrant/EL peer-effect studies cited by the repo; per study, outcome normalization, stakes, identifying comparison, fixed effects, and whether a shift common to all schools in a state is detectable. Plus a search for between-state absolute-measure (NAEP) studies.

## Coverage log

- All ten brief items covered (Diette–Oyelere as three papers), plus two search finds; CSV `design_us.csv` (14 rows) built by `build_design_us.py`, byte-identical on rerun, LF only.

### 1. Figlio, Giuliano, Özek & Sapienza, ReStud 2024 91(2):972 — COVERED (published full text)
Source: [ReStud full text, UCLA copy](https://www.anderson.ucla.edu/sites/default/files/document/2025-06/diversityinschools.pdf), cached `_cache/figlio_restud.pdf`.
- Outcome: FCAT math/reading grades 3–10. Normalization, p. 977 §2.4: "we standardize the statewide test scores to zero mean and unit variance at the grade-year level over the entire population of students." Footnote 12, p. 984: a robustness run standardizes within the US-born sample only. [SOURCE]
- Stakes: FCAT is Florida's statewide accountability test (the basis of A–F school grades). The paper itself does not describe the stakes (no "accountability" in text except an FLDOE URL) → stakes cell is [TRAINING-DATA], not from the paper.
- Comparison and FE (eq. 2, p. 984; Table 4/5 footers): grade×year FE, school×year FE, family FE, family×year FE (col. 5). Identifying variation, p. 986: "the comparison between siblings in the same year, based on their 'historic' exposure … (1) siblings going to different grades in the same school(s) over time; (2) siblings going to different schools over time." Exposure = cumulative foreign-born share of prior school-specific cohorts.
- Statewide shift detectable? **No.** Grade×year standardization sets every Florida grade-year mean to zero and school×year FE absorb anything common to a school in a year; a statewide shift in standards, curriculum or grading is removed twice. [INFERENCE from the quoted normalization and FE]
- Headline: all US-born, col. 5 math 0.224 (0.074), reading 0.108 (0.064), per unit (0→1) exposure share, SD units (Table 4, p. 985); i.e. 0.0224 / 0.0108 SD per +10pp [CALCULATION]. 10th→90th pct (1%→13%): +2.8% / +1.7% SD (p. 987). White pupils (Table 5, p. 988) col. 5: math 0.128 (0.107), reading −0.007 (0.099) per unit share → +0.0128 SD, CI [−0.0082, +0.0338] per +10pp, matching the capacity-harms memo. [SOURCE]
- Gap: [GAP] stakes from the paper; the paper also has disciplinary-incident outcomes (not tabled here).

### 2a. Diette & Oyelere, IZA Journal of Migration 2017 6:2 — COVERED (published full text, open access)
Source: [Springer OA](https://link.springer.com/article/10.1186/s40176-016-0074-y), cached `_cache/diette_izajom2017.pdf`.
- Outcome: North Carolina End-of-Grade math/reading z-scores, grades 4–8 (value-added: lagged z-score on the right), 1998–2006. Normalization, fn 14 (p. 17): "The z-scores were calculated using the entire student population who took the exams within the grade in that particular year." [SOURCE]
- Stakes: NC EOG tests are the state accountability tests (ABCs); the paper does not discuss stakes → [TRAINING-DATA].
- Comparison/FE, eq. (1), p. 7: year FE, grade FE, school-by-year FE; exposure = LE (and Latino) share of the student's grade in the school-year. p. 7–8: "potential endogeneity is overcome by identifying impacts across grades at a particular point in time." SEs clustered at school-grade-year.
- Statewide shift detectable? **No.** Identification is across grades within a school-year, and the outcome is re-centred within each grade-year statewide. [INFERENCE]
- Headline (Table 4, p. 10, school-by-year FE, panel C with Latino share): white math LE share −0.035 (0.078), white reading −0.002 (0.052), per unit share; largest, black reading −0.128 (0.057), "a 10 % increase in LE student shares would be associated with a decline in reading scores of 0.013 standard deviation" (p. 10). [SOURCE]

### 2b. Diette & Oyelere, AER P&P 2014 104(5):412 — COVERED via working-paper version IZA DP 7856 (Dec 2013)
Source: [IZA DP 7856](https://docs.iza.org/dp7856.pdf), cached. The AER P&P printed version itself was not reached; numbers are from the DP and may differ from the 5-page published tables → [GAP].
- Outcome: NC End-of-Grade math/reading z-scores; DP fn 6 (p. 10): "The z-scores were calculated using the entire student population who took the exams within the grade in that particular year." [SOURCE]
- Comparison/FE: preferred model school-by-year FE (plus grade FE, lagged score), p. 11: "endogeneity is overcome by identifying impacts across grades within a particular point in time." Also reports school-FE and OLS.
- Statewide shift detectable? **No**, same reason as 2a.
- Headline (Table 6, DP p. 28, school-by-year FE): male math −0.0742 (0.034), male reading −0.0719 (0.038); female math −0.0248 (0.033), reading −0.0412 (0.036); per unit LE share, SD units. Text p. 14: +1pp LE share → male math −0.00074 SD. [SOURCE]

### 2c. Diette & Oyelere, Education Economics 2017 25(5):446 — COVERED via working-paper version IZA DP 6561 (2012), same title family ("Do Significant Immigrant Inflows Create Negative Education Impacts?")
Source: [IZA DP 6561](https://docs.iza.org/dp6561.pdf), cached. Journal version paywalled, not reached → published numbers [GAP]. The CV and the Academia listing tie DP 6561 to the Education Economics paper [SOURCE: Exa hits, iza.org CV; the link is the authors' own citation trail, not verified text identity → INFERENCE].
- Outcome: NC EOG math/reading "Z score" (eq. 1, p. 20), grades 4–8, 1999–2006. The DP does not print the normalization sentence; the sister papers (2a, 2b) on the same data say z-scores are computed within grade and year over all test takers → [INFERENCE] same here. Achievement terciles/quartiles are "within their grade in the state in a given year" (p. 8).
- FE: preferred school-by-year FE (Table 5 col. 1); also school-by-grade FE and individual FE. p. 22: "When school by year fixed effects are introduced, we are identify effects within a school across grades at a specific period of time."
- Statewide shift detectable? **No** in all three: school-by-year FE absorb it; school-by-grade and individual-FE models carry year and grade FE, and the outcome is re-standardized each grade-year. [INFERENCE]
- Headline (DP Table 5, p. 43, school-by-year FE): math −0.0516 (0.024), reading −0.0579 (0.026) per unit LE share; top quartile (Table 6) math −0.0823 (0.04), reading −0.0780 (0.03). School-by-grade FE flips math to +0.0572 (0.014). [SOURCE]

### 3. Hunt, JHR 2017 52(4):1060 — COVERED via NBER w18047 (May 2012); published JHR text not reached → published-table numbers [GAP]
Source: [NBER w18047](https://www.nber.org/system/files/working_papers/w18047/w18047.pdf), cached.
- Outcome: attainment — share of natives aged 21–27 who completed 12 years of schooling (census 1950–2000 + ACS 2008–10), adjusted for age/sex (and race/ethnicity) in a first-step individual regression; state-year coefficients λ̂st are the second-step outcome. Completion rates are corrected for GEDs using published GED tables (p. 7). No test score.
- Stakes: n/a (a credential count). A statewide lowering of diploma requirements raises this outcome mechanically. [INFERENCE]
- Comparison/FE: between states over time. Eq. (2), p. 10: state FE γs, year FE νt, BEA-region×year trends, 1940-covariate trends; eq. (3): 10-year differences with 2SLS using 1940 settlement shift-share instruments; SEs clustered by state.
- Statewide shift detectable? **Partly.** State-level variation over time is what identifies the estimate, so a state-specific shift correlated with immigration is inside the design, but only as a change in credential counts: a lowered standard would read as a gain; year FE and BEA-region×year trends absorb national and regional shifts. [INFERENCE]
- Headline (Table 2, col. 7, 2SLS, p. 37): all natives 0.34 (0.11) pp of 12-year completion per 1pp immigrant share of population 11–64 (abstract rounds to 0.3). Table 3 col. 7: non-Hispanic white 0.21 (0.11), black 0.36 (0.14), Hispanic −0.22 (0.24). [SOURCE]

### 4. Figlio & Özek, JOLE 2019 37(4) "Unwelcome Guests?" — COVERED via CALDER Working Paper 181 (Jan 2018); JOLE text not reached → published numbers [GAP]
Source: [CALDER WP (file named WP 180_0, cover says WP 181)](https://caldercenter.org/sites/default/files/2024-11/WP%20180_0.pdf), cached `_cache/haiti_calder180.pdf`.
- Outcome: FCAT reading/math, Spring 2010, 2010–11, 2011–12; p. 7: "test scores in reading and math standardized to zero mean and unit variance at the grade-year level"; also disciplinary incidents, mobility.
- Comparison/FE: eq. (1), p. 6: school FE δs and grade FE θg (school and grade attended in Spring 2010), exposure = % Haitian refugees in the student's school-grade in Spring 2010; p. 6: "we rely on within-school, across-grade variation in refugee concentration". IV: age distribution of entering refugees. SEs clustered by school. Robustness with family FE (App. Table 13) and student FE for discipline.
- Statewide shift detectable? **No.** Each outcome year is a single statewide cross-section standardized within grade-year, and school FE leave only across-grade contrasts in the same school. [INFERENCE]
- Headline (Table 5, p. 27–28, OLS, top refugee-receiving schools, school FE + covariates, col. III, Spring 2010): reading 0.006 (0.004), math 0.003 (0.005) SD per 1pp refugee share; all receiving schools col. III: reading 0.002 (0.003), math 0.001 (0.004). Text p. 12: "0.6 to 0.7 percent of a standard deviation increase in reading … 0.3 to 0.4 percent … in math". [SOURCE]

### 5. Doan, Morales, Özek & Schwartz, "Educational Spillover Effects of New English Learners in a New Destination State" (Delaware), EEPA 2024 — COVERED via EdWorkingPaper 23-818 (Aug 2023); EEPA text not reached → published numbers [GAP]
Note: the brief calls it "Özek et al."; the WP author order is Doan, Morales, Özek, Schwartz (RAND).
Source: [EdWorkingPaper 23-818](https://edworkingpapers.com/sites/default/files/ai23-818.pdf), cached.
- Outcome: Delaware Smarter Balanced (SBAC) ELA/math, 2015-16 to 2018-19, first year after arrival. Eq. (1), p. 10: "test scores standardized to zero mean and unit variance at the year-grade level". SBAC has a vertical scale, but the paper discards it by re-standardizing. [SOURCE for the quote; vertical scale = TRAINING-DATA]
- Stakes: SBAC is Delaware's accountability test; not discussed in the paper → [TRAINING-DATA].
- Comparison/FE: school-by-year FE δst, grade FE θg; exposure = % new EL students in the school-grade-year; SEs clustered at school-by-grade-by-year; "it requires sufficient cross-grade variation in new EL student share within schools" (p. 10).
- Statewide shift detectable? **No.** Within school-year across grades, with within-grade-year standardization. [INFERENCE]
- Headline (Table 2, p. 22, col. III): all existing students ELA 0.008 (0.004), math 0.003 (0.004); never-EL ELA 0.005 (0.003), math −0.000 (0.003); SD per 1pp new-EL share. [SOURCE]

### 6. Borgschulte, Cho, Lubotsky & Rothbaum, NBER w33961 (June 2025) — COVERED (WP full text)
Source: [NBER w33961](https://www.nber.org/system/files/working_papers/w33961/w33961.pdf), cached.
- Outcomes: adult W-2 income rank in the national distribution, log income, employment, HS and BA completion, migration; cohorts born 1977–85, linked tax records. p. 22: "Child and parental income ranks reflect their standing within the national distribution."
- Comparison: cross-sectional across 214 commuting zones, eq. (1) p. 12: 1980–90 immigrant inflow rate; 1980 CZ controls and 1940 mobility controls; shift-share enclave IV; SEs clustered by CZ. No state FE in the primary model. Robustness: CZ-of-birth FE with decile×instrument interactions, which "comes at the cost of removing cross-CZ variation" (p. 14).
- Statewide shift detectable? **Partly.** Between-CZ variation includes between-state variation and the earnings rank is national, so a state- or city-wide learning loss that lowered adult earnings would load on β; but the design cannot say the channel is schools, and HS completion would rise under lowered standards. [INFERENCE]
- Headline (Table 1 col. 1, p. 54): rank per 1pp inflow, decile 1 +0.147 (0.080), decile 10 −0.238 (0.076) → +1.5 / −2.4 points per 10pp (p. 22). BA completion decile 10 −0.593 pp per 1pp (Table 5 col. 6, p. 58). [SOURCE]

CSV: `design_us.csv` written with rows 1–6 (8 rows incl. the three Diette–Oyelere papers) by `build_design_us.py`.

### 7. Cho, PAA 2011 manuscript (ECLS-K ELL classmates) — COVERED (manuscript full text via Exa fetch; the direct curl to the PAA server returned nothing). Published version (Economics of Education Review 2012) not reached → [GAP]
Source: [PAA 2011 paper 110005](https://paa2011.populationassociation.org/papers/110005), text saved `_cache/cho_paa2011.txt`.
- Outcome: ECLS-K reading/math IRT scale scores, spring K and spring 1st grade (1998–2000), value-added with lagged score. p. 12: "the test scores are transformed to have mean 0 and standard deviation 1 for the overall sample on each of the tests and time periods." So the IRT scale is re-standardized per wave over the national sample. Low-stakes (a federal survey assessment, no consequences for schools). [SOURCE; stakes = INFERENCE from the survey design]
- Comparison/FE: OLS, school FE (Table 2), child FE (Table 3), child FE + school FE (Table 3 col. 2, Table 5). Exposure = dummy for any ELL classmate; child FE identify off "the difference in the chance of having any ELL classmates between kindergarten and first grade" (p. 15).
- Statewide shift detectable? **No.** Exposure varies across classrooms inside a school and within a child across two waves; exposed and unexposed children in the same state share any statewide shift, and wave standardization removes the national level. [INFERENCE]
- Headline: Table 5 (p. 39), child FE + school FE, reading: non-Hispanic white −0.037 (0.023), all −0.042 (0.019); Table 2 (p. 33) school FE: reading −0.052 (0.017), math −0.039 (0.017). SD per any-ELL-classmate dummy. Matches the repo memo's −0.037 / 0.023. [SOURCE]

### 10 (brief order). Repo ECLS-K checks, research/immigration-school-peer-checks-2026-09-20.md — COVERED (repo memo + lane README)
- Outcome: ECLS-K 1998 IRT scale fields; lane README: "Outcomes use the correct IRT scale fields, standardized separately in each wave using that wave's positive child weights across all origins." Low-stakes survey assessment.
- Comparison/FE: school FE (classrooms within a school), baseline cubic reading/math, controls; exposure = any LEP classmate or classroom LEP share; CR1 school-cluster SEs.
- Statewide shift detectable? **No**, same logic as Cho: within-school, across-classroom exposure. [INFERENCE]
- Headline (memo table): spring 2000 reading −0.040 [−0.111, +0.031], math −0.056 [−0.136, +0.024] SD for any LEP classmate, school FE; K reading +0.004, math −0.026. [DATA: repo memo, lane `derived/results.json`]

### 8. Ahn & Jepsen, IZA Journal of Migration 2015 4:5 — COVERED (published OA full text)
Source: [Springer OA 10.1186/s40176-015-0030-2](https://link.springer.com/article/10.1186/s40176-015-0030-2), cached `_cache/ahn_jepsen2015.pdf`.
- Correction to the repo's school-angle RESULT (Block 2), which called this "association, not a causal design — no FE/IV claimed in the abstract": the full text uses student FE, school FE and grade-by-year FE (eq. 1, p. 9; Table 2–3 footers). It is a FE panel design, not a raw association. [SOURCE]
- Outcome: NC EOG reading/math, grades 6–8, 2006–2012, value-added. p. 9: "The dependent variable is a standardized test score"; p. 13: "test scores are standardized with mean zero". The paper does not say at what level (grade-year statewide is the NCERDC convention) → normalization level [UNVERIFIED].
- Stakes, stated by the paper (p. 6): "The exam scores are used to generate school-level report cards and enter into the final grade calculations for the students. Therefore, the exams are high-stakes not only for the school, but for the students as well."
- Comparison: within student over time as the grade-level (and class-level) % LEP changes, net of school FE and grade-by-year FE; SEs clustered school-grade-year.
- Statewide shift detectable? **No.** Grade-by-year FE absorb anything common to all NC students in a grade-year, and the scores are mean-zero standardized. [INFERENCE]
- Headline (Table 2 NL1, p. 12, non-LEP reading): % LEP −0.106 (0.042); math (Table 3 NL1) −0.073 (0.056). p. 11–12: "a one-percent increase in percent LEP in the grade … corresponds with a 0.106 percent of a standard deviation decrease in the reading test score" → −0.0106 SD per +10pp [CALCULATION]. [SOURCE]

### 9. Betts & Fairlie, JPubE 2003 87:987 — COVERED (published full text, author copy)
Source: [author PDF](https://people.ucsc.edu/~rfairlie/papers/published/jpube%202003%20-%20native%20flight.pdf), cached.
- Outcome: private-school enrollment of native-born children (1980 and 1990 census microdata), not achievement.
- Comparison/FE: two-step; probit with MA FE and MA×1990 terms, then the 1980→90 MA first-difference effects regressed on the change in immigrant share (eq. 3.1–3.2, p. 997); GLS/OLS/IV; no state FE.
- Statewide shift detectable? **Partly.** Between-MA changes include between-state policy changes, so a response to a statewide degradation would register, but only as enrollment behaviour.
- Headline (Table 2, secondary): immigrant share GLS 1.7766 (0.8514), scaled derivative 0.2594 → "Each immigrant added to the public schools in an MA results in a predicted decrease of 0.26 native students in public schools" (p. 1001); IV 3.9049 (2.3059), scaled 0.5702. Primary: no significant relation (abstract). [SOURCE]

CSV rebuilt: 12 rows (all ten brief items; Diette–Oyelere is three rows).

## Search for between-state absolute-measure (NAEP) studies

Result: **no US study found that relates immigrant, EL or Hispanic enrollment share to white, native or non-EL achievement between states over time on NAEP or another absolute, low-stakes scale.** This is a search result, not proof of absence.

Searches run (2026-09-27/28):
1. Exa: "state NAEP panel regression immigrant or English learner or Hispanic share of enrollment effect on white or native student achievement between states over time" → NCES Hispanic–White gap reports (descriptive), Pew ELL gap report (descriptive), Urban Institute demographically adjusted NAEP (adjusts for composition, no immigration regression), AIR NVS 2024 (below), Spees–Potochnick–Perreira 2016 (below), "Compositional Effects, Segregation and Test Scores: Evidence from NAEP" (journals.sagepub.com/doi/10.1007/s12114-014-9200-3; not opened; title suggests race segregation, not immigration) [GAP].
2. Exa: "Neymotin … SAT scores state-level immigrant share" → Neymotin 2009 EER (abstract only; CSV row marked [UNVERIFIED]).
3. Exa: "Study of Changes in Public School Composition During the Pandemic … NAEP" → AIR NVS 2024, full PDF read (`_cache/air_nvs_composition_2024.pdf`). Between-state NAEP, but a Beaton–Chromy composition decomposition, not an effect on non-EL students. CSV row added.
4. Exa: "immigrant inflows and native students' NAEP test scores across states, difference-in-differences or shift-share, state and year FE" → only within-state peer papers already tabled, Jaeger–Ruist–Stuhler (shift-share methods), Spees et al.
5. Exa: "new immigrant destination states EL growth effect on non-EL achievement NAEP restricted-use" → Spees, Potochnick & Perreira, EPAA 24(99) 2016: restricted NAEP grade 8, 2003–07, compares LEP (and non-LEP) achievement in new vs established destination states. Cross-sectional state-type contrast, no change-on-change design, outcome is LEP youths' own scores; non-LEP youth score ~3 points higher in new destinations (Exa extract of the paper; not a peer-effect estimate) [SOURCE: redalyc PDF via Exa highlights; full table not read].
6. S2 `search_papers`: "immigration state NAEP test scores native students panel" and "English language learner share state achievement NAEP fixed effects white students" → nothing relevant (Dee–Jacob NCLB, Song–Yang–Garet CCR standards on state NAEP by subgroup — policy, not immigration).
7. Exa: Fetzer 2016, "The Effect of Unrestricted Immigration on Schools" (Palgrave chapter) → abstract: city time series for Mariel Cubans in Miami, Algerians in Marseille, Eastern Europeans in Dublin; "does not substantially … affect overall test scores". Test scale and design unverified; chapter not reached [UNVERIFIED], not tabled.
8. Exa: SEDA-based district studies of Hispanic/EL share → only immigration-enforcement papers (Kirksey et al. 2020, deportations and White–Latino gaps; Secure Communities and Hispanic students). None estimate white achievement against EL/immigrant share. SEDA itself (NAEP-linked, cross-state comparable) is the natural data for the lane's Test 6.

Nearest analogues on absolute or between-unit outcomes: Hunt 2017 (between states, attainment), Borgschulte et al. 2025 (between CZs, national earnings rank), Betts & Fairlie 2003 (between MAs, enrollment), Neymotin 2009 (SAT, two states, unverified), AIR NVS 2024 (between states, NAEP, composition only).

## Gaps
- [GAP] Published versions not read for AER P&P 2014, Education Economics 2017, JHR 2017, JOLE 2019, EEPA 2024, Cho EER 2012; numbers are from working papers and may differ.
- [GAP] Stakes for FCAT / NC EOG / Delaware SBAC come from training knowledge except Ahn–Jepsen, which states it.
- [GAP] Ahn–Jepsen standardization level; DP 6561 normalization (inferred from sister papers).
- [GAP] Neymotin 2009 full text; Fetzer 2016 chapter; the Review of Black Political Economy NAEP compositional-effects paper.
- Next queries if re-dispatched: SEDA white-student scores × district EL share (Reardon/Fahle papers); "Mapping State Proficiency Standards" × EL share; ProQuest dissertations "state NAEP immigrant share".

## Verdict
Every US achievement study the repo cites (Figlio et al., the three Diette–Oyelere papers, Figlio–Özek, Doan–Özek et al., Ahn–Jepsen, Cho, the repo's ECLS-K checks) identifies off within-school, within-family or within-student contrasts with school×year, school or grade×year FE, and eight of nine re-standardize scores within grade-year or wave. They cannot detect a shift common to all schools in a state. The designs that use between-state or between-metro variation (Hunt, Borgschulte et al., Betts–Fairlie) measure credentials, earnings or enrollment, not learning on an absolute scale. I found no between-state NAEP study of immigrant/EL share and native achievement.
