claude-opus-5[1m]

**Verdict:** A **descriptive** CPS-ORG decomposition — no instrument, no quasi-experiment, the word
"causal" appears zero times — showing that splitting the US Black workforce by own/parental nativity
splits the "Black-White earnings gap" into three different objects: 2nd-generation Black immigrant men
sit at −0.110 log points at the median and −0.028 at p90, 2nd-generation women are *above* White women
(+0.077, +0.059), while native Black men stay at −0.340 / −0.280 (Table 1, p.28). Education closes 26%
of the native male median gap and 67% of the 1st-generation female one, but *nothing* for 2nd-generation
men, whose gap widens on adjustment because they out-educate White men. The arithmetic is reproducible
from the printed cells and the settlement simulation has a passing placebo. Three caveats must travel
with any citation: (a) **no standard errors appear anywhere in the tables** — the authors suppress them
deliberately (p.13), so the only precision information is the 95% bands in Fig. 2/4, widest for the 2nd
generation (n=812 men, 961 women) at roughly ±0.10–0.15 and crossing zero; (b) "parity" is **conditional
on working** — including non-workers the 2nd-generation male median gap more than doubles to −0.269
(Table S3, p.39); (c) **for transfer to the Mexican-origin population there is no Hispanic, Mexican or
Latino comparison group of any kind** (all 31 "Hispanic" hits are inside "non-Hispanic White"), and the
mechanism — a 2nd generation that out-educates native Whites by 3–5 pp BA+ — is the mirror image of the
Mexican-origin case. Contrast case and method template, not an analogy.

## Citation and version
Rong Fu (Waseda), Neeraj Kaushal (Columbia and NBER), Felix Muchomba (Rutgers). "How Immigration is
Changing the Black-White Earnings Gap." NBER WP 34327, October 2025, 42 pp. SSRN mirror 5568718.
**Not peer-reviewed; no published version as of 2026-09-21** (one web search; NBER/SSRN/RePEc show WP
only). No external funding. Standard NBER disclaimer: "They have not been peer-reviewed…" (p.1).

## Question, data, sample
CPS Outgoing Rotation Group files via IPUMS ("Flood and others 2024"), **1995–2024**, ages 25-64, pooled
into five six-year periods (1995-2000 … 2019-24): "To bolster sample sizes, we study five time points
comprising six years each" (p.4-5). National; **state is the finest unit** — "the CPS does not allow
analysis below the state level" (p.15).

Earnings concept: **log weekly earnings in 2024 dollars**, non-imputed only, excluding self-employed
(16%) and armed forces (1%), CPS earnings weights (p.6). Imputation rates differ sharply by group —
"25% of the non-Hispanic White workers' earnings data were imputed. The corresponding proportions for
Black workers were 38% for natives, 36% for 2nd generation immigrants and 37% for 1st generation" (p.6);
a replication including imputed values "yielded similar findings" but **no table is shown**.

Sample sizes, **2019-24 only — N is never reported for the other four periods**:

| 2019-24 | 1st gen | 2nd gen | Native Black | White reference |
|---|---|---|---|---|
| Male workers (Table 1, p.28) | 3,125 | **812** | 11,940 | 137,028 |
| Female workers (Table 1, p.28) | 3,358 | **961** | 15,857 | 131,967 |
| Male working-age pop. (Table S3, p.39) | 4,356 | 1,202 | 22,984 | 189,629 |
| Female working-age pop. (Table S3, p.39) | 5,797 | 1,535 | 30,827 | 216,954 |

## Identification
**None in the causal sense.** Four pieces: (1) quantile regressions of log weekly earnings at p50 and
p90 on a Black-group indicator plus five-year age dummies, or age + four education categories, by sex
and period; (2) kernel densities for 2019-24; (3) rank regressions where the outcome is the worker's
weighted percentile *in the White same-sex distribution*, 0-100, following Bayer and Charles (2018);
(4) a reweighting simulation. "shift-share", "difference-in-differences" and "causal" = zero hits;
"selection" appears once, in the discussion. **The GPSS / Borusyak-Hull-Jaravel / Adão-Kolesár-Morales /
Jaeger-Ruist-Stuhler apparatus is not applicable — nothing is instrumented.** Do not cite for a causal
claim.

The settlement simulation (p.14-16): estimate within-state empirical distributions of age-and-education
residuals per group, then draw 200,000 counterfactual observations per group with immigrant groups
redistributed across states on the **Black-native state share**, holding own earnings structure fixed.
Run twice, on the native-Black distribution of **2019** and of **1995**, to blunt endogeneity of current
location. The native column is an implicit placebo and passes: natives simulated onto their own 1995
pattern return −0.246 vs an adjusted −0.250 (men) and −0.094 vs −0.090 (women) — the machinery does not
manufacture gaps.

## Main estimates
Table 1 (p.28), CPS-ORG 2019-24 workers, log weekly earnings gap vs same-sex non-Hispanic Whites.
**No standard errors are printed.**

| Quantile / spec | 1st gen M | 2nd gen M | Native M | 1st gen F | 2nd gen F | Native F |
|---|---|---|---|---|---|---|
| p50 unadjusted (age) | −0.374 | **−0.110** | −0.340 | −0.271 | **+0.077** | −0.196 |
| p50 adjusted (age+educ) | −0.290 | −0.131 | −0.250 | −0.090 | +0.063 | −0.090 |
| p50 Diff. (educ share) | +0.084 | −0.021 | +0.090 | +0.181 | −0.014 | +0.106 |
| p50 Simulation-1995 | −0.339 | −0.209 | −0.246 | −0.136 | −0.032 | −0.094 |
| p50 Simulation-2019 | −0.342 | −0.211 | — | −0.130 | −0.031 | — |
| p90 unadjusted (age) | −0.184 | **−0.028** | −0.280 | −0.170 | **+0.059** | −0.218 |
| p90 adjusted (age+educ) | −0.170 | −0.045 | −0.164 | −0.091 | 0.000 | −0.094 |
| p90 Diff. (educ share) | +0.014 | −0.017 | +0.116 | +0.079 | −0.059 | +0.123 |
| p90 Simulation-1995 | −0.152 | −0.059 | −0.153 | −0.145 | −0.069 | −0.101 |
| p90 Simulation-2019 | −0.156 | −0.062 | — | −0.153 | −0.065 | — |

Verbatim rows (p.28): `Unadjusted (controls for age)  -0.374  -0.110  -0.340  -0.271  0.077  -0.196`
and `Unadjusted (controls for age)  -0.184  -0.028  -0.280  -0.170  0.059  -0.218`.

**Education's share** = Diff./|unadjusted| [INFERENCE, arithmetic on printed cells]: native men 26%
(p50) / 41% (p90); native women 54% / 56%; 1st-gen men 22% / 8%; 1st-gen women **67% / 46%**. For
2nd-gen men it is *negative* (−19% at p50): "Because 2nd-generation Black men have a higher educational
attainment than non-Hispanic White men, adjusting for education actually increases their earnings level
gap" (p.13-14). For 2nd-gen women the entire p90 advantage is education: +0.059 → exactly 0.000.

**Location's share**, simulation vs age+education-adjusted (p.16): "1st-generation Black men would have
a 5-percentage-points higher earnings gap (4.9=33.9-29.0 or 5.2=34.2-29.0) and 2nd-generation Black men
would have an 8-percentage-points higher gap (7.8=20.9-13.1 or 8=21.1-13.1); 1st-generation Black women
workers would have had a 4-percentage-points higher earnings gap and 2nd-generation women would have had
a 9-percentage-points higher earnings gap." Smaller at p90.

**Trends (Fig. 2, p.25 — plotted, never tabulated; read off `_cache/fig2-26.png`).** Male p50: 1st gen
flat and worst (≈−0.43, −0.47, −0.48, −0.45, −0.37); 2nd gen best (≈−0.20, −0.09, −0.12, −0.14, −0.11);
native ≈−0.35 flat. Male p90: 1st gen ≈−0.32, −0.38, −0.41, −0.31, −0.18 — the "halving" is measured
**from the 2007-12 trough**: "shrinking of the gap from (minus) 0.4 log points in 2007-2012 to (minus)
0.2 log points in 2019-2024" (p.8). 2nd-gen men cross above zero in 2001-06 (≈+0.05). Female p50: the
2nd-generation advantage **declines monotonically**, ≈+0.19 → +0.09 → +0.04 → +0.04 → +0.08.

**Rank gaps (Fig. 4, p.27)** are prose-only. One runs against the headline: 2nd-generation Black women
"started with positive rank gaps … but this advantage steadily declined toward zero by the study's end"
(p.12-13).

## Heterogeneity and mechanisms
Region of origin (Table S2, pp.37-38) is the only disaggregation the CPS supports — "sample sizes across
ethnic groups in the CPS are too small to allow analysis by specific country of origin" (p.10). 1st-gen
men: African 46% of group / 50.3% BA+; Caribbean 35% / 27.9%; Other 19% / 26.1%. 2nd-gen men: African
18% / 57.5%; Caribbean 51% / 42.5%; Other 31% / 37.9%. 2nd-gen women BA+: African 61.2%, Caribbean
53.6%, Other 40.4%. "all three groups of 2nd-generation Black female workers have earnings higher than,
or equal to, non-Hispanic White women" (p.18).

Education levels (Table S1, pp.36-37), 2019-24 vs same-sex Whites: 2nd-gen men **+3.0 pp** BA+, 2nd-gen
women **+4.9 pp**; native Black men **−17.6 pp**, native women **−16.1 pp** — and the native BA+ gap
*widened* from −16.7 and −11.8 pp in 1995-99. About a third of native Black working-age men and women do
not work in 2019-24 (p.7, Fig. S1).

## Robustness and what the authors concede
- **SEs suppressed by choice**: "We do not show the standard errors because they could be biased in
  regression models when the dependent variable is the residuals from a different regression (Chen,
  Hribar, and Melessa 2018)" (p.13).
- **Including non-workers** (earnings set to $1, log = 0), Table S3 p.39, is where the headline degrades
  most: the native male p50 gap blows out to **−0.537**, and — unremarked by the authors — the
  **2nd-generation male gap more than doubles to −0.269** and *worsens* to −0.298 under education
  adjustment, while 2nd-gen women fall to **+0.011** (parity, not advantage). The 1st-gen male gap
  *narrows* (−0.286 vs −0.374) because their employment rate is high. The paper reports only that "the
  primary patterns … remain" (p.12-13) and flags the native male widening (pp.9-10).
- **Third-generation truncation**, conceded: "our data allow us to identify only the 1st and 2nd
  generations … the category that we identify as natives includes 3rd and higher generations of Black
  immigrants, particularly those from the Caribbean whose forefathers arrived at the start of the 20th
  century" (p.18).
- Controls limited to age, education, state: "we do not control for other factors" incl. family
  composition (pp.18-19). Alternate simulation with White N fixed at 200,000 gives "similar" results
  with the protective influence "somewhat higher" — not shown (pp.15-16).

## Threats the authors do not address
- [INFERENCE] **The CPS race question changed in January 2003 to allow multiple-race reporting**, and
  the paper never states whether "self-reported Black race" is Black-alone or Black-in-combination —
  "multiracial", "multiple race", "alone", "2003" all have **zero** hits. A 1995-2024 race-gap trend
  crosses that break, and the 2nd generation is the group most likely to have one non-Black parent, so
  part of the 2nd-gen female downward drift in Figs. 2 and 4 could be definitional.
- [INFERENCE] **Ethnic attrition is never mentioned** ("attrition", "intermarri", "Duncan", "Trejo" =
  zero hits). If higher-SES 2nd-generation Black immigrants intermarry more and their children leave the
  self-reported Black sample, the measured advantage is bounded in one direction and the residual
  "native" pool is contaminated in the other.
- [INFERENCE] **Two sample filters are behavioral, not random.** Non-imputed-earnings selection bites
  11-13 pp harder on Black groups (38/37/36% vs 25%), and non-response correlates with job instability,
  so the retained Black sample is plausibly the more stably employed one — which flatters every gap here
  (asserted robust, no table). Excluding the self-employed (16%) additionally conditions the
  1st-generation estimates on wage-and-salary attachment, a common immigrant entry route.
- [INFERENCE] **The $1-earnings device in Table S3 is not an earnings gap** — at p50 it is close to a
  mechanical function of relative non-employment rates. A bound, not an estimate.
- [INFERENCE] **The simulation cannot separate place from selection into place.** The 1995 base year
  addresses reverse causation from current earnings to current location, not the fact that immigrants
  who chose high-opportunity states differ from those who did not; and the residual distribution is
  estimated within state from that same self-selected sample. State granularity is also very coarse
  relative to the neighborhood mechanism (Chetty-Hendren) the paper invokes, as it half-concedes (p.15).
- [INFERENCE] "the gap among men is twice that among women" (p.17) is loose: 1.7× at p50 (−0.340 vs
  −0.196), 1.3× at p90. The framing is also openly advocacy-adjacent ("set the record straight",
  pp.18-19, after a paragraph of political quotations on p.3) — which does not touch the arithmetic but
  predicts which robustness result goes unmentioned, and the Table S3 2nd-gen male reversal is that one.

## Answers to the repo's questions
**1. Data and generation identification.** CPS-ORG via IPUMS, 1995-2024, ages 25-64. Generations come
from **CPS parental birthplace**: "Starting in 1994, the CPS provides detailed data on respondents' and
their parents' countries of birth, which we use to stratify male and female workers with self-reported
Black race into three groups" (p.5). 1st gen = foreign-born; 2nd = US-born with **at least one**
foreign-born parent; "native" = US-born with **both** parents US-born (p.2). Earnings = log weekly
earnings, 2024 dollars, non-imputed, ex-self-employed and armed forces, earnings-weighted. N is given
**only for 2019-24** (table above); the binding cells are 812 2nd-gen men and 961 women. Since the
1st+2nd-generation share of the Black working-age population rose from 5% in 1994 to 23% in 2024 (p.2),
the unreported early-period 2nd-generation cells are materially smaller than 812.

**2. Gaps, quantiles, SEs, shares.** Full p50/p90 grid by generation and sex is the Table 1 block under
*Main estimates*; trends by period are the Fig. 2 reads below it. **SEs: none published** — suppressed
citing Chen-Hribar-Melessa (p.13); the only uncertainty anywhere is the 95% band in Figs. 2 and 4, read
off the rendered page as roughly ±0.10-0.15 for the 2nd generation and crossing zero. Any repo use of
"parity" must carry that. Education accounts for 26%/41% (native men, p50/p90), 54%/56% (native women),
22%/8% (1st-gen men), 67%/46% (1st-gen women), **−19%** for 2nd-gen men. Location is worth ~5 pp
(1st-gen men), 8 pp (2nd-gen men), 4 pp (1st-gen women), 9 pp (2nd-gen women) at p50.

**3. Parental selection, ethnic attrition, 3rd generation.** Selection is cited and **explicitly not
tested**: "Researchers attribute the success of Black immigrants to their positive self-selection
(referring to skills and other characteristics at arrival), cultural differences, and employer favoritism
vis-à-vis native Black workers (Model 2008a; Model 2008b; Waters 1999; Waters, Kasinitz, and Asad 2014).
Studies also show that 2nd-generation Black men and women have benefited disproportionately from
affirmative action policies (Massey et al. 2007; Rimer and Arenson 2004). More research is needed"
(p.18). No selection correction, no origin-country-quality control, no arrival-cohort decomposition. On
the third generation they concede only **truncation** (quote above, p.18) — 3rd+ generation Black
immigrants are pooled into "native", biasing the native benchmark *upward* and making the
2nd-gen-vs-native contrast conservative. **They do not engage the ethnic-attrition literature at all**,
so the selective-identification problem that dominates the Mexican-origin G3 literature is untouched.

**4. Hispanic or Mexican-origin comparison — there is none.** Grepped the full text: "Hispanic" occurs
31 times and **every occurrence is inside "non-Hispanic White"** (the reference group); "Mexic*",
"Latino" and "Latinx" occur **zero** times. The only within-Black disaggregation is Africa / Caribbean /
other (Table S2, Fig. S5). What transfers to this repo is the **method** — CPS parental-birthplace
G1/G2/G3+ stratification, level *and* rank gaps against a same-sex reference distribution, the
unadjusted-minus-adjusted education decomposition, and the state-reweighting settlement simulation with a
1995 base year — plus a **contrast result**: this 2nd generation out-educates the native White reference
by 3-5 pp BA+, the opposite sign of the Mexican-origin second generation, so nothing here should be read
as a general immigrant-generation regularity.

## Files covered / skipped
Read in full: `_cache/black_white_gap_immigration_w34327.txt` (1,109 lines = all 42 PDF pages of
extractable text) — cover, abstract, §I-IV body (pp.2-19), references (pp.19-23), Table 1 (p.28), Tables
S1-S3 (pp.36-39), Supplementary Text framework (pp.40-41). Table 1 and S1-S3 extracted cleanly under
`-layout`; no re-extraction needed. Rendered and read visually: **Fig. 2** (PDF page 26 →
`_cache/fig2-26.png`, `pdftoppm -r 160`), the paper's only source of uncertainty information; trend
values quoted from it are figure reads and are labeled as such.
**Skipped:** Figs. 1, 3, 4 and S1-S8 are raster images with no embedded numeric labels and no underlying
data table; their content is taken from the authors' prose and cross-checked against Table 1/S1 where it
overlaps. Fig. 4's rank-gap series are therefore prose-only — numeric rank gaps are not recoverable from
this PDF and would have to be re-estimated from CPS-ORG.
