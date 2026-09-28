claude-opus-5-5

**Verdict:** For **sons**, the second-generation Hispanic earnings gap exists at entry and widens through the career;
for **daughters**, it exists at entry and barely widens. Log gap to G3+ non-Hispanic white of the same sex in mean
annual earnings including zero years, NLSY97 round weights:

| | 25–27 | 35–40 | Same people, change (balanced panel, 1997 base weight) |
|---|---|---|---|
| G2 Hispanic men | −0.150 (SE 0.049, n=326) | −0.271 (0.063, n=309) | −0.164 → −0.279: **−0.116 (0.057)**, n=281; IPW −0.113 (0.056) |
| G2 Hispanic women | −0.134 (0.055, n=330) | −0.202 (0.068, n=324) | −0.142 → −0.200: **−0.059 (0.060)**, n=306; IPW −0.060 (0.060) |

[CALCULATION: `analyze.py` → `derived/gaps.csv`, `derived/growth.csv`; SEs from a Rao–Wu bootstrap over the NLSY97
variance PSUs, 300 replicates]

- **Men.** About 55–60% of the midlife gap is present at 25–27. The widening is in hourly pay (−0.064 at 25–27,
  −0.165 at 35–40); lower employment adds −0.05 and −0.07; weeks and hours per week add nothing. Reweighting the white
  reference to G2 Hispanic men's education at 25 leaves −0.072 (0.049) → −0.105 (0.056); adding AFQT leaves −0.047
  (0.050) → −0.041 (0.059). The widening goes with the education and test-score mix: pay differences by schooling grow
  with age. Among men who worked in both windows, the within-person log growth shortfall is −0.050 (0.052), close to
  the published fixed-effects estimate (−0.039 at 43–45). [CALCULATION]
- **Women.** About two-thirds of the midlife gap is present at 25–27, and the change is not distinguishable from
  zero. Reweighted to their education at 25 the gap is +0.041 (0.050) → −0.016 (0.065); with AFQT +0.113 (0.055) →
  +0.093 (0.069). At equal education their hourly pay at 35–40 is **8% above** comparable white women (+0.082, SE
  0.044), offset by lower employment and fewer weeks. [CALCULATION]
- **G3+ Hispanics** (same cohort, not the children of these G2): men −0.197 (0.064) → −0.297 (0.065); women −0.212
  (0.077) → −0.158 (0.094). At 35–40, G3+ men's gap is 1.1 times G2 men's and G3+ women's 0.8 times G2 women's, in
  line with ladder 232's stall after the second generation (≈0.84). Education leaves G3+ men at −0.183 (0.061); it
  closes the women's gap. [CALCULATION]
- **Scope.** Hispanic here means 1997 screener ethnicity. Among Hispanics who answered the 1997–98 ASVAB origin item,
  a Mexican origin was named by 57% of G2 men, 62% of G2 women and 53–55% of G3+ (weighted, any of three mentions),
  not two-thirds. The cohort is 1980–84 births living in the US in 1997; G1 are child arrivals. All results describe
  trajectories; none is causal. [DATA: `derived/person_counts.csv`]

## Method

Earnings are the respondent's wage and salary income plus business or farm income for the calendar year before each
interview (1997–2010 annually, 2012–2022 every second year), including verified zeros (no to both questions), floored
at zero. Weeks and annual hours for the same calendar year come from the event-history created variables
`CVC_WKSWK_YR_ALL` and `CVC_HOURS_WK_YR_ALL`; hourly pay is earnings over hours. Generations come from the verified
parent linkage (`family_analysis_rows.csv`, hash-pinned): G2 = US-born with at least one foreign-born biological
parent; G3+ = US-born with both parents US-born; G1 = born abroad. [SOURCE: archive codebook;
research/immigration-nlsy97-parent-linkage-2026-09-17.md]

The gap decomposition is exact: log gap in mean earnings = log gap in the share with positive earnings + gaps in mean
log weeks, hours per week and hourly pay among workers with 100+ hours and pay of $2–$500 + a bridge term (dispersion
and the worker restriction). Education is the highest degree reported by the round held in the calendar year the
respondent turned 25 (five categories plus unknown); adjustment reweights the white reference to the target group's
cell shares, re-estimated in each replicate. The panel change is a two-period person fixed-effects comparison (person
means in each window, people present in both). Attrition IPW: a logit of being seen at 35–40 on group, education,
birth year and 25–27 earnings and employment, per sex. The 1997 base weight gives −0.151/−0.269 (men) and
−0.135/−0.201 (women) against the round weights' −0.150/−0.271 and −0.134/−0.202. [CALCULATION: `analyze.py`,
`derived/gaps.csv` weight `w0`]

## Attrition

Seen at 35–40: 281 of 326 G2 Hispanic men with entry data, 1,230 of 1,411 G3+ white men, 306 of 330 G2 Hispanic women,
1,192 of 1,324 G3+ white women. G2 Hispanic men who left earned less at 25–27 than those who stayed ($25,700 vs
$28,743) while white men who left earned a little more ($35,004 vs $33,863), so the sons' observed late gap is, if
anything, understated. The IPW arm moves the widening by 0.003. The women's attriter cells (24 and 10) are too small to
read. [DATA: `derived/attrition.csv`, `derived/growth.csv`]

## CPS cross-check (the synthetic-cohort reading)

Same birth cohort, CPS ASEC 2025 (earnings 2024, ages 41–44 at interview, all-origin Hispanic generations built like
the NLSY ones), against NLSY97 income year 2022 (ages 38–42). [CALCULATION: `cps_check.py` → `derived/cps_check.csv`]

| Log gap to G3+ NH white | CPS 2024, ages 41–44 | NLSY97 2022, ages 38–42 |
|---|---|---|
| G2 Hispanic men | −0.133 (0.125, n=165) | −0.312 (0.059, n=234) |
| G3+ Hispanic men | −0.238 (0.108, n=198) | −0.233 (0.089, n=169) |
| G2 Hispanic women | −0.182 (0.087, n=154) | −0.234 (0.073, n=276) |
| G3+ Hispanic women | −0.178 (0.098, n=272) | −0.165 (0.102, n=161) |

Three of four cells agree closely. G2 Hispanic men differ by 0.18, about 1.3 combined standard errors, so this test
cannot separate the panel from the cross-section. The account's own Mexican-origin masks give −0.411 (0.097) for G2
men and −0.185 (0.157) for G3+ men in the same CPS cells: origin mix moves the G2 male figure more than the
panel/cross-section difference does. The repo's ASEC frame is 2025 only, so the brief's 2020–2024 pooling was not
available locally. [DATA]

## The two published companions (read in full, 2026-09-29 01:17 JST)

Neither paper uses NLSY97. Both are Villarreal and Tamborini, linking March CPS/ASEC 1996–2018 respondents (2001
excluded) born 1970–1979 and aged 25+ at interview to SSA Detailed Earnings Records, annual earnings 1980–2019, ages
25–45; random-effects models with seven three-year age bins fully interacted with generation × race; match-adjusted
CPS weights. [SOURCE: Villarreal & Tamborini 2023, *Demography* 60(5):1415–1440, doi:10.1215/00703370-10924116,
PMC11784594, "Sample and Measures", "Modeling Strategy"; Villarreal & Tamborini 2024, *Social Forces* 103(2):655–680,
doi:10.1093/sf/soae078, PMC11784599, "Analytical Sample", "Measurements", "Methods". Full text read from the PMC
AWS open-data XML, men's online appendix PDF from the same bucket.]

| | Men (Demography 2023) | Women (Social Forces 2024) |
|---|---|---|
| Earnings | W-2 wages only; self-employment enters as a dummy | W-2 plus Schedule SE, summed |
| Outcome | log annual earnings, person-years with earnings ≥ $5,000 only (3.7% of person-years dropped); top-coded at p99.5; 2020 $ (CPI-W) | employment = earnings ≥ $5,000 (LPM); log earnings among employed; top-coded p99.5; 2020 $ (CPI-U) |
| G2 | US-born, ≥1 foreign-born parent; Puerto Rico–born are **not** immigrants | US-born, ≥1 parent born outside the 50 states + DC; PR/territory-born **are** immigrants |
| Education | 3 categories, time-invariant (CPS at interview); college/non-college split models | college/non-college split models; time-invariant |
| n, G2 Hispanic | 3,065 matched persons, 51,007 person-years (Table 1; appendix Table A2) | not reported by cell in the main text; total 95,811 matched women |

**Men.** G2 Hispanic vs G3+ white log-earnings gap (Table 2, RE, SE in parentheses): 25–27 −0.116 (0.014); 28–30
−0.129; 31–33 −0.130; 34–36 −0.149; 37–39 −0.153; 40–42 −0.148; 43–45 −0.156 (0.019). The text converts these to
"11.0% lower" at entry and "14.5% less" at 43–45. Within-person (fixed effects, appendix Table A1), the extra
growth shortfall relative to 25–27 is −0.013 (28–30), −0.013, −0.032* (34–36), −0.037* (37–39), −0.030, −0.039
(0.022) at 43–45. So about three-quarters of the midlife gap among men earning ≥ $5,000 is already present at 25–27,
and the widening is about 0.04 log points over 18 years. Controlling for education, the G2 Hispanic gap is significant
from 34–36 on; adding occupation at 25–35 makes every age bin insignificant. [SOURCE: PMC11784594 Table 2, "Multivariate
Results", "Differences by Education", "The Effect of Early Occupational Insertion"; online appendix Table A1.] The
paper describes this as Hispanic men who "begin their careers with an earnings deficit ... and fall further behind".

**Women.** G2 Hispanic minus G3+ white employment probability (Table 3, RE LPM): 25–27 −0.040 (0.007); 28–30 +0.005;
31–33 +0.040; 34–36 +0.042; 37–39 +0.044; 40–42 +0.029; 43–45 +0.025 (0.008). Earnings among the employed are shown
only as figures (Figure 4, with tables in an online appendix that PMC serves behind a browser challenge). The text
says: "The lower earnings growth of second-generation Hispanic women is entirely explained by their low educational
attainment. After accounting for their education, both non-college- and college-educated second-generation Hispanic
women earn more than third-plus generation Whites throughout almost the entire age span." [SOURCE: PMC11784599
Table 3, "Multivariate Models of Women's Earnings".] So the women's paper also finds a **raw** earnings shortfall for
G2 Hispanic women; its favourable comparison is conditional on education and on working.

What the two papers do not measure, and NLSY97 can: the zero- and low-earnings years (both drop years under $5,000
from the earnings models), hours and hourly pay, a 1980–84 cohort, and education measured before the midlife window.
[INFERENCE from the method sections.]


## Where this agrees with the two papers, and where it does not

- **Men, agree.** Both find a gap at 25–27 that grows modestly for workers: the paper's fixed-effects widening is
  −0.039 (0.022) by 43–45; ours for men working in both windows is −0.050 (0.052). Both find education explains most
  of it, with a residual in the late 30s (paper: significant from 34–36 with education controls; here −0.105 at 35–40
  after reweighting). [SOURCE: PMC11784594 Table 2, appendix Table A1; CALCULATION]
- **Men, larger here.** Our mean-earnings gap widens by −0.116, three times the paper's log widening, because it keeps
  zero and low years (the paper drops years under $5,000) and a mean weights the top of the white distribution, which
  pulls away with age (pay and bridge terms). [INFERENCE from the decomposition]
- **Women, agree.** The paper finds employed G2 Hispanic women's lower earnings "entirely explained" by education and
  higher earnings after it; here the raw gap is ≈0 after education and pay is 8% higher at equal education.
  [SOURCE: PMC11784599; CALCULATION]
- **Women, disagree on employment.** The paper finds G2 Hispanic women 2.5–4.4 points more likely to earn $5,000+ than
  G3+ white women from 31 on (Table 3). Here the share with any earnings at 35–40 is 77.6% against 81.6%. Candidate
  reasons, untested: 1970s vs 1980–84 births, a $5,000 threshold vs any earnings, W-2 records vs self-report, and the
  paper counting Puerto Rico–born mothers as immigrants. [INFERENCE]

## Would change it

- **Parent birthplace in Puerto Rico.** NLSY97 parent questions say "United States" without naming the territories,
  so some G2 here may have Puerto Rico–born parents, whom the CPS and the men's paper count as G3+. A restricted
  geocode file with parent country, or a sensitivity dropping ASVAB Puerto Rican self-identifiers (code 24), would
  test whether this drives the G2 male gap. [GAP]
- **Bracket-only earnings.** 12% of G2 Hispanic men's interviewed person-years (539 of 4,615) and 9% of white men's
  (1,703 of 19,923) give only a bracket and are left out; a bracket-midpoint arm would show whether levels shift.
  [DATA: `derived/coverage.csv`; GAP]
- **Education after 25** is not in the adjustment; a time-varying education arm could move the adjusted widening. [GAP]
- **A larger CPS sample** (ASEC 2021–2025 pooled) would decide whether the G2 male panel gap (−0.31) and the
  cross-section (−0.13) differ. [GAP]

## Coverage

- **Fields used (259, `derived/field_inventory.csv`):** person keys (sex, birth date, screener ethnicity and race,
  variance stratum and PSU, AFQT percentile, ASVAB origin items, last round, final degree); per round the wage filter,
  wage amount and bracket, business filter, amount and bracket, cumulative-cases round weight, highest degree and
  grade; per calendar year 1996–2023 weeks and hours worked. Every field's count of non-skipped values equals the
  codebook total. The archive holds all 305,325 public NLSY97 variables, not 806.
- **Skipped:** gap-year income for missed rounds (`YINC-1400A/1700A`, small), job-level hourly rates
  (`CV_HRLY_PAY.xx`, replaced by earnings over hours), employee-only weeks and hours, other income sources. Income for
  odd years after 2010 is not asked; weeks and hours in those years are not used.
- **Respondents dropped:** Hispanics with unresolved generation (169 men, 144 women of 1,899 Hispanics), all other
  non-Hispanic non-white respondents, and anyone without a valid person-year in a window. Person-years dropped:
  bracket-only or refused earnings, missing weeks or hours (by group in `derived/coverage.csv`).
- **Small cells:** G1 Hispanic at 40–42 (57 men, 89 women) and the women's attriter cells are flagged, not read.
- **Reproduction:** `uv run --no-project --offline python3 scripts/rerun_lane.py
  infra/immigration-fiscal/career_trajectories_2026_09_29 "uv run --no-project --offline python3 {lane}/extract.py"
  "uv run --no-project --offline python3 {lane}/analyze.py" "uv run --no-project --offline python3
  {lane}/cps_check.py"` → IDENTICAL, 13/13 files. `extract.py` streams the 8 GB archive CSV (about 4 minutes).

## Log

- 2026-09-29 01:12 JST — lane created; stub written.
- 2026-09-29 01:31 JST — `extract.py` verified the archive hash (8c513e48…), indexed 305,325 codebook variables and selected 259
  fields; every field's non-skipped count equals the codebook total (`derived/field_inventory.csv`). The archive
  holds the whole public NLSY97 (305,325 variables), not 806 fields. `analyze.py` ran (2.4 s); outputs in
  `derived/`. Pending: CPS cross-check, rerun check, final write-up.
- 2026-09-29 01:41 JST — cps_check.py written and run; rerun_lane IDENTICAL 13/13; final write-up.

## Lead verification (2026-09-29 02:03 JST)

- Every verdict figure matches `derived/gaps.csv`, `growth.csv` and `levels.csv`: raw and adjusted gaps at 25–27 and 35–40 for both sexes and G3+, the balanced-panel and IPW widening, the men's pay (−0.064 → −0.165) and employment (−0.052 → −0.070) components, and the women's 77.6% against 81.6% with any earnings at 35–40.
- `scripts/rerun_lane.py` over extract, analyze and cps_check: IDENTICAL 13/13.
- Both papers checked in the PMC open-data XML. Men's Table 2: −0.116 (0.014) at 25–27 and −0.156 (0.019) at 43–45, which the text gives as "11.0% lower" and "14.5% less". Women's Table 3, G2 Hispanic column: −0.040 (0.007) at 25–27, +0.040 to +0.044 at 31–39, +0.025 at 43–45. These rows are level gaps, not changes from 25–27: the text says second-generation women "have significantly higher employment rates through nearly the entire 20-year age span", with "the only exception" at 25–27. The employment disagreement stands.
