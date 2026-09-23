# Integrity audit of the external studies behind the current conclusions (2026-09-23)

**Verdict:** None of the 26 external studies and data inputs audited shows signs of fabricated or
unreproducible data; each has public data, a replication deposit or a named agency access route.
Measurement flaws at data capture run in both directions, usually toward the author's own
conclusion, and the two clearest cases come from advocacy sources on opposite sides: Cato counted
Texas offenders of "unknown or other" status as native-born, and Lott used an Arizona "deportable"
flag that includes some legal immigrants (he bounded that error at 10–21%). The repo's own text
went beyond its source 18 times: 14 in the direction favourable to immigration, legalization or
birthright citizenship, 3 against, and once both ways. Most of that split is composition. Of the 26
sources, 18 report favourable results, and the repo overstated two-thirds of the studies on each
side, usually by quoting a point estimate without its interval or the population it was measured
on. The directional remainder is small but real: the two double standards the audit found both
favour immigration. The repo dismissed Lott's Arizona study over a contaminated status flag, an
unsourced claim that the Arizona prison department had confirmed the error, and Lott's affiliation,
while it rated Texas data contaminated in the opposite direction as robust. It also accepted a
Hispanic-ethnicity proxy for immigrant status in Freedman, Owens & Bohn that it treats as a bias
elsewhere. Every overstatement found has been corrected where it was made.

Question from the operator (2026-09-23): "check other studies we rely on that they're not FAKE or
politicized (starts at data capture)". Trigger: in chat the German jus soli result had been quoted
as cutting boys' crime by half (see the §3.1 revision in the
[generational crime mechanisms memo](immigration-generational-crime-mechanisms-2026-09-16.md)).

## Method

Four researcher subagents (Opus 5.5), one per cluster, followed a shared
[brief](../infra/immigration-fiscal/study_audit_2026_09_23/BRIEF.md). For each study they traced
the pipeline from data capture (who recorded status, ethnicity, crime or benefits, how, and where
residual categories go), then design and precision, replication and critique, politicization
signals (funding, advocacy ties, abstract against tables, and whether the repo applies the same
critique to studies on the other side), and whether the repo's wording matches the paper. Before
editing, the parent session checked the numbers each correction rests on against the primary text:
Hainmueller's interval, Cascio's 34 g and 65 g, Abramitzky's Social Security number rule, Light's
extreme-case footnote, Lott's contamination bound and Cato's later note that detainers undercount,
Freedman–Owens–Bohn's enactment estimate, Gunadi's murder coefficient, and Pinotti's Table 3
(re-fetched after the agent's local copy turned out to be a different paper). Cato's relabelling was
checked against the primary quotes in the 2026-09-16 classification notes, not re-fetched. The
parent audited the German study before the agents ran. Labor-market papers were audited on
2026-09-17 ([canon citation audit](immigration-canon-citation-audit-2026-09-17.md)) and
crime-statistics pipelines on 2026-09-16
([bias mechanisms](immigration-crime-statistics-bias-mechanisms-2026-09-16.md)); neither was redone.

## Results by study

"Finding favours" and "Lean" are judgements [INFERENCE]; "favourable" means favourable to
immigration, legalization or birthright citizenship.

| Study | Finding favours | Audit verdict | Where the repo went beyond it | Lean |
|---|---|---|---|---|
| Andres et al. 2026, German jus soli | birthright | sound design, imprecise: −70% of treated youth crime, 95% interval −16% to −125% on 24 clusters; children of parents with 8 years' legal residence | "cut boys' crime by half", used as an argument about US birthright | favourable |
| Hainmueller et al. 2017, DACA mothers | legalization | sound, imprecise: −4.3 points on a 7.9% base, 95% CI 0.6–7.9; age eligibility only, one state | "4.3–4.5 points" read as a measured effect of protection | favourable |
| Cascio, Cornell & Lewis 2024, IRCA | legalization | sound, imprecise: 34 g in the average county; the 96 g per applicant falls to 65 g with birth composition fixed; t ≈ 2.1 | "+96 g" | favourable |
| Bean et al. 2011, IIMMLA | legalization | measurement risk: unknown-status and never-migrated mothers pooled with unauthorized, which overstates the gap | IV of 1.24 years quoted with no SE or first stage | favourable |
| Tran 2025, DACA | legalization | Medicaid substitution, no coverage gain | "improve" | favourable |
| Amuedo-Dorantes & Antman 2016 | legalization | sound, imprecise: 95% CI 13–62%; near-poverty not significant | interval omitted (mild) | favourable |
| Landale et al. 2015 | status matters less | sound | "no worse on behaviour"; the quote covers the externalizing index only | against |
| Abramitzky et al. 2021 | immigration | sound; the SSN link drops about 21% of Hispanic children, flattering Mexican mobility | "cannot see children of unauthorized parents at all"; IRCA-legalized parents' children are in | against |
| Light, He & Robey 2020, Texas | immigration | measurement risk flattering the undocumented: 0.40 → 0.73 of the native felony rate on the authors' extreme recode; a second leak unbounded | "robust" | favourable |
| Cato, Texas convictions | immigration | "unknown or other" relabelled native; the extract date moved one year's rate from 8% below to 20% above the state rate | "closes the arrests ≠ guilt objection" | favourable |
| Cato PA 994, ACS | immigration | imputation inflates the illegal rate, so conservative for Cato | none | — |
| Lott 2018, Arizona | against | measurement risk inflating the undocumented rate; +94% to +121% on Lott's own bound; contested, not refuted | dismissed on an unsourced "AZ DOC itself confirms", an ad hominem, and a flaw tolerated in Light | favourable |
| Gunadi 2019, ACS | immigration | sound, imprecise; errors run both ways | none | — |
| Ousey & Kubrin 2018 | immigration | sound for an area-level association only | none | — |
| Baker 2015, IRCA | legalization | sound, imprecise: imputed county UCR, ecological, standard errors not read | none | — |
| Pinotti 2017, Italy | legalization | best design, imprecise: −0.6 pp on 1.1%, 95% CI about −1.2 to 0.0; all in likely fictitious domestic-worker sponsorships; unobserved expulsion biases it toward zero | "halves serious crime" | favourable |
| Freedman, Owens & Bohn 2018 | mixed | legalization phase null (0.003, SE 0.007); losing legal work access raised charges (0.037, SE 0.011) | read as legalization evidence; its ethnicity proxy accepted | favourable |
| Miles & Cox 2014 | immigration | sound; null only with county trends, −4% and significant without | generalized to all enforcement | favourable |
| Gunadi 2020, DACA | legalization | state-panel association; its murder coefficient implies about 340 murders averted per 100,000 recipients a year | property result used as mechanism support | favourable |
| Bersani & Pittman 2019 | immigration | sound, imprecise; the dyads carry a period confound | none | — |
| Borjas 2017 imputation | neutral | unvalidated person-level classifier; program users are legal by rule | gaps read as status effects; the Medicaid rule narrows the poverty gap (+19.7 → +10.2) and widens the insurance gap (+4.8 → +14.1) | both |
| Residual population estimates | neutral | sound, imprecise for the 2021–24 cohort | none | — |
| Colas & Sachs 2024 | immigration | sound as a calibrated model; dropouts stay a net cost | working-paper range ($770–2,100) quoted for the published $750–1,900; dropout result omitted | favourable |
| Wilson & Zhou 2026 | against | sound, imprecise: housing first stage F ≈ 14 | an insignificant permit response read as "confirming" inelastic supply | against |
| CBO school response | neutral | sound, used correctly | none | — |
| CPS under-reporting | neutral | sound; the correction was already run | a stale "roughly a quarter" line in the welfare memo | — |

[SOURCE: audit files [A](../infra/immigration-fiscal/study_audit_2026_09_23/A_crime_levels.md),
[B](../infra/immigration-fiscal/study_audit_2026_09_23/B_crime_causal.md),
[C](../infra/immigration-fiscal/study_audit_2026_09_23/C_children_status.md) and
[D](../infra/immigration-fiscal/study_audit_2026_09_23/D_fiscal_inputs.md), with quotes and page
references; the Borjas gap figures are the two rule sets in
[parent_status RESULT.md](../infra/immigration-fiscal/parent_status_2026_09_23/RESULT.md)]

## Which way the overstatements lean

The raw count, 14 favourable to 3 against, overstates the tilt, because most of the cited
literature reports favourable results:

| Studies whose finding | Number | Overstated in that direction |
|---|---:|---:|
| favours immigration, legalization or birthright | 18 | 12 (67%) |
| cuts against | 3 | 2 (67%) |
| is mixed, or a neutral input | 5 | — |

[CALCULATION: counts from the table above]

A repo that overstated every study at the same rate, whatever its direction, would produce this
split from these 21 studies. The habit is real and the same on both sides: quoting a point estimate
as settled. With three unfavourable studies, the equal rate is consistent with no directional
difference but cannot establish it.

The other four overstatements went beyond quoting. Two are double standards and both favour
immigration: the Lott dismissal and the ethnicity proxy accepted in Freedman–Owens–Bohn. One is a
critique overstated in the other direction (Abramitzky). The Borjas reading cut both ways. Four
cases cannot establish a direction, but the two most serious errors in the audit run the same way,
and they match the benefit-of-the-doubt pattern in [the LLM bias note](../notes/llm-bias-caveat.md).

## What changes in the conclusions

- **Crime by status.** Illegal immigrants in Texas are arrested less than natives on every
  published construction. How much less is not settled: 0.40 to 0.73 of the native felony rate,
  plus a second misclassification, also in their favour, that nobody has bounded. Arizona's
  opposite result is contested, not refuted.
- **Legal status and crime.** "Legalization reduces crime" rests on one well-identified but
  imprecise Italian design and one US county study. "Enforcement has no effect on crime" holds for
  deportation screening of people already arrested, once county trends are controlled; the one
  study of losing legal work access found felony charges rose.
- **Children and parents' status.** Every study points the same way, but each effect is a single
  noisy estimate. The two identified effects stop at age 12 (Hainmueller) and at birth (Cascio),
  and the only schooling estimate (Bean's IV) reports no precision. In today's CPS the imputation's
  Medicaid rule moves the poverty and insurance gaps in opposite directions; the schooling and
  employment gaps move little.
- **Fiscal account.** No input changes a value. In its own paper, Colas–Sachs's indirect benefit
  does not make high-school dropouts a net gain.

## Reading the pattern

- **Leading explanation.** Nothing is fabricated. Measurement flaws lean toward each author's
  conclusion on both sides. The repo's overstatements are mostly a direction-neutral habit that
  lands on the favourable side because most of what it cites is favourable, plus two double
  standards that both favour immigration.
- **Top alternative.** The tilt sits upstream, in which studies the repo cites: 18 favourable of
  26 could reflect the literature or the repo's selection, and this audit did not test which. A
  second alternative is the audit itself: it ran after the operator's complaint, through the same
  model family that wrote the original text, and may have looked harder in one direction.
- **Discriminating evidence.** A direction-blind search for unfavourable studies of comparable
  design on the three questions (crime by status, legalization and crime, children and parents'
  status): if the repo omitted several, the tilt is in selection. A blind re-grade of the 26 rows by
  a different model family, given the repo sentence and the paper's passage without the lean
  column, tests the audit.
- **Decision impact.** Already applied: ladder entries 45, 48, 49, 50, 144, 185 and 186 and the
  crime-rates memo were narrowed. No fiscal value moved.
- **Next action.** The operator decides on the protocol changes below. The direction-blind search
  costs one researcher epoch per question.

## Corrections applied

Commits e96d832 (German jus soli), 1154e67 (children), 703b5e5 (crime levels), f3f42dd (fiscal
inputs) and 8ac7d92 (crime causal), plus the commit that adds this memo, which qualifies the two
remaining −70% mentions in the mechanisms memo. Memo and ladder text was annotated in place with a
2026-09-23 note; the parent-status lane's RESULT.md and literature.md were rewritten to the audit's
wording.

## Proposed protocol changes (need the operator's yes)

If approved, these go into the project's [quant-bias checklist](../notes/quant-bias-checklist.md):

1. Quote every external causal estimate with its interval or standard error and the population it
   was measured on.
2. Before dismissing a study for a flaw, search the repo for studies on the other side with the same
   flaw, and grade both the same way.
3. Give an author's affiliation or reputation no weight in a grade, or apply it to every
   advocacy-affiliated source alike.
4. Report the lean of any audit's findings against the lean of the audited set, as above.

## Gaps

- **Crime levels:** Light's supplementary appendix (violent-only extreme case; whether
  prison-identified status is included); Cato PA 994 tables not re-parsed; Gunadi 2019 full text;
  the Washington Post fact check, so the Arizona prison department's position on its flag is
  unverified; Ousey–Kubrin moderators.
- **Crime causal:** Baker's standard errors (AER and SSRN blocked); Miles–Cox tables; Inkpen 2024;
  Hines & Peri on Secure Communities; Freedman–Owens–Bohn's conviction-rate table.
- **Children:** Tran and Landale not re-read; the Hainmueller supplement, which may report the
  first stage that decides whether a 4.3-point effect is plausible; Cascio's grams-column standard
  error; no search for published comments or replications.
- **Fiscal inputs:** Van Hook et al. 2015 and Brown et al. 2018 on status-imputation error rates;
  the CBO 61464 primary; Meyer–Mok–Sullivan; Borjas's agreement table against Pew's files; comments
  on Colas–Sachs.

## Revisions

- 2026-09-23: created from the four audit files after the operator's request.
- 2026-09-23 (later): the operator approved the four proposed rules; they are in
  `notes/quant-bias-checklist.md` with a fifth, pricing costs and benefits alike
  ([decision](../decisions/2026-09-23-evidence-symmetry-rules.md)). Concept affected: how
  evidence is graded and which channels are priced.
