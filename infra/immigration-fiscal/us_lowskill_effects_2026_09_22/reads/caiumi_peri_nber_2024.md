<!-- reader extraction, opus-low agent, 2026-09-22; every numeric row carries a verbatim quote re-found in the parsed corpus text with rg -F; parent spot-checked the rows cited in the memo -->
# Caiumi & Peri (2024), "Immigration's Effect on US Wages and Employment Redux", NBER WP 32389

[SOURCE: /Users/alien/Projects/corpus/doi_10_3386_w32389/parsed.pymupdf4llm@0.3.4+cfg-99914b93/page.md]
[UNVERIFIED] — extraction from the parsed NBER working-paper text only; no replication, no cross-check against the published version.

**Verdict:** A national skill-cell ("factor-supply") nested-CES study that estimates native–immigrant and cross-skill substitution elasticities on US Census/ACS 1960–2022 with a new skill-cell shift-share IV plus a demographic-projection IV, then *simulates* (not estimates) native wage and employment effects; identification of the elasticities is moderately credible (F ≈ 13–36 post-2000, passes a pre-trend placebo), but the headline "+1.7 to +2.6% for less-educated natives" is a model calibration, not a measured wage effect, and rests on parameters partly imported from other papers.

## Population, period, unit

- Unit of observation: 32 national **education × experience cells** (4 education groups × 8 five-year potential-experience bins), by year. Not geographic.
  > "for each year in our data we build 32 cells identified by different combi-" … "nations of education and experience, as in Ottaviano and Peri (2012)"
- Education groups: no high school degree, high school graduate, some college, college degree or more. Experience: 0–5 … 35–40 years of potential experience, entry age 17/19/21/23 by education.
- Years: 1960, 1970, 1980, 1990, 2000, 2005, 2010, 2015, 2019, 2022. Panels run 1960–2019, 1980–2019, or 2000–2019; simulations for 2000–2019 and 2019–2022.
- Sample: aged 18+, not in group quarters, worked ≥1 week last year; wage sample drops invalid income and self-employed; a full-time subset is ≥40 weeks and ≥35 usual hours.
- Foreign-born = noncitizens plus naturalized citizens.
  > "and foreign-born females. The status of foreign-born is given to those individuals who are" … "noncitizens or are naturalized citizens."
- Wage variable: real weekly wage (INCWAGE / weeks, 1999 dollars, top-code adjusted), cell average weighted by hours × person weight.
- Data: IPUMS USA v14.0, Decennial Census 1960–2000 + ACS 2005/2010/2015/2019/2022, downloaded 2024-01-12.

## Design and identification

Structural nested CES (equations 1–6): capital and a labor aggregate; labor nests (i) high vs low schooling (σ_HL), (ii) within-high some-college vs college (σ_HH) and within-low no-degree vs high-school (σ_LL), (iii) eight experience groups within each education group (σ_EXP), (iv) **natives vs foreign-born within each education × experience cell (σ_IMMI)**. Wage equations come from equating marginal product to wage; the key regression is log(native wage / immigrant wage) on log(immigrant employment / native employment) with cell and year fixed effects, whose coefficient is 1/σ_IMMI.

Instruments (Section 4):
1. **Skill-cell shift-share for immigrant supply.** Shares = each origin's 1960→1980 net immigration distribution across the 32 skill cells; shifts = that origin's aggregate net flow per decade 1980–2019. 12 origins: Mexico, Cuba, China, Philippines, Korea plus 7 continents. Negative cell net flows set to zero so shares are non-negative and sum to one.
2. **Demographic projection for native supply.** Native population in cell (k, j) predicted from the previous decade's (or 5-year period's) population in (k, j−10) (or j−5), education structure held fixed; the two youngest experience groups are imputed from the prior period's youngest-cohort education shares. Called the "best one decade-ahead prediction".

The relative-wage regression instruments the log ratio with the ratio of the two imputed populations; the employment regression instruments log immigrant employment with the shift-share imputed immigrant population alone.

First-stage strength (effective/robust F, clustered at cell level):

| Panel | Period | F |
|---|---|---|
| Relative employment (Table 5 A) | 1980–2019 | 71.58 / 75.80 / 92.05 / 96.08 |
| Immigrant employment (Table 5 B) | 1980–2019 | 16.19 / 18.48 / 15.86 / 18.38 |
| Relative employment (Table 6 A) | 2000–2019 | 22.42 / 13.37 / 31.62 / 17.25 |
| Immigrant employment (Table 6 B) | 2000–2019 | 36.14 / 75.37 / 30.21 / 58.49 |

> "F statistics reported in the tables surpass the critical value of 23.1 for 2SLS with a worst-case" [bias of 10%]

The authors flag Table 5 Panel B as the weak case: "Table 5, which should therefore be taken with a bit of caution."

Validity: placebo of 2000–2019 IV-imputed population changes on stacked 1980–90 and 1990–2000 *pre-period* outcome changes (Table 4, N = 64 cells). Eight coefficients; none significant at 5%, one (0.038, s.e. 0.019) at 10%.
> "The estimates, some of which were visualized in Figure" … "6, are never significant at the 5% confidence level, and only one coefficient out of eight is"

Controls throughout: cell (education × experience) fixed effects and year fixed effects; some specifications use all two-way (education × year, experience × year, education × experience) fixed effects. Weights = cell employment. Standard errors clustered at the education × experience cell.

## Headline estimates

All "estimate" entries are 1/σ unless stated. SEs in the SE column.

| Outcome | Estimate | SE | Table / page | Verbatim quote (≤40 words) |
|---|---|---|---|---|
| 1/σ_IMMI, OLS, pooled hours, cell+year FE, 1960–2019 | 0.044 | 0.013 | Table 1 Panel A row 3 col (2), p. 19 | "Pooled, Hours 0.023** 0.044*** 0.035** 0.058* 0.028*** 0.057*** 0.048*** 0.023" |
| 1/σ_IMMI, OLS, pooled hours, cell+year FE, 2000–2019 | 0.068 | 0.018 | Table 1 Panel B row 3 col (2), p. 19 | "Pooled, Hours 0.033** 0.068*** 0.061*** 0.073* 0.041*** 0.073*** 0.063*** 0.076*" |
| 1/σ_IMMI, OLS men, population-IV for hours, 2000–2019, all two-way FE | 0.085 | 0.032 | Table 1 Panel B row 6 col (4), p. 19 | "Men, Hours (IV) 0.022 0.065*** 0.064*** 0.085*** 0.029** 0.067*** 0.065*** 0.083***" |
| **1/σ_IMMI, 2SLS pooled, new shift-share + demographic IV, 2000–2019, weighted, all workers** | **0.058** | **0.025** | **Table 6 Panel A row 3 col (1), p. 38** | "Pooled, Rel. employment (SS IV + demogr. IV) 0.058** 0.050** 0.059** 0.049**" |
| 1/σ_IMMI, 2SLS men, same IV, 2000–2019 | 0.035 (n.s.) | 0.027 | Table 6 Panel A row 1, p. 38 | "Men, Rel. employment (SS IV + demogr. IV) 0.035 0.026 0.041 0.029" |
| 1/σ_IMMI, 2SLS women, same IV, 2000–2019 | 0.073 | 0.028 | Table 6 Panel A row 2, p. 38 | "Women, Rel. employment (SS IV + demogr. IV) 0.073** 0.063** 0.068** 0.058**" |
| 1/σ_IMMI, 2SLS pooled, 1980–2019 | 0.018 (n.s.) | 0.020 | Table 5 Panel A row 3, p. 37 | "Pooled, Rel. employment (SS IV + demogr. IV) 0.018 0.020 0.030* 0.030**" |
| 1/σ_IMMI by education, 2SLS, pooled, 2000–2019, **no HS diploma** | 0.115 | 0.031 | Table 7 Panel A row 1 col (1), p. 39 | "Pooled, Rel. employment - No HS diploma 0.115*** 0.101*** 0.025 0.052**" |
| … **HS diploma** | 0.017 | 0.006 | Table 7 Panel A row 2, p. 39 | "Pooled, Rel. employment - HS diploma 0.017*** 0.015*** 0.018*** 0.018***" |
| … **some college** | 0.041 | 0.005 | Table 7 Panel A row 3, p. 39 | "Pooled, Rel. employment - Some college 0.041*** 0.040*** 0.044*** 0.046***" |
| … **college degree** | 0.104 | 0.008 | Table 7 Panel A row 4, p. 39 | "Pooled, Rel. employment - College degree 0.104*** 0.098*** 0.112*** 0.107***" |
| 1/σ_IMMI by education (men, population IV), 2000–2019, no HS | 0.126 | 0.037 | Table 2 Panel B row 1, p. 22 | "Men, Rel. hours (IV) - No HS diploma 0.126*** 0.119*** 0.040 0.072***" |
| … men, college degree | 0.096 | 0.008 | Table 2 Panel B row 4, p. 22 | "Men, Rel. hours (IV) - College degree 0.096*** 0.094*** 0.106*** 0.107***" |
| β_emp: native emp/pop ratio per log immigrant employment, 2SLS pooled, 2000–2019 | 0.075 | 0.013 | Table 6 Panel B row 3 col (1), p. 38 | "Pooled, Imm. employment (SS IV) 0.075*** 0.057*** 0.095*** 0.048***" |
| β_emp, 2SLS pooled, 1980–2019 | 0.056 | 0.020 | Table 5 Panel B row 3, p. 37 | "Pooled, Imm. employment (SS IV) 0.056*** 0.040** 0.114*** 0.057**" |
| β_emp, simple population IV, pooled, 2000–2019 | 0.048 | 0.007 | Table 3 Panel B row 3 col (1), p. 25 | "Pooled, Imm. employment (IV) 0.048*** 0.047*** 0.056*** 0.045***" |
| β_emp by education, pooled, 2000–2019, no HS / HS / some college / college | 0.029 (n.s.) / 0.043 / 0.047 / 0.049 | 0.022 / 0.022 / 0.022 / 0.022 | Table 7 Panel B col (1), p. 39 | "Pooled, Imm. employment - No HS diploma 0.029 0.039* 0.132** 0.154***" |
| β_occ: native occupational-quality index per log immigrant employment, pooled, 2000–2019 | 0.020 | 0.005 | Table 8 Panel B row 3 col (1), p. 41 | "Pooled, Imm. employment (SS IV) 0.020*** 0.018*** 0.009 0.010***" |
| β_occ, pooled, 1980–2019 | 0.036 | 0.010 | Table 8 Panel A row 3 col (1), p. 41 | "Pooled, Imm. employment (SS IV) 0.036*** 0.030*** 0.022*** 0.017***" |
| **Simulated native wage effect 2000–2019, no HS degree** | +1.8 to +2.4% | (0.8)–(1.0) | Table 9 row 1 cols (1)–(4), p. 46 | "No High School Degree 1.8 1.8 2.4 1.7 -1.5 -6.1" |
| **… high school degree** | +2.0 to +2.6% | (0.3)–(0.6) | Table 9 row 2, p. 46 | "High School Degree 2.1 2.0 2.6 2.1 2.8 9.0" |
| **… some college** | −0.2 to +0.7% | (0.2)–(0.5) | Table 9 row 3, p. 46 | "Some College Education 0.5 0.7 0.4 -0.2 2.0 6.0" |
| **… college degree** | −0.5 to +0.7% | (0.2)–(0.5) | Table 9 row 4, p. 46 | "College Degree -0.5 0.1 -0.1 0.7 4.2 12.4" |
| **… average native** | +0.5 to +0.8% | (0.3)–(0.5) | Table 9 row 5, p. 46 | "Average 0.5 0.8 0.8 0.8 2.4 7.4" |
| Simulated native emp/pop effect 2000–2019, average | +2.4 p.p. (all workers) / +7.4 p.p. (full-time) | not reported | Table 9 cols (5)–(6), p. 46 | "immigration boosted the employment-population ratio of natives" … "on average by 2.4 percentage points (and as much as 7.4 p.p. when considering full-time" |
| Simulated native wage effect 2019–2022, no HS | +0.7 to +1.1% | (0.3) | Table 10 row 1, p. 47 | "No High School Degree 0.8 0.8 1.1 0.7 -0.1 -0.3" |
| … 2019–2022, high school degree | +0.9 to +1.1% | (0.1)–(0.3) | Table 10 row 2, p. 47 | "High School Degree 0.9 0.9 1.1 0.9 0.0 0.1" |
| … 2019–2022, some college | −0.3 to −0.0% | (0.0)–(0.1) | Table 10 row 3, p. 47 | "Some College Education -0.0 -0.0 -0.1 -0.3 -0.2 -0.6" |
| … 2019–2022, college degree | −0.2 to −0.0% | (0.0)–(0.1) | Table 10 row 4, p. 47 | "College Degree -0.2 -0.1 -0.2 -0.0 0.5 1.4" |
| … 2019–2022, average native | +0.0 to +0.1% | (0.1) | Table 10 row 5, p. 47 | "Average 0.0 0.1 0.1 0.1 0.1 0.4" |
| Simulated **foreign-born** wage effect 2000–2019, college degree | −6.7 to −10.9% | (0.8)–(2.5) | Table 14 row 4, p. iv | "College Degree -6.7 -10.8 -10.9 -10.1" |
| Simulated foreign-born wage effect 2000–2019, average | −3.5 to −5.7% | (0.9)–(1.9) | Table 14 row 5, p. iv | "Average -3.5 -5.7 -5.6 -5.6" |
| Immigrant-driven change in hours worked, 2000–2019, college | +13.0% | n/a | Table 11, p. i | "College Degree 1 to 5 years 6.6 -4.7" … "All Experience Groups 13.0 -0.3" |
| Immigrant-driven change in hours worked, 2000–2019, no HS | −1.7% | n/a | Table 11, p. i | "All Experience Groups -1.7 -5.6" |
| Native real weekly wage change 2000–2019, no HS / HS | −5.6% / −6.9% | n/a | Table 11, p. i | "All Experience Groups 7.2 -6.9" |

Note on the employment columns of Tables 9 and 10: the column header reads "Percentage change in native supply" while the text and abstract call the same numbers percentage points of the employment-population ratio. The paper is internally ambiguous on the unit here.

## What it says about

- **Native wages by skill/education.** Central output. Estimated: relative (native/immigrant) wage response inside a cell, i.e. 1/σ_IMMI. Simulated (not estimated): level wage effects by education. 2000–2019 inflow raises less-educated native wages 1.7–2.6% and leaves college natives at −0.5 to +0.7%, average +0.5 to +0.8%, mostly not significant at simulated SEs.
  > "college- and non-college-educated, the immigrant inflow of 2000-2019 helped the wage" … "growth of less educated natives (those with high school degree or less) by between 1.7%"
  The authors stress the sign flip relative to a naive one-factor model comes from immigrants being college-intensive post-2000 plus native–immigrant imperfect substitution.
- **Native employment / crowd-out.** Directly estimated at the national skill-cell level, and positive. A 10 log-point rise in immigrant employment in a cell raises the native employment-population ratio by about 0.5–0.6 p.p.
  > "shows no evidence that, at the national level, immigration is associated with employment" … "displacement, or crowding out of natives."
  They explicitly contrast this with local-labour-market findings of crowd-out (Dustmann et al. 2017; Amior 2020) and argue the national design internalizes internal migration.
- **Housing prices, rents.** Not studied.
- **Fiscal: taxes, transfers, public services, schooling.** Not studied. No fiscal quantity appears anywhere in the paper.
- **Firms, production, investment, profits.** Not studied empirically. Capital enters only as an assumption (below). Monopsony/profit channels are discussed in the literature review and rejected as the frame for post-2000 US immigration, not tested.
- **Mechanism the authors claim.** Occupational specialization and upgrading of natives. Immigrant inflow in a cell raises natives' 1980-wage-weighted occupational quality index by 0.1–0.3% per 10 log points.
  > "an increase of immi-" … "grants by 10 log points in a skill cell (about 10%) increased the occupational quality (wage)"
  They quantify the share this can explain: "increase of native wage by 0 _._ 01 to 0 _._ 02% for each 1% growth of immigrant share can be fully" [due to occupational shifts].
- **Immigrant wages.** Simulated only, and negative: post-2000 inflows cut foreign-born wages, most for college-educated immigrants (−6.7 to −10.9%). The incidence of the supply shock falls on earlier immigrants.

## Capital adjustment assumption

Capital is **fully and endogenously adjusted in the long run**, so the capital-labor ratio is held at its efficient level and total output becomes linear in the labor composite. This is an assumption, not an estimate, and it is what makes the average wage effect of immigration approximately zero by construction, leaving only relative-skill-scarcity effects.

> "We acknowledge that physical capital is complementary to aggregate labor, and that it" … "adjusts in the long run to keep the capital-labor ratio at the efficient level (by equating"

> "By applying this equilibrium condition for capital, one can rewrite" … "the capital term from the production so that total output is a linear function of the labor" … "composite, multiplied by a modified TFP term."

> "However, relative wages across skill groups depend on relative skill abundance" … "and the skill group substitutability."

Productivity effects of immigration are excluded by assumption as well:
> "One important limitation of this" … "approach is that we omit potential effects of immigration on productivity in the analysis,"

## Elasticities or parameters a model could transport

**The one the parent asked for, precisely:** elasticity of substitution between **natives and foreign-born workers within a national education × experience cell** (32 cells; 4 education × 8 potential-experience groups), US workers aged 18+, wage measured as real weekly wage.

| Object | 1/σ | σ | Population / period / method |
|---|---|---|---|
| σ_IMMI, preferred post-2000 estimate | 0.058 (0.025) | **≈ 17.2** | Pooled men+women, all workers, weighted, 2000–2019, shift-share + demographic 2SLS (Table 6 A col 1) |
| σ_IMMI, post-2000 range across the four 2SLS columns | 0.049–0.059 | **≈ 17–20** | Same, 2000–2019 (Table 6 A row 3) |
| σ_IMMI, OLS post-2000 | 0.061–0.088 | ≈ 11–16 | 2000–2019 OLS/population-IV (Table 1 B) — authors summarise "between 12.5 and 16.6 in most cases" |
| σ_IMMI, 1960–2019 long panel OLS | ≈ 0.05 | ≈ 20 | Matches Ottaviano–Peri (2012)'s preferred value |
| σ_IMMI, 1980–2019 2SLS pooled | 0.018–0.030 | ≈ 33–56, often insignificant | Weaker complementarity in the low-skill-inflow era (Table 5 A) |
| σ_IMMI, **no high school diploma** | 0.101–0.115 (all workers) | **≈ 8.7–9.9** | Pooled, 2000–2019, Table 7 A cols (1)–(2); drops to 0.025–0.052 for full-time only |
| σ_IMMI, **high school diploma** | 0.015–0.018 | **≈ 56–67** | Pooled, 2000–2019, Table 7 A |
| σ_IMMI, **some college** | 0.040–0.046 | **≈ 22–25** | Pooled, 2000–2019, Table 7 A |
| σ_IMMI, **college degree or more** | 0.098–0.112 | **≈ 8.9–10.2** | Pooled, 2000–2019, Table 7 A |
| **Simulation values actually used:** 1/σ_N,L (HS degree or less) | 0.045 (0.018) | ≈ 22 | "the average of our estimated coefficients in Table 7" |
| **Simulation values actually used:** 1/σ_N,H (some college or more) | 0.10 (0.008) | ≈ 10 | "the average value for the estimates in the last row of Table 7" |

> "we estimate an elasticity of substitution be-" … "tween immigrants and natives post-2000 around 17-20 in our preferred specification which"

> "In the post-2000 period, native-" … "immigrant elasticity of substitution had a value as low as 9-10 for the two groups at the" … "extremes of the education range, while it was as large as 40-50 for the intermediate ones."

**Parameters imported from the literature, not estimated here** (used in the simulations; the paper's own contribution is only σ_IMMI and β_emp):

| Parameter | Value used | Source |
|---|---|---|
| 1/σ_HL (college-or-more vs HS-or-less) | 0.54 (0.06), alternative 0.71 (0.15) | Ottaviano–Peri (2012); 0.71 is "the exact estimate from Katz and Murphy (1992)" |
| 1/σ_EDU,H (some college vs college degree) | 0.16 (0.08), alternative 0 | Ottaviano–Peri (2012) |
| 1/σ_EDU,L (no degree vs HS degree) | 0.03 (0.02), alternative 0 | Ottaviano–Peri (2012) |
| 1/σ_EXP (across 8 experience groups, within education) | 0.16 (0.05) | Card–Lemieux (2001) / Ottaviano–Peri (2012) |

> "we set" … "1 _/σH_ - _L_ = 0.54, 1 _/σEDU,H_ = 0.16, _σEDU,L_ = 0.03, and 1 _/σEXP_ = 0.16."

> "In column (3) we increase the complementarity between broad education groups and set"

Caution for transport: **σ_EDU,H, σ_EDU,L, σ_EXP and σ_HL are not identified in this paper.** Only σ_IMMI (and β_emp, β_occ) are estimated. A model reusing this paper's four-elasticity set is reusing Ottaviano–Peri (2012) and Katz–Murphy (1992) for three of the four nests.

Also transportable: β_emp ≈ 0.048–0.095 (native employment-population ratio, in ratio points, per unit log immigrant employment in the same skill cell, 2000–2019 pooled) and β_occ ≈ 0.010–0.020 (log native occupational-quality index per log immigrant employment, 2000–2019 pooled).

## Authors' stated limitations and external-validity notes

- **Productivity effects excluded by assumption**, conceded as important especially for high-skilled immigration: "we omit potential effects of immigration on productivity in the analysis, which could be an important consequence, especially in presence of high skilled immigra-"
- **Aggregate, not individual, outcomes.** Individual displacement is compatible with the positive average: "Some individuals may be dis-" … "placed from work or experience reduced wages due to the competition of immigrants."
- **Employment simulations are cruder than the wage simulations** — a partial effect only, with no cross-cell complementarity: "the calculated effects on the employment-population ratio of" … "natives are much more basic than those for wages. They only account for the direct partial"
- **Weak-instrument caution for the 1980–2019 immigrant-employment panel** (Table 5 Panel B), which fails the Olea–Pflueger 23.1 threshold.
- **Multiple endogenous regressors in Table 7** require caution; the Kleibergen-Paap statistic in Panel A is only 3.35–6.65 (Table 18), which the authors do not dwell on although they report it.
- **Occupational mechanism is coarse.** Finer within-occupation task reallocation is untestable in their data: "Our data, however, lack the granularity needed to test this mechanism."
- **Long-run framing.** The whole exercise is a long-run competitive-equilibrium approximation; the estimates are decade-level (or 5-year) and assume wages equal marginal product.
- **NBER working paper, not peer reviewed:** "peer-reviewed or been subject to the review by the NBER Board of Directors that accompanies".

## Data availability

No replication package, code repository, or data-availability statement appears anywhere in the parsed text. The inputs are public and reconstructible: IPUMS USA extracts of Decennial Census 1960–2000 and ACS 2005/2010/2015/2019/2022, cited as "IPUMS USA: Version 14.0 [dataset]," downloaded 2024-01-12 (https://doi.org/10.18128/D010.V14.0). Sample and cell construction are documented well enough to rebuild the cells; the shift-share share matrix would need rebuilding from 1960 and 1980 Census counts by origin (their inputs are shown in Appendix Tables 16 and 17). No restricted data used.

## Verification

Every numeric row in the Headline-estimates table, plus every quoted elasticity/parameter and every limitation quote, was re-found with `rg -F` against the paper path. **59 of 59 checks returned a hit; 0 rows dropped.** Seven quotes initially failed because the parsed PDF breaks them across lines; each was replaced with the exact single-line fragment and re-verified.
