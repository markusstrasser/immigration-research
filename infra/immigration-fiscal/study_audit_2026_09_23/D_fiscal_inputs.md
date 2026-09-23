**Verdict:** No sign that any of the six inputs is fabricated or unreproducible. Borjas's rules are printed in full and the repo reproduces the residual exactly. The Wilson–Zhou and Colas–Sachs tables match their text. CBO's coefficients and the repo's 63–66% arithmetic agree, and the CPS under-reporting correction has already been run in the repo. Colas–Sachs (a calibrated model, correctly labelled in the repo), the CBO school response and the CPS under-reporting correction hold. The residual population estimates are SOUND BUT IMPRECISE, with the imprecision concentrated in the 2021–24 cohort, and so is Wilson–Zhou: its housing first stage is F ≈ 14, not the F ≈ 30 of its labour sample. **The most consequential problem is the Borjas imputation. It is an unvalidated individual-level classifier, and two of its rules decide status from the outcomes the repo later compares.** Rule (b) accepts self-reported citizenship. Rules (c) and (f) classify anyone receiving Medicaid, SSI, Social Security or housing subsidies as legal. Any benefit or outcome comparison by imputed status therefore understates benefit use among the "unauthorized" by construction. The legal share among low-education benefit users (ladder 185) leans upward from the same rules. No validation of this rule set against a status-bearing survey on the 2025 CPS exists in the repo, and I could not retrieve one this session. Ladder 625 also slightly overstates Wilson–Zhou; corrected wording is below.

Model: claude-opus-5-5 (Opus 5.5, 1M). Date 2026-09-23. Scratch copies of the primary PDFs are in this session's scratchpad (not the repo).

---

## 1. Borjas 2017, residual imputation of unauthorized status in the CPS

**Repo claim.** `infra/immigration-fiscal/status_impute_2026_09_16/impute_status.py:2-30` quotes the nine rules verbatim from NBER w22102 pp. 10–11. `research/immigration-unauthorized-population-size-2026-09-19.md` §3 reports that the unmodified rules give 14,896,401 on CPS ASEC 2025 (SE 316,399) and 12,973,901 on ACS 2024, and uses the result as the "repo's own residual". Today's `parent_status_2026_09_23` lane also uses these rules (ladder 185: about half of low-education Mexico-born parents are legal).

**Data capture pipeline, with the sign of the error on the unauthorized count or share.**
1. Census interviews a household member, who self-reports country of birth, year of arrival and citizenship; no status question exists. Proxy reporting is common. Sign: see stage 2.
2. Rule (b) makes self-reported citizens legal. Non-citizens, especially recent Mexican-born arrivals, over-report naturalisation in Census surveys (Van Hook & Bachmeier 2013, *Demographic Research* 29; Brown et al. 2018, Census CARRA WP 2018-02) [TRAINING-DATA; my download of the CARRA PDF returned the wrong document, so this is **[UNVERIFIED]** this session]. Sign: **fewer classified unauthorized**, and misreporters are assigned to the legal group.
3. Rules (c) and (f) make recipients of Social Security, SSI, Medicaid, Medicare, military insurance or housing subsidies (or their spouses) legal. The CPS imputes and misreports program receipt (item 6). Unauthorized adults can appear on Medicaid through emergency or state-funded coverage or household-level misreporting. Sign: **fewer classified unauthorized**, and it is **mechanical**: an imputed-unauthorized person has zero receipt of these programs by definition. `research/immigration-measurement-uncertainty-2026-09-05.md:17` already names this circularity.
4. Rules (d), (e) and (h) (veteran, government worker, licensed occupation) are sound in principle. Rule (h) needs a code list the paper does not print, so the lane supplies one [INFERENCE]. Dropping it adds 2.2% (memo §3).
5. Rule (g): Cuba is the only refugee origin. The wide refugee list subtracts 4.4%.
6. Rule (i): a spouse of a legal immigrant or citizen is classified legal. Mixed-status couples exist, so the sign is **fewer unauthorized**.
7. The residual is every other foreign-born person, so lawful permanent residents and temporary visa holders who arrived after 1980, are not citizens, receive no benefits and work in the private sector all count as "unauthorized". Sign: **more classified unauthorized**. Passel & Cohn (2014) say the logical-edit step alone gives "too many" undocumented. Pew therefore adds a probabilistic assignment and reweights to DHS totals. Borjas stops before that step [SOURCE: w22102 pp. 9–10, quoting Passel & Cohn 2014 p. 23].
8. Linkage and denominator: none. The count is the weighted residual. CPS weights are controlled to Census population estimates, which undercount recent humanitarian arrivals (memo §4).

Stages 2, 3 and 6 push the count down and stage 7 pushes it up. The CPS total of 14.9M falls inside the published 14.6–15.8M, but an aggregate match can come from offsetting individual errors. It does not validate who is assigned to which group.

**Design and precision.** The rules classify; they identify nothing causally. The SDR standard error (316k) covers sampling only. Classification error is larger, and the repo has not quantified it at the person level. The rule sensitivities (+2.2%, −4.4%) are the only classification sensitivity the repo reports.

**Replication and critique.** The published validation of logical-edit methods against a survey with status questions is Van Hook, Bachmeier, Coffman & Harel (2015, *Demography* 52, "Can We Spin Straw Into Gold?"). It uses SIPP 2008 status items and compares logical edits with multiple imputation. My recollection is that it finds logical edits misclassify materially and favours multiple imputation, which is the basis of the MPI method [TRAINING-DATA, **[UNVERIFIED]**: not retrieved within budget]. Borjas benchmarks his extension against Pew's constructed 2012–13 ASEC files, to which Passel gave him access (w22102 pp. 9–11); I did not extract the agreement table [GAP].

**Politicization.** Borjas is a restrictionist-leaning labour economist. The rules come from Passel's Pew and Census method, which is not restrictionist, and they are printed in full. The imputation is transparent, and no author-side distortion is visible. On the symmetry test: the repo accepts residual status imputation here, and it should apply the same person-level misclassification caveat to any opposite-side study built on the Pew or MPI imputations.

**Verdict: MEASUREMENT RISK.** The count is roughly right in aggregate, with opposing errors (stages 2, 3 and 6 down; stage 7 up). For comparisons by imputed status, the direction is fixed. Benefit receipt among the "unauthorized" is understated by construction and moved into the legal group. Citizenship over-reporting also moves some unauthorized people into the legal group. Ladder 185's "about half legal" is therefore more likely overstated than understated among benefit users [INFERENCE]. Nothing suggests fabrication. [GAP] Suggested next step: retrieve Van Hook et al. 2015 and Brown et al. 2018 and quote their misclassification rates, then run the parent_status result with rule (c) and rule (f) dropped as a sensitivity.

---

## 2. Residual population estimates (DHS OHSS, Pew, MPI, CMS, CIS)

**Repo claim.** `research/immigration-unauthorized-population-size-2026-09-19.md` reports 14.6–15.8M for mid-2024 on the broad definition and 8–9.5M on the narrow one.

**Pipeline.** The ACS or CPS foreign-born count is the starting point: self-reported birthplace and arrival year, with weights controlled to Census estimates. The legal stock (LPR admissions, refugees, naturalisations and temporaries from DHS administrative records, less mortality and emigration) is subtracted. The residual is inflated by an assumed undercount rate. The weakest stage is the coverage rate, which every publisher **assumes**. Only the post-enumeration survey measures coverage, and it gives a net decennial rate for all Hispanics (memo §7). Published rates (memo §2 table): DHS 13% at arrival, decaying 7.5% a year; CMS 5% before 2021 and 37% for 2021–24; CIS a flat 2.25%; Pew and MPI apply a rate they do not print [SOURCE: memo §2, `derived/published_definitions.md`]. The error falls mostly on the 2021–24 cohort, which moves from 4.11M counted to 4.21–11.75M depending on the scheme. Every earlier cohort moves by less than 6%.

**Precision.** Publishers give no sampling SE on coverage-adjusted figures. The spread across publishers (14.0–15.8M, 2023–24) is the practical uncertainty.

**Funding and advocacy.**
- DHS OHSS is a government statistical office.
- Pew is funded by the Pew Charitable Trusts, is non-advocacy and uses Passel's method.
- MPI is foundation-funded and its policy work leans pro-immigration.
- CMS (Center for Migration Studies of New York, Scalabrinian and Catholic) is a pro-migrant advocacy organization. Its estimator is Warren, the former INS residual-method author.
- CIS is restrictionist.

[TRAINING-DATA for the funder characterisations.] The symmetry test passes. Restrictionist CIS uses the smallest undercount rate and reaches the highest January 2025 figure through a smaller legal stock. Pro-migrant CMS uses the largest rate for recent arrivals. The advocates' estimates bracket each other within about 1M, so neither side's ideology shows up as a directional bias in the headline.

**Verdict: SOUND BUT IMPRECISE.** The imprecision sits in the 2021–24 cohort's coverage. DHS, CMS and CIS publish their assumptions; Pew and MPI do not print their rate. No sign of fabrication. The repo memo already states the limits correctly.

---

## 3. Colas & Sachs 2024, AEJ: Policy, indirect fiscal benefit of about $750

**Repo claim.** `research/immigration-confidence-ladder.md:605` cites "indirect fiscal benefit ≈ $750/yr (WP range $770-2,100) … Flips the total to surplus in NAS's more optimistic scenarios". Ladder 54 (line 35) reframes it as "a positive modeled channel, not a universal upper-bound theorem". `research/immigration-claim-scorecard-2026-09-18.md:75` also cites it.

**What is measured and what is modelled** [SOURCE: local copy `sources/immigration-fiscal/data/external/lifetime/econstor/colas_sachs_2024_indirect_fiscal_benefits_low_skill.pdf`, parsed with pdftotext].
- **Measured:** effective marginal and participation tax rates for each ACS individual via TAXSIM. The income-weighted rates are T̄′u = 30.3% for low-skilled and T̄′s = 36.6% for high-skilled workers. The paper states "a difference in marginal tax rates of 8.2%", but 36.6 − 30.3 = 6.3 points; the stated 8.2 may be a net-of-tax ratio or a different definition [UNVERIFIED, flag only].
- **Modelled:** the wage effects, which come entirely from a calibrated elasticity of substitution σ between high- and low-skilled labour. The preferred value is σ = 2 (Card 2009's 1.5–2.5), with κs = 0.79. No immigration shock is estimated.
- **Sign driver.** The benefit arises because low-skilled immigrants raise high-skilled natives' wages, which are taxed at the higher effective marginal rate, and lower low-skilled natives' wages. The sign therefore rests on high-skilled effective marginal rates exceeding low-skilled ones, including benefit phase-outs. The magnitude scales inversely with σ.
- **Table 2:** $1,003 / $753 / $602 at σ = 1.5 / 2.0 / 2.5 with no labour-supply response, and $1,132 / $913 / $765 with an endogenous labour-supply response.
- **Robustness:** across alternative models the range is "$750 to $1,900" (text p. 3). The repo's "$770–2,100" is the working-paper range; label it that way.
- **The paper's own limit:** "high school dropouts are a fiscal negative even after accounting for the indirect effects". Only high-school graduates switch to surplus.

**Precision.** The paper reports no confidence interval; the uncertainty is the σ range and the choice of model. Pre-registration does not apply to a calibration exercise.

**Critique.** It is peer-reviewed (AEJ: Policy, doi 10.1257/pol.20220176). I found no published comment [GAP: no citation-graph search run]. The obvious critique is that the benefit is a within-native redistribution (low-skilled natives lose wages while the Treasury gains), and any Borjas-style low σ within skill cells changes the split between the two.

**Politicization.** The abstract says the benefit "may outweigh" the direct effect, and the body qualifies this correctly for dropouts. The paper frames itself against the NAS report "cited by Donald Trump" (p. 2), a mild framing signal only. The repo's own population of interest is low-education Mexican-origin, the dropout-heavy case where the paper itself says the burden remains.

**Verdict: SOUND** as a calibrated model. Ladder 54 describes it correctly. For ladder 605, relabel the range as "published robustness range $750–1,900 (WP $770–2,100)". Also add: "for high-school dropouts the paper finds a net burden remains."

---

## 4. Wilson & Zhou 2026, Dallas Fed WP 2607, housing

**Repo claim.** `research/immigration-confidence-ladder.md:625` states: "+2.2% house prices, +1.4% rents, with supply/permit response statistically null (confirming the inelastic-supply mechanism entry 18 could only infer)". `research/immigration-hedonic-composition-amenity-2026-09-19.md:32` compares the repo's +1.32% with W–Z's +1.4%.

**Data capture** [SOURCE: wp2607.pdf, pp. 3–12, Table 6].
1. Entry: a person is encountered at the border or in the interior and issued a Notice to Appear. EOIR (DOJ) immigration-court records give nationality, age and **self-reported residence zip code**. CBP data cover parole.
2. Exits: removals, voluntary departures and new detention bookings.
3. Gaps: got-aways and overstays are not in the court data by location. Addresses are declared at NTA and are stale after internal moves. Sign: classical-type noise in local flows attenuates OLS toward zero; systematic misallocation of addresses to gateway metros is not classical.
4. Worker conversion: flows are multiplied by the ACS employment rates of recent immigrants from the same origin, giving UIWF (unauthorized immigrant worker flows).
5. Outcomes: Zillow ZHVI and ZORI for 348 and 280 MSAs.

**Design and precision.** A two-way leave-out shift-share IV (Card 2001, Burchardi et al. 2019). The **housing** first stage has Kleibergen–Paap **F = 13.64 (rents) and 14.02 (prices)** with a coefficient of about 0.79 (SE about 0.21). The headline "F near 30" belongs to the CZ labour sample. The ancestry IV has F = 7 and the conventional shift-share F = 14. Rents are 1.438 (SE 0.344), a 95% CI of about 0.76–2.11. Prices are 2.189 (SE 0.741), a CI of about 0.74–3.64 [CALCULATION ±1.96 SE]. At F ≈ 14, a tF-adjusted test (Lee et al. 2022) widens the intervals. The rent t of about 4.2 survives; the price t of about 2.95 is closer to the edge [INFERENCE, approximate]. With the alternative CoreLogic and Freddie Mac price indexes, effects are about 1% with larger SEs (text p. 42). Permits under IV are small and insignificant.

**Replication.** It is an unrefereed working paper. The repo's own panel gets +1.32% rents (SE 0.42) with a different treatment (population share, not employment), so the rent magnitude cross-checks. Disconfirmers are already in ladder 625: JCHS and Yale Budget Lab on timing, Cabral–Steingress on aggregate size.

**Politicization.** The authors are Federal Reserve researchers, and nothing in the paper looks like advocacy. The abstract matches the table.

**Verdict: SOUND BUT IMPRECISE, and slightly OVERSTATED IN REPO.** Ladder 625 says "supply/permit response statistically null (confirming the inelastic-supply mechanism…)". Corrected wording: "the IV permit response is small and statistically insignificant, which is consistent with inelastic short-run supply but does not establish it. The house-price effect is 2.2% (95% CI about 0.7–3.6, housing first-stage F ≈ 14) and about 1% on alternative indexes." The repo's Decker and Smith dismantle memos already say this; ladder 625 lags them.

---

## 5. CBO school-spending response behind the repo's 63–66%

**Repo claim.** `research/immigration-complete-annual-account-2026-09-20.md:139-149` states that CBO associates +1 pp of enrollment growth with −0.37 pp of per-pupil spending growth (decline side −0.34), giving first-order total responses of 63% and 66%. FAQ entry 2 repeats this (`research/immigration-objections-faq-2026-09-21.md:62-65`).

**Source.** CBO, *Effects of the Surge in Immigration on State and Local Budgets in 2023*, June 2025 (publication 61464). The education section and technical appendix are quoted in `notes/immigration-service-response-external-evidence-2026-09-20.md:15-17`. The source is a 1999–2000 to 2019–20 state panel with state fixed effects. Today cbo.gov served a 767-byte stub to curl, so **I could not re-read the primary today** [UNVERIFIED this session; the 2026-09-20 lane quoted it].

**Arithmetic check.** Total spending = enrollment × per-pupil spending, so d ln(total) = d ln(enrollment) + d ln(per-pupil) = 1 − 0.37 = 0.63 for growth and 1 − 0.34 = 0.66 for decline. The repo reads CBO correctly [CALCULATION]. The repo also scopes it properly: the response applies only to the school current-consumption share (71.5–86.5% of education) rather than the whole deficit, it is not described as causal, and CBO's zero response for defense, interest and general services is labelled a repo assumption, not a CBO estimate.

**Remaining caveat.** The coefficient is an association from small year-to-year enrollment changes within states. Transporting it to an established all-age population is an extrapolation, and the repo says so (lines 180ff).

**Politicization.** CBO is nonpartisan. None.

**Verdict: SOUND.** The arithmetic and scope are correct. [GAP] Re-fetch the CBO PDF with a browser-grade fetch to re-verify −0.37/−0.34 verbatim.

---

## 6. CPS ASEC benefit under-reporting

**Repo claim and correction.** The repo **does correct** for under-reporting, twice:
- `infra/immigration-fiscal/ledger_underreport_2026_09_16/RESULT.md`: proportional, false-negative Monte Carlo and differential arms built from published ratios (NBER w21399, Meyer–Mok–Sullivan; w32860; w35680). No arm moves the Mexican second-generation versus white gap by more than $269 per adult, against −6,066 / −8,286. The proportional arm gives +93. The false-negative arm narrows the gap by +269. The differential arms widen it by −10 to −151 [DATA].
- `research/immigration-administrative-checks-2026-09-19.md:78-120`: the existing multipliers (SNAP, SS, SSI and UI ratios transported from income-year 2017) leave raw gaps of −5.85% to −8.72% against 2024 administrative totals. Replacing them with current ratios makes the target balance **$4.9–6.7bn more negative** [DATA].
- Medicaid is valued against CMS administrative spending (`health_admin_2026_09_20`), not survey receipt.

**Stale text.** `research/immigration-welfare-use-by-generation-2026-09-16.md:65` still says under-reporting "lowers every level here by roughly a quarter … no evidence either way in this session" [TRAINING-DATA]. The later lanes supersede it, and it should point to `ledger_underreport_2026_09_16`.

**Differential by nativity or status.** I did not verify this session whether under-reporting differs by nativity. Linked-record studies (Meyer, Mittag & Goerge 2022 JHR; Celhay, Meyer & Mittag on correlates of false negatives) exist [TRAINING-DATA, **[UNVERIFIED]**]. Fear of reporting in mixed-status households is plausible but unmeasured here.

**Sign on the gap.** Consider the case where Mexican-origin or immigrant households under-report more than the white reference. The repo's proportional scaling then under-allocates transfers to them, and the true gap is **more negative** than reported. Unmeasured differentials therefore bias the headline toward a smaller cost [INFERENCE]. The repo's own differential arm points the same way, but only by −37 to −151.

**Verdict: SOUND** as handled. There is a small residual **MEASUREMENT RISK toward understating the gap**, bounded at hundreds of dollars per adult by the repo's arms.

---

## Summary

| Study | Repo use | Weakest pipeline stage | Precision | Politicization signal | Verdict |
|---|---|---|---|---|---|
| Borjas 2017 imputation | Unauthorized count 14.9M; parent_status (ladder 185) | Self-reported citizenship plus benefit-receipt rules; residual LPRs | Sampling SE only; person-level misclassification unquantified | Author restrictionist-leaning, method Pew's and public; none in the data | MEASUREMENT RISK: benefit use of imputed unauthorized understated by construction; legal share among benefit users biased up |
| Residual estimates (DHS/Pew/MPI/CMS/CIS) | Denominators, 14.6–15.8M | Assumed coverage for 2021–24 arrivals | No SE; 2021–24 cohort 4.2–11.75M | Advocates on both sides bracket each other; Pew and MPI don't print their rate | SOUND BUT IMPRECISE |
| Colas & Sachs 2024 | Indirect +$750 per low-skilled immigrant (ladder 54, 605) | σ calibrated, not estimated | $602–1,003 across σ; $750–1,900 across models | Mild framing against the NAS report; body qualifies dropouts | SOUND (model); relabel range, add the dropout caveat in ladder 605 |
| Wilson & Zhou 2026 | +2.2% prices / +1.4% rents (ladder 625, 182–183) | EOIR self-reported address; got-aways and overstays unlocated | Housing F ≈ 14; rents CI 0.76–2.11; prices CI 0.74–3.64 | None (Fed researchers) | SOUND BUT IMPRECISE; ladder 625 "confirming" overstated |
| CBO school response | 63–66% (complete account, FAQ 2) | Within-state association of small enrollment changes | Directional sensitivity pair | None | SOUND (arithmetic correct) |
| CPS under-reporting | Adjustment plus under-reporting lane | Nativity differential unmeasured | Arms move the gap ≤ $269 | None | SOUND; small risk toward understating the gap |

## Coverage

- **Done:** all six. Primary texts read this session: Borjas w22102 (rules and the Passel–Cohn passage); Wilson–Zhou wp2607 (data section, Table 6, first-stage text); Colas–Sachs local PDF (Table 2, calibration, dropout result, tax rates); the repo's CBO quote note; the under-reporting and administrative-check lanes.
- **Not retrieved:**
  - Van Hook et al. 2015 and Brown et al. 2018: my CARRA download returned an unrelated minimum-wage paper, and the turn budget ran out, so their misclassification rates stay [UNVERIFIED].
  - The CBO 61464 primary: cbo.gov returned a stub to curl.
  - Meyer–Mok–Sullivan JEP: aeaweb returned HTML.
  - Linked-record nativity differentials in under-reporting.
  - Borjas's agreement table against Pew's 2012–13 files.
  - Any citation search for comments on Colas–Sachs.
- **Suggested next queries:** "Van Hook Bachmeier Coffman Harel 2015 Demography legal status imputation SIPP"; "Brown Heggeness 2018 citizenship ACS administrative records noncitizen report citizen"; "Celhay Meyer Mittag survey program participation false negatives covariates immigrant"; fetch the CBO 61464 PDF via firecrawl.
