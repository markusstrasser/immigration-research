claude-opus-5-5[1m]

**Verdict:** No study shows any sign of fabrication. The code and data are either public or held by an agency with a named access route. The direction holds: every study that identifies an effect finds children or households better off when parents gain status. The repo's wording overstates the size and the scope. Four readings need fixing. (1) Hainmueller et al. 2017 is SOUND BUT IMPRECISE. It is one Oregon RD with 95% CI −0.6 to −7.9 points, and its sample does not screen mothers on DACA's arrival and schooling rules. Scaling the 4.3-point intention-to-treat effect to the mothers who could actually qualify therefore implies an effect near or above the 7.9% baseline. The true effect is probably nearer the lower CI bound. (2) Cascio–Cornell–Lewis's "96 g" extrapolates a county-level gradient to a 100% application rate. The effect in the average county is 34 g, 65 g after holding birth composition fixed. The interval is wide (log estimate 0.0263, SE 0.0127, so t ≈ 2.1). (3) Bean et al.'s 1.24-year IV figure is printed without a standard error or first-stage statistic, and its "unauthorized" side pools never-migrated and status-unknown mothers. (4) Tran's +5 Medicaid points do not raise total insurance coverage. The ladder calls that an "improvement", but on the fiscal ledger it is added public spending. The most consequential problem is that the ladder and RESULT.md present "−4.3 to −4.5 points", "+96 g" and "1.24 years" as agreeing, well-measured effects of legalization. They are one noisy intention-to-treat estimate of DACA eligibility, one extrapolated county gradient and one IV point estimate with no reported precision. None measures a child outcome past age 12, and none measures school or adult outcomes by identified legalization.

# C: Children of unauthorized parents, legal-status studies audit (2026-09-23)

Repo claims audited:
- `infra/immigration-fiscal/parent_status_2026_09_23/literature.md:1` (verdict) and rows 1–15.
- `RESULT.md:145–161` ("Published evidence").
- `research/immigration-confidence-ladder.md:303` (entry 186, "Published evidence runs the same way … improve citizen children's mental health (−4.3 to −4.5 points), birthweight (+96 g) and Medicaid enrollment (+5 points)").

Primary texts parsed this session: the Hainmueller Science PDF (authors' copy), the Cascio NBER w32635 PDF, the Bean corpus PDF, the Amuedo-Dorantes & Antman author PDF and the Abramitzky et al. NBER w26408 PDF. All were converted with pdftotext and are held in the session scratchpad. The Tran and Landale texts were not re-read (see Coverage).

---

## 1. Hainmueller, Lawrence, Martén, Black, Figueroa et al. 2017, *Science* 357:1041, doi:10.1126/science.aan5893

**1. Repo claim.** literature.md:1 says: "DACA protection of mothers cut their citizen children's adjustment and anxiety diagnoses by 4.3–4.5 points from about 7.9%". RESULT.md:154 and ladder 186 repeat it, and ladder 186 renders it as "−4.3 to −4.5 points". It is the main piece of causal evidence that parental status itself, and not selection, harms children.

**2. Data capture pipeline.**

| Stage | Institution | What happens | Likely error sign on headline |
|---|---|---|---|
| Mother's status | Oregon Health Authority, Emergency Medicaid (labor and delivery) | Unauthorized status is **inferred from Emergency Medicaid coverage at birth**. "The program mainly serves unauthorized immigrants, but lawful permanent residents with less than 5 years of residency can also obtain coverage"; the 90–99% unauthorized share comes from CA and NC estimates, not Oregon [SOURCE: paper p.1041] | Recent LPRs cannot be affected by DACA, so misclassification dilutes the ITT toward zero |
| DACA eligibility | Researchers | Only the **age rule** is observed, from the mother's exact birthdate (cutoff 15/16 June 1981). "We do not observe whether mothers apply for DACA" [SOURCE: p.1041]. Nothing screens on arrival before age 16, residence since 2007 or the schooling requirement | The first stage (actual DACA receipt at the cutoff) is small, maybe 10–30% [INFERENCE; no first-stage figure in the main text]. Scaling the −4.3 ITT to recipients gives about −14 to −43 points against a 7.9% baseline, which is implausible. Either the effect spills over to ineligible-but-near-cutoff families, or the point estimate is inflated (winner's curse) |
| Outcome | Oregon Medicaid claims (provider ICD-9 codes) | Diagnoses of adjustment, acute stress or anxiety disorder appear only if the child visits a Medicaid provider who codes them | A drop in diagnoses could reflect less contact or children leaving Medicaid. The authors tested this: visits show no discontinuity (fig. S12, table S16), and a non-prespecified restriction to children with ≥1 visit gives similar estimates [SOURCE: p.1043]. Residual risk is small but runs toward overstating the benefit |
| Sample | Same | 5,653 mothers born 1980–82, 8,610 children born 2003–15, followed to 2015 at ages 0–12; 73% Hispanic [SOURCE: p.1041]. Estimation windows: ±199 days (n = 3,039 children) for the combined outcome [SOURCE: Fig. 2 note] | Children who leave Oregon or Medicaid drop out; not shown by cutoff side [UNVERIFIED] |

**3. Design and precision.**
- Sharp RD intention-to-treat, local linear, MSE-optimal bandwidth.
- **Prespecified estimate: −4.3 points, P = 0.023, 95% CI 0.6 to 7.9, baseline 7.9%.** Adjustment disorders alone: −4.4 (CI 0.9–7.8). Anxiety: P = 0.153 (CI −0.6 to 4.1) [SOURCE: p.1043].
- The **−4.5 (7.8 → 3.3%, P = 0.037)** figure is a ±150-day graphical fit (n = 2,260) of the same data [SOURCE: p.1042 text; Fig. 1 note]. "4.3–4.5" is therefore two specifications of one estimate, not two results.
- Balance holds: pre-DACA placebo 0.4 points (P = 0.817), covariate p-values look uniform, the density test is clean, and children of standard-Medicaid mothers show no effect.
- Preregistered: EGAP 20170227AC; the paper was received 5 May 2017 [SOURCE: p.1044]. Whether the authors saw outcome data before the 27 Feb 2017 registration is not stated [UNVERIFIED].
- Non-prespecified subgroups: ages 6–12 carry the effect; by sex the difference is not significant.

**4. Replication and critique.** Replication code is on Harvard Dataverse (doi:10.7910/DVN/8EEDAP) [SOURCE: p.1044]. The Oregon claims data are restricted, so outsiders cannot reproduce it end to end. I found no published comment or reanalysis in this session [GAP; not searched beyond the paper]. No independent replication in a second state is known to me [TRAINING-DATA, UNVERIFIED].

**5. Politicization signals.** Funders are the Russell Sage Foundation and the Ford Foundation (which gives operational support to the Stanford Immigration Policy Lab) [SOURCE: p.1044]. The title and abstract say "protecting mothers improves children's mental health", but the tables show only that age eligibility reduces diagnoses. The discussion goes beyond the data: "it is reasonable to expect that permanent legal status or a pathway to citizenship would have an equal, if not greater, effect" [SOURCE: p.1043]. The design itself is strong. Symmetry test: the IZA jus soli paper (brief trigger) was downgraded for a wide CI, and the same treatment applies here. The CI's lower bound (0.6 points) is 1/7 of the point estimate.

**6. Verdict: SOUND BUT IMPRECISE, and OVERSTATED IN REPO.** There is no sign of fabrication.
- Repo text: "DACA protection of mothers cut … diagnoses by 4.3–4.5 points".
- Corrected: "Mothers' age eligibility for DACA (Oregon, Emergency-Medicaid births) cut diagnosed adjustment/anxiety disorders among their children aged 0–12 by 4.3 points (95% CI 0.6–7.9) from 7.9%. It is one preregistered RD in one state, receipt of DACA is not observed, and the upper range is implausibly large for the share of mothers who could qualify."

---

## 2. Cascio, Cornell & Lewis 2024, NBER w32635, "The Intergenerational Effects of Permanent Legal Status"

**1. Repo claim.** literature.md:1 and RESULT.md:156 say "IRCA legalization raised Mexican mothers' birthweights by 96 g". Ladder 186 says "birthweight (+96 g)".

**2. Data capture pipeline.**

| Stage | Institution | What happens | Error sign |
|---|---|---|---|
| Birth and mother's origin | State vital registration → NCHS natality detail files, 1982–1999 | Mother's birthplace (Mexico) and Hispanic origin come from the birth certificate; birthweight is recorded at delivery (hard measurement) | Small |
| Legalization exposure | INS Legalization Applications Processing System (LAPS) + 1990 5% PUMS | **No person-level link.** "We cannot merge these anonymized universe files at the person level", so the county application rate (Mexican-born women born 1944–72) is merged by county of residence [SOURCE: pp. 4, 17–18] | Ecological. The denominator comes from 1990 PUMS, which the authors say causes attenuation (the above-median dummy gives larger coefficients) [SOURCE: p.19]. Toward zero |
| County sample | Authors | 273 counties computable → 119 with balanced panels → **89 counties in 8 states after dropping California** (Medi-Cal) [SOURCE: pp. 18–19; state counts CO 7, FL 16, IL 11, IN 8, NJ 10, NY 10, OH 4, TX 23] | Texas carries a quarter of counties; external validity to CA (half of IRCA) is untested |
| Composition | Natality | Legalization changed who gave birth (fertility, sponsored wives). Holding parity, age, sex and multiplicity fixed, the first-period effect is **65 g, not 96 g** (58 with father-on-certificate; 74 adding prenatal care) [SOURCE: p.27, Table 4] | Raw 96 g overstates the per-birth health effect by about a third |

**3. Design and precision.**
- County application rate × event-time DiD within state, standard errors clustered on 89 counties, weighted by pre-period births. Placebo: US-born Mexican-ethnic mothers. Pre-trend joint p = 0.59 [SOURCE: p.18].
- **Scaling:** 95.6 g is the coefficient on the application rate, a 0→1 change, described as "the average IRCA legalization applicant". In the average county (application rate 0.357) the effect is **34 g in 1987–93** and 59 g in 1993–99 [SOURCE: pp.18–19].
- Log column: 0.0263 (SE 0.0127), t ≈ 2.07 [SOURCE: Table 2 col. 2]. The implied 95% CI is about 0.1–5.1%, roughly 5–186 g per applicant [INFERENCE from the log SE; the grams-column SE was not parsed].
- The above-median-dummy specification gives p = 0.048 for the first period [SOURCE: p.19].
- Many specifications (nine alternatives in Fig. 4) point the same way. The paper is not preregistered.

**4. Replication and critique.** It is a working paper. I found no comment or reanalysis [GAP]. The inputs (natality files, LAPS, PUMS) are public or archival, so it can be reproduced.

**5. Politicization.** I see none in the text. The authors bound the effect and decompose mechanisms, crediting fertility with about a third. The abstract's "96 g" is the extrapolated per-applicant number, which is the larger framing, but the text also gives 34 g.

**6. Verdict: SOUND BUT IMPRECISE, and OVERSTATED IN REPO.**
- Repo: "IRCA legalization raised Mexican mothers' birthweights by 96 g".
- Corrected: "Counties with more IRCA applicants saw Mexican-born mothers' babies grow heavier after 1987. That is 34 g in the average county, which extrapolates to 96 g per legalized mother (t ≈ 2), and about a third of it comes from changed birth composition (65 g adjusted). It is county-level exposure in 8 states, California excluded, and a working paper."

---

## 3. Bean, Leach, Brown, Bachmeier & Hipp 2011, *IMR* 45(2):348–385

**1. Repo claim.** literature.md:1 and 19 and RESULT.md:147–150 say: "2.04 fewer years of school, 1.51 after controls, 1.24 with an IRCA-timing instrument". Ladder 186 matches this with the lane's n = 7 cell (2.03).

**2. Data capture pipeline.**

| Stage | Institution | What happens | Error sign |
|---|---|---|---|
| Survey | IIMMLA 2004 (Russell Sage-funded, five-county LA phone survey) | Adult 1.5- and second-generation respondents aged 20–40 | LA-only, and phone response selects on stability |
| Parent status | Respondent's recall | Adult children report each parent's entry, green card and naturalization steps. Children may not know a parent's history, and "unknown" is a category | Recall error is likely to under-report past unauthorized status among legalized parents |
| Residual categories | Authors | "Unauthorized (or unknown)" is pooled throughout. The MUFU reference class includes "others with status unknown" [SOURCE: pp. 365–366 legend, lines 807–808; Table 1]. In Table 4 the probability that the mother "migrated to U.S." is only 0.28 in MUFU and 0.36 in MUFL (already flagged in literature.md row 1b) | Pooling never-migrated or unknown mothers with unauthorized ones probably **overstates** the status gap [INFERENCE]. Footnote 8's defence compares status-unknowns with unauthorized-at-interview parents on observables only, not never-migrated mothers [SOURCE: fn. 8] |
| Outcome | Self-report | Completed years of schooling | Small |

**3. Design and precision.**
- 2SLS instrument: mother "having come to the country to stay before 1982", in a first-stage logit with antecedents. LPR entrants are kept in the first stage [SOURCE: p.373].
- **No first-stage F statistic and no 2SLS standard error are printed.** The text gives the point estimate 1.24 [SOURCE: p.374].
- The exclusion restriction is argued ("no difference between the earlier and later arriving groups … other than … secular increases") and adjusted through duration in the US [SOURCE: p.373]. Pre-1982 arrival also means more of the child's schooling was spent in the US and an older cohort, which violates exclusion unless duration fully absorbs it [INFERENCE].
- Latent classes plus nested models plus IPTW add up to a large specification space. There is no preregistration.

**4. Replication and critique.** IIMMLA is public (ICPSR 22627). This lane's independent recode found 2.03 years unadjusted on a purer n = 7 cell, which is a partial reproduction of the raw gap. The IV has not been reproduced [GAP].

**5. Politicization.** The follow-up book *Parents Without Papers* (RSF 2015) is framed as a case for legalization. The press-release means (2.3 years) were never checked against tables (literature.md row 2 already grades this C). The paper itself hedges ("reduces but does not appear to eliminate").

**6. Verdict: MEASUREMENT RISK (direction: overstates the gap), and OVERSTATED IN REPO for the IV.** No sign of fabrication.
- Repo: "1.24 with an IRCA-timing instrument".
- Corrected: "1.24 years by 2SLS (no standard error or first-stage strength reported; the 'unauthorized' side includes mothers of unknown status and many scored as never having migrated)."

---

## 4a. Tran 2025, *Contemporary Economic Policy*, doi:10.1111/coep.70009

**1. Repo claim.** literature.md row 8, RESULT.md:157 ("DACA mothers' children gained 5 points of Medicaid enrollment") and ladder 186 ("improve citizen children's … Medicaid enrollment (+5 points)").

**2. Capture.** ACS: parents' status is **imputed** ("likely undocumented"); child insurance is self-reported by the household, and ACS Medicaid reports are known to undercount [TRAINING-DATA]. Imputation error dilutes toward zero.

**3. Precision.** Not re-parsed this session [GAP]. literature.md quotes the author: "no clear increase in overall health insurance coverage among children with likely DACA mothers", and no effect through fathers.

**5–6. Verdict: OVERSTATED IN REPO [FRAMING-SENSITIVE].** The result is a shift from private coverage to Medicaid with no gain in coverage. The ladder lists it among outcomes that "improve". For the fiscal account it is a rise in public transfers.
- Corrected ladder wording: "shifted citizen children from private coverage to Medicaid (+5 points Medicaid, no clear change in total coverage; mothers only)."

## 4b. Amuedo-Dorantes & Antman 2016, *Economics Letters* 147:1–4

**1. Repo claim.** literature.md:1 says it "cut eligible households' poverty 38%"; RESULT.md does not repeat it.

**2. Capture.** ACS. Status is proxied by "Mexican non-citizens" with HS+ who arrived before age 16 and before 2007 [SOURCE: p.3]. Non-citizens include LPRs, which dilutes toward zero.

**3. Precision.**
- n = 3,573 household heads aged 27–34, DiD by age eligibility, standard errors clustered by state.
- **DACA×Eligible −0.106 (SE 0.035)** on mean 0.281, so 95% CI −0.037 to −0.175, i.e. 13–62%.
- **Near-poverty (<1.5× line) −0.061 (SE 0.058), n.s.** [SOURCE: Table 3].
- Age-cohort DiD relies on parallel income-age trends. The authors report a pre-trend check [SOURCE: p.6].
- Implied effect on actual recipients (≈ −0.106 ÷ take-up) is large relative to plausible earnings gains [INFERENCE].

**6. Verdict: SOUND BUT IMPRECISE.** It is a household-head outcome; children are not analysed. literature.md should add "(95% CI 13–62%; near-poverty n.s.)".

---

## 5. Landale, Hardie, Oropesa & Hillemeier 2015, *JHSB* 56(1):2–18

**1. Repo claim.** literature.md row 15 and RESULT.md:159 say: "no worse than children of US-born mothers on behaviour".

**2. Capture.** LA FANS asks mothers their legal status directly [SOURCE: literature.md row 15, not re-read]. Undocumented mothers under-reporting their status would move some of them into the "documented" group, which **narrows** the documented–undocumented gap [INFERENCE]. So the measured "worse than documented" result is, if anything, conservative.

**3–6.** Not re-read: the ASA URL now returns HTML, not the PDF [GAP]. The repo's summary matches the quoted text for **externalizing** only. RESULT.md's "no worse … on behaviour" drops the internalizing index, which the quote does not cover. **Verdict: SOUND (cross-sectional, LA only); repo wording slightly broad.** Corrected: "no worse than children of US-born mothers on the externalizing index (internalizing not stated)."

---

## 6. Abramitzky, Boustan, Jácome & Pérez 2021, *AER* 111(2):580–608

**1. Repo claim.** literature.md:1: "exclude children of unauthorized parents because the tax link needs SSNs". RESULT.md:160: "cannot see children of unauthorized parents at all".

**2. Capture.** Census/ACS records get PIKs through the Census Person Identification Validation System, which matches against SSA Numident [TRAINING-DATA]. Children are linked to parents through the 1040 returns that claim them as dependents (Chetty et al. method) [TRAINING-DATA]. The paper states: "we are not able to observe pairs for which either the child or the parents lack a Social Security Number … restricted to children who are either US citizens or authorized immigrants … and whose parents are also US citizens or authorized immigrants"; coverage is about 79% of Hispanics against about 100% for other groups [SOURCE: w26408 pp. ~20–21, lines 457–507].

**Selection.** Exclusion depends on the parent **lacking an SSN in the tax years used**, not on having been unauthorized. For the 1978–83 birth cohorts, parents legalized under IRCA in 1987–88 had SSNs by the 1990s and stay in the sample [INFERENCE from IRCA timing plus the SSN rule]. What drops out is the roughly 21% of Hispanic children whose parents never gained status or an SSN, or never filed. The retained Mexican sample is therefore positively selected, and Mexican-origin mobility is **overstated** relative to all children of Mexican immigrants [INFERENCE]. That runs against the pro-immigration reading and in favour of this repo's caution.

**6. Verdict: SOUND (descriptive); repo wording OVERSTATED.**
- RESULT.md "cannot see children of unauthorized parents at all" → "excludes children whose parents never obtained SSNs (about 21% of Hispanic children); children of parents legalized under IRCA are included."

---

## Repo's own reading: other overstatements

- Ladder 186's "Published evidence runs the same way" lists three effects as a series. Each rests on one study, and the lower CI bounds are 0.6 points, about 5 g per applicant and not reported. Suggested replacement: "Published quasi-experiments agree in sign but are imprecise: DACA age eligibility −4.3 points (CI 0.6–7.9) on diagnosed anxiety/adjustment disorders (Oregon RD); IRCA +34 g average-county birthweight (≈96 g per applicant extrapolated, t ≈ 2; 65 g composition-adjusted); DACA mothers' children +5 points Medicaid with no gain in total coverage."
- literature.md:1 grades Hainmueller "A" and calls DACA "protection". The study measures eligibility (ITT), not protection or receipt. A− is fairer given one state, no first stage and a winner's-curse-sized estimate.
- RESULT.md:147–149 is accurate on 2.04/1.51/1.24 but should carry "(IV standard error not reported)".
- The repo already flags the Bean unknown-status mix (row 1b), which is to its credit.

## Summary table

| Study | Repo use | Weakest pipeline stage | Precision | Politicization signal | Verdict |
|---|---|---|---|---|---|
| Hainmueller 2017 | DACA → child diagnoses −4.3/−4.5 | Eligibility = age only; DACA receipt unobserved (small first stage makes ITT implausibly large) | CI 0.6–7.9 on 7.9% baseline; p = .023; one state | Ford/RSF; discussion extrapolates to green cards | SOUND BUT IMPRECISE; OVERSTATED IN REPO |
| Cascio–Cornell–Lewis 2024 | IRCA → +96 g | County-level exposure, no person link; composition | log 0.0263 (SE .0127), t ≈ 2.1; avg county 34 g | None seen | SOUND BUT IMPRECISE; OVERSTATED IN REPO |
| Bean et al. 2011 | 2.04/1.51/1.24 years | Child-recalled parent status; unknown/never-migrated pooled with unauthorized | IV: no SE, no first-stage stat | Legalization-advocacy book framing | MEASUREMENT RISK (overstates gap); OVERSTATED (IV) |
| Tran 2025 | +5 pts child Medicaid, "improve" | Imputed parent status | not re-parsed | None seen | OVERSTATED IN REPO (framing: substitution, no coverage gain) |
| Amuedo-Dorantes & Antman 2016 | −38% household poverty | Non-citizen proxy includes LPRs | CI 13–62%; near-poverty n.s. | None seen | SOUND BUT IMPRECISE |
| Landale 2015 | contrary result | Self-reported status (bias toward conservative gap) | not re-read | None seen | SOUND; repo wording slightly broad |
| Abramitzky et al. 2021 | mobility excludes unauthorized children | SSN/PIK linkage (79% Hispanic coverage) | descriptive | None seen | SOUND; repo "cannot see at all" OVERSTATED |

Fabrication: no study shows signs of fabricated or unreproducible data. Hainmueller's data are restricted but its code is public. Cascio and Bean use public or archival sources.

## Coverage

- **Done at source (text parsed this session):** Hainmueller main text, Cascio (intro, §IV–V, Table 2 log column), Bean (IV section, footnote 8, Table 1 lines), Amuedo-Dorantes & Antman (sample, Table 3), Abramitzky et al. w26408 linkage passage.
- **Not re-read:**
  - Tran 2025 (relied on literature.md's Exa-verified quotes; no SE parsed) and Landale 2015 (the ASA URL returns HTML). Next step: `fetch_paper` doi:10.1111/coep.70009 and doi:10.1177/0022146514567896.
  - The Hainmueller supplement (the science.org and author-site SI URLs returned HTML). It may report the eligible share or first stage, which would settle the ITT-plausibility point [GAP].
  - Cascio's grams-column SE.
- **Not searched:** published comments or replications for any of the seven (budget). Suggested queries: "Hainmueller 2017 DACA mental health reanalysis", Crossref "is-referenced-by" on doi:10.1126/science.aan5893.
- **Budget:** about 13 turns against 12.
