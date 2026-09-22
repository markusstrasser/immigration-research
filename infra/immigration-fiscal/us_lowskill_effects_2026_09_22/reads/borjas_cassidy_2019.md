<!-- reader extraction, opus-low agent, 2026-09-22; every numeric row carries a verbatim quote re-found in the parsed corpus text with rg -F; parent spot-checked the rows cited in the memo -->
[UNVERIFIED] — descriptive/regression extraction from a single paper; no independent replication.

# Borjas & Cassidy (2019), "The Wage Penalty to Undocumented Immigration", Labour Economics 61: 101757

Paper source: /Users/alien/Projects/corpus/doi_10_1016_j_labeco_2019_101757/parsed.pymupdf4llm@0.3.4+cfg-99914b93/page.md
(The parsed file carries no printed page numbers; anchors below give section/table/figure plus the
line range in the parsed markdown, written as `L<n>`.)

**Verdict:** A descriptive Mincerian decomposition on ACS 2008–2016 with imputed undocumented
status showing that the ~35–41% raw legal/undocumented wage gap is almost entirely composition
(education, years-since-migration, English), leaving a 2–6% adjusted penalty; identification is
selection-on-observables and rests entirely on an unvalidated residual imputation, with only the
state-level second stage (shift-share IV, E-Verify timing) attempting causal identification.

## Population, period, unit

- Foreign-born workers in the American Community Survey, **2008–2016** cross-sections (2012–2013
  cross-checked against Pew-built CPS-ASEC files; life-cycle regression uses pooled 2006–2016 text,
  elsewhere stated as pooled 2008–2016). Unit = individual worker; second stage = state-year cell.
- Sample restriction: "persons aged 21–64 who are not enrolled in school, and who report positive
  wage and salary income in the previous calendar year, positive weeks worked, and positive usual
  hours worked weekly" (Sec. 2, L276–279). Self-employed excluded (Table 1 notes, L260–262).
- Outcome: log hourly wage = wage and salary income / (weeks worked × usual hours worked weekly).
- ACS 2012–2013 male sample sizes (H-1B-corrected): natives 980,270; legal 124,433; undocumented
  58,155 (Table 1, panel B, L257). Women: 933,459 / 115,854 / 30,519 (Table A1, L~1590).
- Not a Mexican-origin study. It is legal-status, not national-origin; country of birth enters only
  as fixed effects. No generational dimension, no natives-vs-immigrant causal design.

## How undocumented status is imputed (the residual method rules)

Warren–Passel (1987) residual logic at the *individual* level, via the Pew/Passel-Cohn (2014)
algorithm as reverse-engineered by Borjas (2017) and applied here to the ACS. A foreign-born person
is classified **legal** if ANY of (Sec. 2, L167–181):

(a) arrived before 1980; (b) is a citizen; (c) receives Social Security, SSI, Medicaid, Medicare or
Military Insurance; (d) is a veteran or currently in the Armed Forces; (e) works in the government
sector; (f) resides in public housing or receives rental subsidies, or is the spouse of someone who
does; (g) was born in Cuba; (h) works in an occupation requiring licensing (physicians, registered
nurses, air traffic controllers, lawyers); (i) has a spouse who is a legal immigrant or citizen.
Everyone not caught by (a)–(i) is the residual, classified undocumented.

ACS-specific deviations:
- **Condition (f) is dropped** for the ACS: "the ACS does not identify whether a particular
  household is living in public housing or receiving subsidized rents, and thus we omit condition
  _f_" (L186–189).
- ACS starts in 2008 because pre-2008 ACS lacks Medicare/Medicaid receipt (fn. 4, L204–205).
- **Authors' own H-1B filter added** on top of Pew: legal if (1) occupation commonly employs H-1B
  holders (computer/info-system managers, computer and mathematical, architecture and engineering,
  postsecondary teachers), AND (2) US residence ≤ 6 years, AND (3) at least a college graduate
  (L297–310, fn. 5). Motivation: Albert (2019) found the Pew algorithm "mistakenly classified around
  25% of college educated immigrants as undocumented" (L295). The filter cuts undocumented men with
  a college degree from 17.8% to 14.2% and identifies 598,000 H-1B holders (L305–307, fn. 6).
- **No reweighting / no undercount correction**: "our methodology does _not_ perform any
  reweighting" (L353), unlike the CMS/Warren approach; DHS assumes a 10% undercount (fn. 2).
- Validation is indirect: age profile matches Pew (Fig. 1), summary statistics match Pew (Table 1),
  and the 2010 state distribution matches CMS/Warren/DHS/Pew (Table 2). Total for 2010:
  Borjas–Cassidy 12,256 thousand vs CMS 11,725, DHS 11,570, Pew 11,400 (Table 2, L415).

## Design and identification

- **Main estimate:** pooled Mincerian OLS on working immigrants only (legal + undocumented, natives
  excluded), `log w_i = βh_i + β_L L_i + ε_i`, with `β_L` the wage penalty (Eq. 1, L369–376).
  Controls: age fixed effects in 5-year bands, 51 state fixed effects, years-since-migration as a
  fourth-order polynomial, education fixed effects (<12, 12, 13–15, 16, >16 years), country-of-birth
  fixed effects, and (ACS only) English-proficiency fixed effects (fn. 13, L473–481).
  This is **selection on observables**, not a causal design. The authors note the pooled-β regression
  is numerically identical to an Oaxaca–Blinder decomposition with pooled reference coefficients
  (fn. 11).
- **Covariate attribution:** Gelbach (2016) decomposition (Stata `b1x2`), order-independent.
- **DACA:** difference-in-differences in event-study form on 2010–2016 ACS, legal-status dummy
  interacted with year, in the sample meeting DACA demographic criteria (arrived before age 16,
  ≤31 in 2012, ≥high school), with a placebo sample that misses only the arrival-age rule (Table 4).
- **State second stage:** state-year wage penalties from Eq. (4) regressed on undocumented share,
  E-Verify mandate, and state unemployment rate; 459 state-year cells, state and year fixed effects,
  weighted by (n_L × n_U)/(n_L + n_U), SEs clustered by state.
- **Instrument:** shift-share, 1995–2000 pooled CPS country-of-origin settlement shares × national
  ACS counts by origin. **First stage coefficient 0.916 (SE 0.188)** (L1313–1315). No F-statistic
  reported. The authors cite Jaeger, Ruist and Stuhler (2018) as a critical appraisal of the design.

## Headline estimates

All wage-penalty numbers are log points on legal status; positive = legal immigrants earn more than
observationally equivalent undocumented immigrants.

| Outcome | Estimate | SE | Table/figure and anchor | Verbatim quote (≤40 words) |
|---|---|---|---|---|
| Raw log wage gap, legal vs undocumented, men, ACS 2012–13 | 0.413 | 0.003 | Table 3, "Difference", L544–545 | "the raw wage gap is approximately 39.8% in the Pew CPS and 41.3% in the ACS" |
| Raw gap, men, Pew CPS 2012–13 | 0.398 | 0.009 | Table 3, L544–545 | "the raw wage gap is approximately 39.8% in the Pew CPS and 41.3% in the ACS" |
| Raw gap, women, ACS 2012–13 | 0.385 | 0.004 | Table 3, L544–545 | "Difference 0.398 0.413 0.413 0.358 0.385 0.385" |
| Raw gap, women, Pew CPS 2012–13 | 0.358 | 0.011 | Table 3, L544–545 | "Difference 0.398 0.413 0.413 0.358 0.385 0.385" |
| Adjusted penalty, men, ACS, no English control | 0.086 | 0.003 | Table 3 col (1), L548–549 | "an estimated wage penalty of 6.0% in the Pew CPS and of 8.6% in the ACS" |
| Adjusted penalty, men, Pew CPS | 0.060 | 0.009 | Table 3, L548–549 | "an estimated wage penalty of 6.0% in the Pew CPS and of 8.6% in the ACS" |
| **Adjusted penalty, men, ACS, full model with English** | **0.061** | 0.003 | Table 3 col (2), L548–549 | "adding English language proficiency fixed effects to the regression model further reduces the wage penalty in the ACS, from 8.6 to 6.1% for men and from 6.3 to 4.2% for women" |
| **Adjusted penalty, women, ACS, full model with English** | **0.042** | 0.004 | Table 3 col (2), L548–549 | "from 8.6 to 6.1% for men and from 6.3 to 4.2% for women" |
| Adjusted penalty, women, ACS, no English | 0.063 | 0.004 | Table 3 col (1), L548 | "Unexplained 0.060 0.086 0.061 0.046 0.063 0.042" |
| Adjusted penalty, women, Pew CPS | 0.046 | 0.011 | Table 3, L548 | "Unexplained 0.060 0.086 0.061 0.046 0.063 0.042" |
| Adjusted penalty with occupation controls added, men | 0.027 | n/r | fn. 16, L603–606 | "Adding occupation controls to the decomposition further lowers the wage penalty to 2.7% for men and to near zero for women in the ACS" |
| Gap explained by education alone, men | 0.144 | 0.002 | Table 3, "Education" col (2), L557–558 | "differences in educational attainment alone generate a 14.4% wage gap, about a third of what is actually observed" |
| Gap explained by YSM + education + English, men | 0.272 | n/r | Sec. 3, L591–592 | "these three sets of variables together generate a 27.2% wage gap, about two-thirds of what is actually observed" |
| Gap explained by English alone, men | 0.071 | 0.001 | Table 3, "English", L561–563 | "English - - 0.071 - - 0.067" |
| Gap explained by YSM, men | 0.057 | 0.002 | Table 3, "YSM" col (2), L555–556 | "YSM 0.053 0.080 0.057 0.061 0.090 0.066" |
| Gap explained by age, men | 0.035 | 0.001 | Table 3, "Age" col (2), L551–552 | "leads to a 3.5 percentage point wage gap for men, while the covariate group \"state of residence\" generates only a 0.4 percentage point wage gap" |
| Gap explained by state of residence, men | 0.004 | 0.001 | Table 3, L553–554 | "generates only a 0.4 percentage point wage gap" |
| Gap explained by occupation, men / women | 0.153 / 0.177 | n/r | fn. 16, L604–606 | "occupation explains 15.3 and 17.7 percentage points of the wage gap between legal and undocumented immigrants for men and women, respectively" |
| Penalty, all men, 2013 | 0.067 | 0.006 | Fig. 2 top, L615–618 | "In 2013, for example, the wage penalty for the average male worker was 6.7 percentage points (with a standard error of 0.6)" |
| **Penalty, all men, 2016** | **0.041** | 0.006 | Fig. 2 top, L617–618 | "it declined to 4.1 percentage points by 2016 (with a standard error of 0.6)" |
| Penalty, low-skill men, 2013 → 2016 | 0.083 → 0.066 | ~0.006 | Fig. 2 top, L621–623 | "The wage penalty for low-skill workers stood at 8.3% in 2013, before beginning its decline and ending up at 6.6% in 2016." |
| Penalty, high-skill men, 2013 → 2016 | 0.061 → 0.027 | ~0.006 | Fig. 2 top, L623–624 | "the wage penalty for high-skill workers was 6.1% 2013, but by 2016 had declined to 2.7%" |
| Penalty, women, 2010 → 2016 | >0.05 → ~0.02 | ~0.008 | Fig. 2 bottom, L657–658 | "In 2010, the wage penalty for women stood at over 5%. By 2016, it had fallen to about 2%." |
| Summary of the whole trend | ~6% men / 4% women pre-2013 → 2–4% by 2016 | n/r | Sec. 6, L~1470 | "hovered around 6% until about 2013 for men and 4% for women, at which point it began a noticeable decline. Between 2013 and 2016, the wage penalty ... had shrunk to about only 2–4%" |
| Penalty, newly arrived (≤3 yrs), 2011 → 2016 | 0.107 → 0.050 | 0.015 (2016) | Fig. 3, L728–729 | "The wage penalty to new immigrants fell from 10.7% in 2011 to 5.0% (with a standard error of 1.5) by 2016." |
| Penalty, immigrants >10 years in US, 2013 → 2016 | ~0.06 → ~0.04 | n/r | Fig. 3, L731–733 | "with the wage penalty declining by only about 2 percentage points (from about 6% in 2013 to 4% in 2016)" |
| DACA-eligible baseline penalty, 2012–13 | 0.064 | 0.008 | Table 4 col (1), L810–811 | "the wage penalty in the demographic sample potentially affected by DACA stood at 6.4% during this baseline period" |
| DACA-eligible, 2016 interaction (decline) | −0.038 | 0.012 | Table 4 col (1), L819–820 | "2016 −0.038 −0.045 −0.045 0.028" |
| DACA-eligible incl. enrolled, 2016 decline | −0.045 | 0.011 | Table 4 col (2), L819–820 | "the measured decline in the wage penalty in the post-DACA period is slightly larger, about 4.5 percentage points" |
| DACA-eligible, exactly 12 yrs schooling, baseline / 2016 decline | 0.068 / −0.045 | 0.011 / 0.017 | Table 4 col (3), L810–820 | "the wage penalty in the baseline period 2012–2013 was 6.8% and had declined by 4.5 percentage points by 2016" |
| Placebo: not DACA-eligible, age<31 in 2012, 2016 interaction | +0.028 | 0.017 | Table 4 col (4), L819–820 | "the wage penalty in this comparable, but non-eligible, sample did not decline over time. If anything, the wage penalty was _rising_ somewhat over the life cycle" |
| Undoc–native raw log gap at age 25 / age 45, men | 0.24 / 0.47 | n/r | Fig. 4, L916–920 | "the hourly wage of undocumented men in the ACS is 0.24 log points below that of natives and 0.27 log points below that of legal immigrants. By age 45, the wage gap ... rose to 0.47 log points" |
| Undoc–legal raw log gap at age 25 / age 45, men | 0.27 / 0.37 | n/r | Fig. 4, L916–920 | "the wage gap between legal and undocumented immigrants rose to 0.37 log points" |
| Life-cycle growth in penalty to age 35, men, baseline | +19.4 pp (−12.9% → +6.5%) | n/r | Fig. 6, L1063–1067 | "the baseline wage penalty for men grows by 19.4 percentage points" |
| Life-cycle growth to age 35 with occupation FE, men | +15.5 pp (−12.4% → +3.1%) | n/r | Fig. 6, L1066–1067 | "the wage penalty that adjusts for the widening gap in occupational attainment grows by only 15.5 percentage points" |
| Effect of +1 pp undocumented share on penalty, men, OLS | 0.009 | 0.003 | Table 6 col (1), L1234–1236 | "An increase of 1 percentage point in the undocumented share raises the wages penalty by about 0.9 percentage points." |
| Same, men, IV | 0.009 | 0.003 | Table 6 IV col (1), L1243–1245 | "A one percentage point increase in the undocumented share again increases the size of the wage penalty by about 0.9 percentage points." |
| Undocumented share coefficient, low-skill / high-skill men, OLS | 0.012 / 0.017 | 0.005 / 0.006 | Table 6 cols (3),(4), L1234–1236 | "Undocumented share 0.009 0.011 0.012 0.017 0.015" |
| Undocumented share coefficient, women, OLS / IV | 0.015 / −0.002 | 0.004 / 0.011 | Table 6 col (5), L1234–1245 | "Undocumented share 0.009 0.011 0.013 0.019 −0.002" |
| E-Verify mandate effect on penalty, men | +0.045 (OLS and IV) | 0.014 / 0.013 | Table 6, L1237–1247 | "legislation mandating the use of E-Verify had a significant positive impact on the wage penalty to undocumented immigration, raising the wage penalty by 4.5 percentage points (in both the OLS and IV regressions)" |
| State unemployment rate effect | −0.003 | 0.005 | Table 6, L1239–1240 | "the impact of the local unemployment rate on the wage penalty is near zero, both statistically and numerically" |
| First-stage coefficient, shift-share instrument | 0.916 | 0.188 | Sec. 5, L1313–1315 | "The relevant coefficient of the first stage is 0.916, with a standard error of 0.188." |
| Inverse-elasticity regression coefficient, men | −0.059 | n/r | Eq. (5), L1273–1281 | "elasticity of substitution between the two groups is 17.0. For women," |
| Elasticity of substitution legal vs undocumented, men | 17.0 | n/r | Eq. (5), L1271 | "elasticity of substitution between the two groups is 17.0. For women," |
| Elasticity of substitution legal vs undocumented, women | 11.5 | coef SE 0.029 | Sec. 5, L1281–1284 | "the coefficient on the log ratio of legal to undocumented immigrants" + "elasticity of 11.5" |
| Employment rate, legal vs undocumented men, 2012–13 CPS | 84.7% vs 88.1% | n/r | Sec. 5, L1396–1398 | "the employment rate in the 2012–2013 CPS is 84.7% for legal immigrant men and 88.1% for undocumented men" |
| Employment rate, legal vs undocumented women | 64.4% vs 56.7% | n/r | Sec. 5, L1398–1399 | "the employment rate is 64.4% for legal immigrant women and only 56.7% for undocumented women" |
| Undocumented men with ≥college, before/after H-1B filter | 17.8% → 14.2% | n/r | Sec. 2, L305–307 | "the application of the H-1B filter reduces the fraction of undocumented immigrant men with at least a college degree from 17.8 to 14.2%" |
| Pew algorithm misclassification of college-educated | ~25% | n/r | Sec. 2, L294–296 | "mistakenly classified around 25% of college educated immigrants as undocumented" |
| Undocumented population total, 2010, authors' imputation | 12,256,000 | n/r | Table 2, L415 | "US Total (thousands) 12,256 11,725 11,725 11,570 11,400" |
| Undocumented share of male workforce, ACS 2012–13 | 6.9% | n/r | Table 1 panel B, L243 | "fraction of the population that is undocumented is 6.5%" |
| Undocumented men who are HS dropouts, ACS | 44.5% (H1B-corrected) | n/r | Table 1 panel B, L246 | "High school dropouts 5.6 19.2 19.0 42.6 44.5" |

## Trend over time, stated compactly

Men: flat at 5–6% through 2013, then a statistically significant fall to 4.1% in 2016. The fall is
steeper for high-skill (6.1 → 2.7%) than low-skill (8.3 → 6.6%). Women: decline starts earlier,
around 2010, from over 5% to about 2% by 2016. Recent arrivals drive much of it (10.7% in 2011 to
5.0% in 2016) while the >10-year stock barely moves (6% to 4%). The authors' robustness check with
composition held fixed at pooled 2008–2016 shares "also reveals a decline of 3–+5 percentage points
in the wage penalty starting around 2012 or 2013" (fn. 19).

## Authors' interpretation of why the adjusted penalty is small

1. **Composition, not differential treatment.** The raw gap is mostly education, years since
   migration, English proficiency, and birthplace. "Two variables, educational attainment and
   English language proficiency, account for nearly half of the observed wage gap between the
   groups" (intro finding 1). Adding occupation drops the residual to 2.7% for men and near zero for
   women, i.e. the remaining penalty largely reflects which jobs the undocumented hold.
2. **External corroboration.** The IRCA-amnesty literature (Kossoudji & Cobb-Clark 2002; Kaushal
   2006) found legalized workers' "wage rose by at most 6% between 1989 and 1992", which the authors
   say "closely resemble the penalty implied by the wage data in the early years of our ACS
   cross-sections." Rivera-Batiz (1999) on undocumented Mexicans reached the same covariate ranking.
3. **The legal environment relaxed.** The post-2013 decline "coincides with the timing of actions by
   the Obama administration which led to a less restrictive approach to undocumented immigration",
   and the DACA event study shows the eligible group's penalty falling 4–5 pp while a matched
   non-eligible group's did not.
4. **The small average hides large dispersion.** The authors explicitly resist the reading that the
   penalty is unimportant: it is negative for workers in their 20s, rises ~19 pp by age 35, is
   larger in high-undocumented-share states, and rises 4.5 pp under E-Verify.
5. **Honest non-identification of the national trend.** "It is difficult to identify precisely which
   factor drove the decline in the wage penalty in the national labor market after 2013", because
   composition of the undocumented population changed in unknown ways (fn. 21).

## What it says about

- **Native wages by skill/education** — not studied. Natives appear only as a descriptive benchmark
  in Table 1 and the Fig. 4 age-earnings profiles. No native-wage-impact regression anywhere.
- **Native employment / crowd-out** — not studied. The only employment numbers are legal vs
  undocumented immigrant employment rates quoted from Borjas (2017).
- **Housing prices, rents** — not studied. Public housing and rental subsidies appear only as
  imputation rule (f), which is dropped for the ACS.
- **Fiscal: taxes, transfers, public services, schooling** — not studied as outcomes. Benefit receipt
  (Social Security, SSI, Medicaid, Medicare, Military Insurance, public housing) is used only as a
  *classifier* for legal status, which mechanically means the imputed undocumented population
  receives none of those programs by construction. Schooling appears only as a control and as a
  sample restriction (not enrolled), plus the note that DACA "encourages further education".
- **Firms, production, investment, profits** — essentially not studied. The only production content
  is the nested-CES reading of the state-level relative-wage regression (elasticity 17.0 men / 11.5
  women) and the claim that employer exploitation is possible because of deportation risk.
- **Mechanism the authors claim** — (i) observable human capital, above all education, English and
  time in the US, explains most of the raw gap; (ii) blocked **occupational mobility** (licensing,
  legal barriers) generates the flat age-earnings profile and the life-cycle rise in the penalty —
  cognitive task requirements rise more slowly and then fall for the undocumented while non-cognitive
  requirements stay high; (iii) the **legal environment** shifts the penalty (DACA down, E-Verify up);
  (iv) **imperfect substitution** between legal and undocumented workers makes the penalty rise with
  the relative supply of the undocumented.

## Elasticities or parameters a model could transport

1. **Elasticity of substitution between legal and undocumented immigrant workers, within a state
   labour market, nested CES** — **17.0 for men**, **11.5 for women**. Estimated as the reciprocal of
   the coefficient from regressing the state-year wage penalty on the log legal/undocumented quantity
   ratio with state and year fixed effects (men coefficient 0.059; women 0.087, SE 0.029). Population:
   ACS 2008–2016 foreign-born workers aged 21–64, 459 state-year cells. Note this is a *very high*
   elasticity, i.e. near-substitutes, and its point is only that perfect substitution is rejected.
   It is a legal-status nest, not the native-vs-foreign-born nest the parent's production term uses,
   so it is not a drop-in value for ε there; if anything it bounds how finely one can split the
   foreign-born aggregate.
2. **Semi-elasticity of the legal/undocumented wage gap to undocumented share of the state
   workforce** — +0.009 log points per percentage point (OLS and IV alike for men); +0.012 low-skill
   men, +0.017–0.019 high-skill men; unstable and near zero for women under IV. Population as above.
3. **E-Verify mandate effect on the legal/undocumented wage gap** — +4.5 pp (SE 0.014 OLS / 0.013 IV),
   identified off four states: Arizona 2008, South Carolina 2010, Mississippi 2011, Alabama 2012.
4. **DACA effect on the wage penalty of eligible workers** — a fall of 3.8–4.5 pp by 2016 relative to
   2012–13, with a null in the matched non-eligible sample.
5. **Composition shares of the raw gap (Gelbach)** — education 0.144, English 0.071, YSM 0.057,
   birthplace 0.042, age 0.035, state 0.004, occupation 0.153, out of a 0.413 total for men. Useful
   as a decomposition benchmark if the parent ever attributes an immigrant wage gap to status vs
   human capital.
6. **Level facts usable as inputs** — undocumented = 6.9% of the male ACS workforce and 3.8% of the
   female; 44.5% of undocumented men are high-school dropouts vs 5.6% of natives; ~14% of
   undocumented men have at least a college degree even after the H-1B filter; 12.26M undocumented in
   2010.

## Authors' stated limitations and external-validity notes

- **Everything hinges on the imputation.** "the robustness of the evidence presented below depends on
  the validity of the procedure used to impute undocumented status at the micro level" and "In the
  absence of administrative data on the characteristics of the undocumented population, it is not
  possible to quantify the direction and magnitude of any potential bias."
- **High-education misclassification** survives even after the H-1B filter ("both the original Pew
  files and our imputation in the ACS still produce a relatively large number of undocumented
  workers with high levels of educational attainment").
- **Female selection.** Nearly half of undocumented women do not work; "The selection biases in wage
  regressions are likely to be substantial when nearly half the sample self-selects out of the
  workforce." All female results should be read as selection-contaminated.
- **Cross-section age profiles ≠ life cycle.** Assimilation, cohort quality (Borjas 1985), and
  status-switching ("some of the undocumented will be able to 'filter themselves' out and obtain
  green cards as they age") all contaminate the Fig. 4/Fig. 6 profiles.
- **E-Verify not generalizable.** "our evidence exploits the enactment of the E-Verify system in only
  a very small number of states, so that it would not be prudent to generalize from this exercise to
  a prediction of what would happen to the wage penalty if the system were adopted nationwide."
- **Instrument timing is weak by design.** "Ideally, the instrument would employ the geographic
  settlement of legal and undocumented immigrants many years prior to the sample period of
  2008–2016", but no micro survey before the 1994 CPS supports the imputation; Jaeger–Ruist–Stuhler
  (2018) is cited as a critical appraisal of shift-share designs.
- **Geography is coarse.** State, not metro or commuting zone, "because the sample size of
  undocumented immigrants would fall substantially in many of these smaller geographic units."
- **National trend unexplained.** Composition change over 2008–2016 cannot be measured with their
  data (fn. 21).
- **Scope claim.** "the analysis reported in this paper represents a first step in any evaluation of
  the proposals being discussed to regularize the status of undocumented workers."

## Data availability

No replication package, code repository, or data-availability statement appears in the parsed text.
Inputs are public: ACS microdata via IPUMS (Ruggles et al. 2018), O*NET version 17.0, BLS state
unemployment rates, NCSL/NumbersUSA E-Verify dates. The **Pew CPS-ASEC legal-status files are
restricted** — obtained by special arrangement: "After being granted access to some of the Pew data
files, Borjas (2017) used a variant of this algorithm", with thanks "to Mark Lopez and Jeffrey Passel
of the Pew Research Center for their generosity in sharing data files." The ACS imputation is the
authors' own reconstruction and is not distributed here. Decomposition uses the Stata package `b1x2`.

## Verification

Every numeric row in the headline table was re-checked with `rg -F` against the paper file.
46 fragments were run in the first pass: 32 matched immediately and 14 failed only because the
parsed markdown is hard-wrapped and `rg` matches line by line. Those 14 were re-run as line-safe
sub-fragments and all matched, so **46 of 46 quote fragments are confirmed present in the source**
and no row was dropped. Quotes in the table that span a line break in the parsed file are still
verbatim; the two rows where a single-line fragment was needed (the elasticity row and the
undocumented-share row) now carry the shortened, line-contiguous fragment.
