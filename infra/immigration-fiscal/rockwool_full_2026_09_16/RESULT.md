# Rockwool Study Paper 283 — full-paper read

**Verdict:** **Ladder 72 does NOT stand as written. Three of its five clauses are confirmed, one is wrong, and one is not in this paper at all.** Confirmed: the descendant gap surviving above 200 in Denmark and the Netherlands (Fig. 3B terminal ~205 and ~265); New Zealand's nonwestern groups convicting below the majority in both generations; the general shape "immigrant gap is mostly composition, descendant gap is not." **Wrong:** Denmark's adjusted immigrant gap in 2017 is **not** negligible — the paper states the counterfactual Danish gap has been "relatively stable at an average of +20" over the last ten years (p. 14); only Norway goes to zero. **Not in the paper:** the MENAPT-vs-Southeast-Asian split. Study Paper 283 uses a **binary western/nonwestern** classification and says in a footnote it was forced to (p. 6 fn. 5) — there is no origin-country, regional, MENAPT or Southeast-Asian breakdown anywhere in its 63 pages. The "~70%" headline is also not a paper figure: the paper's own wording is "more than halved," and the per-country shares read off Figs. 2 and 3 run 63% to 100%, not 70%.

Model self-report: Claude Opus 5 (1M context), model ID `claude-opus-5[1m]`.

Provenance: [DATA: full PDF read, figures rendered at 200 dpi and read] [INFERENCE: verdicts, share-explained arithmetic, transfer judgments] [SOURCE: S3 URL below] [FRONTIER]

## Scope
Read the full PDF of Rockwool Foundation Study Paper 283 (2026), "A statistical
decomposition of nativity gaps in criminal convictions using full-population data
from five developed democracies", and verify every number ladder entry 72
(`research/immigration-confidence-ladder.md`) rests on.

## Findings

See checkpoints below. Claim-by-claim table in section 3.

## Gaps

- Resolved. See "Remaining gaps" at the end.

---

## Checkpoint 1 — paper retrieved and body read [DATA]

[SOURCE: https://rockwoolfonden.s3.eu-central-1.amazonaws.com/wp-content/uploads/2026/03/RF_Study-paper_283_A-Statistical-Decomposition-of-Nativity-Gaps-in-Criminal-Convictions-Using-Full-Population-Data-from-Five-Developed-Democracies_March2026.pdf]
Local: `rf283.pdf` (1,436,071 B, 63 pp, PDFium, CreationDate 2026-03-16), `rf283.txt`.

**Structural fact that governs every number below:** the paper declares on its title
page "Tables and figures: **0 tables, 4 figures**. Online supplements: Country profiles;
2 tables" (p. 3). Tables A1 (the ~1,200-cell composition means) and A2 (the data
comparability matrix) are **NOT in this PDF** — the bundled supplement (pp. 33-61) is
country profiles + references only. So every headline magnitude in ladder 72 is read
off a **line chart**, not a table cell. No point estimate for any year is printed
anywhere in the paper.

### 1. Sample and outcome definitions [DATA, pp. 8-9, 24-25]
- Countries: Denmark, the Netherlands, New Zealand, Norway, Sweden. **No Finland.**
- Sample: **men only**, **ages 15-30**, full population registers, repeated cross-sections.
- Outcome: binary, convicted of a penal-code violation within the year (1/0).
  Country penal codes differ (SWE excludes drug offences; DNK includes sale/trafficking;
  NZL has no penal code, comparability sought through offence categories). Authors argue
  this shifts levels between countries, not within-country group comparisons — and state
  that assumption "could not be formally tested" (p. 24).
- Majority population = born in country **with at least one parent born in country**
  (Scandinavian convention). This excludes Western immigrants and their children from
  the analysis entirely.
- "Second generation" is their term for children of immigrants, chosen because the age
  window is 15-30 (p. 7).
- Nonwestern is a **crude binary**. The paper says explicitly it could not obtain legal
  ground of residence in all countries "whereby we were forced to focus on the cruder
  western/nonwestern categorization" (p. 6 fn. 5). **There is no MENAPT coding, no
  origin-country breakdown, and no Southeast-Asian category anywhere in the analysis.**
- Years (Materials and Methods, p. 25): focus period **1991-2017**; DNK and SWE full
  window; **NOR 1995-2017**; NLD and NZL restricted to **2006-2017**. Individuals
  weighted by fraction of year resident and alive.
  **[GAP/internal inconsistency]** The Results text (p. 12) says "In 2018, the last
  available data year, conviction rates were below 3% for all groups in the European
  countries, except for second-generation men of nonwestern backgrounds in DNK (5%)."
  Methods says 2017. The paper contains both. Flag when citing a terminal year.

### 2. Method and covariates [DATA, pp. 10-11, 25-27]
- **Blinder-Oaxaca** (Jann 2008, Stata Journal 8(4):453-79, ref. 32), OLS linear
  probability model, run **separately per country** (data pooling across countries was
  forbidden for data-security reasons, p. 11) — so no formal cross-country test exists.
- Reported quantity is the **"differences in composition"** term of the two-term BO
  equation, i.e. the counterfactual where groups are identically composed AND face
  identical returns. Not Gelbach, not a sequential/KOB variance decomposition.
- Covariate clusters: **age**; **basic composition** (has children, married/cohabiting);
  **education** (completed level + missing-credential dummy); **labour market status and
  income** (employed / self-employed / unemployed / outside labour force, missing-status
  dummy, log equivalised household disposable post-tax income). For the second generation
  two extra clusters: **parents' education and labour market status** (father's and
  mother's level and status + missing dummies) and **parents' social influence** (parents
  married, parents convicted in previous 5 years, parents deceased).
- **Education was available only for the Scandinavian countries** (p. 15). NLD and NZL
  have no education cluster. NZL has the fewest variables overall (p. 11).
- Cluster-wise figures come from 18 separate decompositions for immigrants and 28 for the
  second generation, **pooled across all years within country** (p. 11).
- No neighbourhood covariate. No origin-country covariate.

## Gaps after checkpoint 1
- [GAP] Figure 3/4 point values still to be read off the rendered plots.
- [GAP] Tables A1/A2 not in this file; would need the separate online supplement.

---

## Checkpoint 2 — figures read [DATA]

Figures 1-4 are raster images on pp. 31-34 with **no numbers in the text layer**.
Rendered with `pdftoppm -r 200 -png` (`fig-31.png` … `fig-34.png`) and read visually.
**Figure 4 is the only place in the paper that prints numeric point estimates.**
All Figure 2 and Figure 3 values below are chart reads at the terminal year (~2017),
accurate to roughly ±10 gap points. [INFERENCE: chart reads]

### Figure 4 — per-cluster counterfactual change in the gap, pooled over years [DATA, p. 32]
Negative = closing the gap. Blank = variable cluster unavailable in that country.

| Cluster | | NOR | SWE | DNK | NLD | NZL |
|---|---|---|---|---|---|---|
| Age | immigrants | −3 | +8.9 | +5.9 | +0.8 | +14.1 |
| Age | 2nd gen | +9.3 | −9.6 | −2.6 | −0.3 | −20.7 |
| Basic (children, married) | immigrants | +10.5 | +19.6 | −1.3 | −5.5 | −33.9 |
| Basic | 2nd gen | +14.6 | +5.3 | −0.4 | −4.1 | −42.6 |
| Education | immigrants | −27.7 | −31 | −26.4 | — | — |
| Education | 2nd gen | −31.3 | −3.8 | −8.5 | — | — |
| Labour market + income (LMSI) | immigrants | **−58.2** | **−70.1** | **−61.8** | **−66.5** | +3.2 |
| LMSI | 2nd gen | −27.5 | −18.2 | −13.4 | −14.7 | +12.4 |
| Parents' education + labour market | 2nd gen | **−102.8** | −47.4 | −29.5 | −13.7 | +14.3 |
| Parents' social influence | 2nd gen | +19.6 | +1.7 | +0.5 | −5.3 | −8.2 |

Three things this table settles that no summary carries:
1. **Age works against the immigrant story.** Equalising age composition would *widen*
   the immigrant gap in four of five countries (immigrants are older than majority men
   in the 15-30 window). It narrows the second-generation gap instead.
2. **Education is missing for NLD and NZL.** Any claim that "own education" explains the
   Dutch immigrant gap is unsupported — that covariate does not exist in the Dutch model.
3. **The parental cluster is weakest exactly where the descendant gap survives.**
   Norway −102.8 and Sweden −47.4, but Denmark only −29.5 and the Netherlands only −13.7
   (where LMSI −14.7 is in fact marginally larger). The paper's prose claim that the
   parental cluster "generally represent[s] the largest estimates for the second
   generation" (p. 19) is true within DNK but overstated for NLD. [INFERENCE]

### Figures 2 and 3 — raw vs adjusted gaps at the terminal year [DATA, pp. 31-33, chart reads]

| Country | Immigrants raw (Fig 2A) | Immigrants adjusted (Fig 3A) | Share closed | 2nd gen raw (Fig 2B) | 2nd gen adjusted (Fig 3B) | Share closed |
|---|---|---|---|---|---|---|
| Denmark | ~130 | **~+20** | ~85% | ~305 | **~205** | ~33% |
| Netherlands | ~248 | ~+55 | ~78% | ~368 | **~265** | ~28% |
| Sweden | ~150 | ~+55 | ~63% | ~123 | ~+62 | ~50% |
| Norway | ~72 | **~0** | ~100% | ~100 | ~+60 | ~40% |
| New Zealand | ~−67 | ~−50 | advantage shrinks | ~−32 | ~−17 | advantage shrinks |

Paper's own prose anchors for these reads: immigrant gaps "would have been more than
halved" in all European countries; "For NOR, the gap would have disappeared"; for DNK
"During the past 10 years, the counterfactual gap has been relatively stable at an
average of +20"; NLD "would close by as much as 150 percentage points, from about 250 in
the uncontrolled results to about 100 in the counterfactual situation" (p. 14 — note this
150-point statement is about the *period average*, and the terminal-year Dutch solid line
sits lower, near 55); for DNK and NLD second generation "only about one-third of these
gaps in Figure 3 seems attributable to differences in composition" (p. 15).

Raw Figure 2 trajectory detail worth keeping: the **Danish second-generation raw gap
rose from ~190 in 2006 to ~305 in 2017**, and the *adjusted* gap rose with it from ~100
to ~205. The descendant gap in Denmark is not a legacy level, it is a rising one, and it
is rising net of composition. Same direction in the Netherlands (adjusted ~235 → ~265).

---

## 3. Claim-by-claim audit of ladder entry 72 [INFERENCE on [DATA] above]

| Ladder 72 clause | Paper value | Location | Verdict |
|---|---|---|---|
| "About 70% of the non-Western immigrant gap … is own education, employment and income" | Paper says gaps "would have been more than halved"; no 70% anywhere. Terminal-year shares closed by the **full** model (which also contains age and family composition): DNK ~85%, NOR ~100%, NLD ~78%, SWE ~63%. Education+LMSI **alone**, pooled: DNK −88.2, SWE −101.1, NOR −85.9 gap points; NLD has LMSI only, −66.5 | Fig. 2, Fig. 3, Fig. 4; pp. 14, 32 | **CORRECT IN DIRECTION, WRONG AS A NUMBER.** Replace "about 70%" with "more than halved in every European country, 63-100% at the end of the period", and drop "own education" from the Dutch case (no education variable exists there) |
| "in Denmark and Norway 2017 the adjusted immigrant gap is negligible" | **Norway: yes** ("the gap would have disappeared"). **Denmark: no** — "relatively stable at an average of +20" over the last decade; Fig. 3A terminal ≈ +20, a 20% higher conviction rate | p. 14, Fig. 3A | **HALF WRONG.** Strike Denmark, or restate as "reduced to about +20" |
| "the descendant gap survives at over 200% in Denmark and the Netherlands" | DNK adjusted ≈ 205, NLD adjusted ≈ 265 at terminal year; "only about one-third … attributable to differences in composition" | p. 15, Fig. 3B | **CONFIRMED** |
| "New Zealand's non-Western groups convict below the majority" | Immigrants raw ~−50 across the whole period (paper text) to ~−67 terminal; second generation between **−41 and −18** (paper text, p. 13); both stay negative after adjustment (−50 and −17), i.e. **adjustment shrinks the NZ advantage** — "immigrants to NZL are positively selected" | pp. 13-14, Figs. 2, 3 | **CONFIRMED**, with the addition that the advantage is itself compositional |
| "Southeast Asian origin in Denmark matches ethnic Danes since 2007-08 while MENAPT descendants stay about 3× after controls" | **Absent.** Binary western/nonwestern only: "we were forced to focus on the cruder western/nonwestern categorization" | p. 6 fn. 5; whole paper | **NOT FROM THIS PAPER.** The source memo already attributes it to "a companion 2026 analysis"; ladder 72 folds it into the 283 decomposition and must not. Source it separately or drop it |

### Further corrections to memo §9 wording [DATA, pp. 25]
- Coverage: **NOR 1995-2017, not 1993-2017**; **NZL 2006-2017, not 2007-2017**. DNK and
  SWE 1991-2017 and NLD 2006-2017 are right.
- **Internal inconsistency in the paper itself:** Methods says the focus period ends 2017
  (p. 25) while Results says "In 2018, the last available data year…" (p. 12). Cite the
  terminal year as "2017/2018 (the paper states both)".
- The covariate list is not just "own and parental education, employment and income" —
  it also carries **age**, **marital status / having children**, and a **parents' social
  influence** cluster (parents married, parents convicted in the previous 5 years,
  parents deceased).
- Author list is 11, not 8: add **Anders Nilsson, Peer E. Skov, Daniel J. Vigild**.
- The decomposition reports **only the composition term** of the Blinder-Oaxaca equation
  (p. 26); the "differences in correlations" term is estimated but not shown.

---

## 4. Mechanism, heterogeneity, and the paper's own limitations [DATA, pp. 17-24]

**Mechanism offered for the descendant gap.** Intergenerational transmission of parental
labour-market disadvantage: "the selective migration of low-skilled parents with poor
labour market prospects results in social disadvantage that transmits intergenerationally"
(p. 19). The authors then concede the residual: the null hypothesis that composition
explains everything "was rejected by the data in all comparison countries but Norway"
(p. 21), and they list three candidate sources for the residual they cannot separate —
differential returns ("discrimination"), unobserved correlates such as PTSD diagnoses,
and "features that are inherent to immigrants and their children … such as specific
culturally patterned ways of life" (pp. 21-22). That last phrase is the paper's own,
unhedged, and it is the sentence most likely to be quoted against a compositional reading.

**Origin-country heterogeneity: none.** No origin breakdown of any kind. The cross-country
contrast is the paper's entire heterogeneity argument, and it is explicitly *informal*:
data could not be pooled for security reasons, so cross-country differences "are forced to
infer … from the country profiles rather than formally testing" (p. 11).

**Limitations the paper states.** (a) Conviction measures "crimes that are reported,
solved, and have led to formal conviction … conviction is as much the product of a
judicial process as of actual behavior" (p. 24); crime reports could not be linked to
perpetrators. (b) Penal-code content differs across countries; the assumption that this
affects levels but not within-country group ratios "could not be formally tested" (p. 24).
(c) Institutional differences between NZL and Europe limit attributing the NZ reversal to
selective migration alone (p. 23).

**Limitations the paper does NOT state — [VERIFIED NEGATIVE], searched the full text:**
- **No differential-policing or enforcement-bias discussion as a measurement threat.**
  Discrimination appears only as a labour-market/school mechanism and as a name for the
  returns term. The words policing, enforcement bias and stop rates do not appear.
- **No selection into residence.** Nothing on return migration, emigration of convicted
  immigrants, deportation, or naturalisation moving people between the immigrant and
  majority categories. Given the "majority = born here with at least one parent born
  here" rule, naturalisation does not reclassify anyone, but return migration of the
  unsuccessful would bias the immigrant gap **downward** and is never raised.
- **No register-coverage discussion** beyond the weighting-by-time-resident sentence
  (p. 25). Undocumented residents are outside the registers entirely and are not mentioned.
- No standard errors, confidence intervals or significance tests appear on any figure.

---

## 5. What transfers to the US Mexican second-generation question [INFERENCE]

**Transfers.**
- The **design logic**: composition explains most of the first-generation gap and much
  less of the second-generation gap. That asymmetry is the finding worth carrying, and it
  is reproduced in four European countries independently.
- **Parental SES is the dominant second-generation covariate** where it is measured well.
  This is direct support for the selectivity-index result in ladder 75 (parents' education
  transmitted at ~0.8 points of BA share per point) arriving from a completely different
  data regime and a different outcome.
- **The New Zealand case is the closest thing in the literature to a placebo for
  "nonwestern" as a category.** Same crude coding, opposite sign, and the paper attributes
  it entirely to what kind of migration the country selected. That is an argument against
  reading any nonwestern/immigrant gap as a property of origin rather than of selection.

**Does not transfer.**
- **Composition of the treated group.** European "nonwestern" is predominantly MENAPT
  refugees and family reunification. Mexican migration to the US is labour migration —
  the NZ *motive* — but **negatively** selected on education (ladder 75: 9.9% vs 17.0%),
  where NZ's Asian and Pacific labour migrants are positively selected. Rockwool's own
  framing makes Mexico a third cell its design never observes: labour-motivated,
  negatively selected. Neither European nor NZ results predict it.
- **Outcome.** Annual conviction flow for any penal-code offence versus US
  institutionalization stock. Levels are not comparable, and the US measure sits at a far
  higher severity threshold. Ratio-to-majority is the only shared currency.
- **Sample.** Men 15-30 only. The US second-generation fiscal and institutionalization
  work in this repo runs adults of both sexes over wider ages.
- **Reference group.** "Majority" here excludes Western immigrants and their children,
  which has no US analogue; the repo's comparison is third-plus-generation whites.
- **The register itself.** Parental birthplace links make the second generation
  observable for the whole population. The US has no such link (ladder 71), which is
  precisely why this paper cannot be replicated on US data rather than merely being
  un-replicated.

---

## Follow-ups (≤5)

1. **Fetch the separate online supplement** (Tables A1 and A2). A1 is the ~1,200-cell
   composition-means table — the only way to see the actual education, employment and
   income gaps behind the decomposition — and A2 is the comparability matrix naming the
   30 comparability issues across 240 variables. Neither is in this PDF. Also 3 code files.
2. **Find and grade the "companion 2026 analysis"** carrying the MENAPT vs Southeast-Asian
   Danish split. Until it is identified, that clause of ladder 72 is unsourced.
3. **Rewrite ladder 72** per the audit table: drop "about 70%", strike Denmark from the
   negligible-immigrant-gap clause, move the MENAPT sentence to its own entry, fix the
   NOR/NZL coverage years, and change the rating from "summaries read, full paper not" to
   "full paper read; headline magnitudes are chart reads, the paper prints 0 tables".
4. **Check whether ladder 73's claim** that full-control studies "cut the immigrant gap by
   30-70%" should be widened — this paper's terminal-year range is 63-100%.
5. **The rising adjusted Danish descendant gap** (~100 in 2006 → ~205 in 2017) is a live
   finding for the mechanisms memo, which currently cites ROCKWOOL 2023 for the same
   widening residual on a different sample. Two independent Danish estimates of a widening
   *conditional* descendant gap is a stronger fact than either alone.

## Remaining gaps
- [GAP] Tables A1/A2 and the code supplement are not in this PDF; section 4's composition
  claims rest on the paper's prose summary of A1, not on A1 itself.
- [GAP] All Figure 2 and Figure 3 values are 200-dpi chart reads, ±~10 gap points. Only
  Figure 4 values are printed. Do not quote Fig. 2/3 numbers to better than two digits.
- [GAP] The paper's terminal year is internally inconsistent (2017 in Methods, 2018 in
  Results); unresolved from the text alone.
