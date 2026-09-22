<!-- reader extraction, opus-low agent, 2026-09-22; every numeric row carries a verbatim quote re-found in the parsed corpus text with rg -F; parent spot-checked the rows cited in the memo -->
[SOURCE: /Users/alien/Projects/corpus/doi_10_3102_0002831219860816/parsed.pymupdf4llm@0.3.4+cfg-99914b93/page.md]
[UNVERIFIED]

# Dee & Murphy (2019), "Vanished Classmates: The Effects of Local Immigration Enforcement on School Enrollment", AERJ

**Verdict:** A county-year difference-in-differences (with event study and a DDD using non-Hispanic
enrollment as the within-county control) showing that local 287(g) ICE partnerships cut county Hispanic
public-school enrollment by 7.3% on average and ~10% by two or more years after adoption, with a clean
non-Hispanic placebo; the design is credible for the policy's demographic footprint but is *not* an
immigration-quantity or fiscal estimate, and its dynamic (event-study) coefficients are individually
imprecise.

> Parsing note: the PDF-to-markdown converter renders the minus sign as "2" and "<" as "\". In the
> quotes below, a leading `2` before a decimal is a minus sign, `21 year lag` means "2+ year lag"
> (2 or more years after adoption), `61 years` means "±1 years", and `p \ .05` means p < .05.

## Population, period, unit
- Unit: **county-year**. Sample: the 168 U.S. counties in which a law-enforcement agency *applied* for
  a 287(g) agreement, 2000–2011; 55 of them had an agreement approved and active during the window.
  Unbalanced panel, N = 1,862 county-years (92.4% of the 2,016 potential cells).
  Quote: "our analytical sample consists of an unbalanced county-year panel of 1,862 observations (i.e., 168 counties observed annually over as many as 12 years)".
- Outcome population: K–12 public-school students, split Hispanic vs non-Hispanic, from NCES Common
  Core of Data universe surveys (enrollment as of October 1). Non-Hispanic is defined as White + Black +
  American Indian/Alaska Native + Hawaiian/Pacific Islander; **Asian and "two or more races" are excluded**
  from the control group because Asians are a non-trivial share of the undocumented population.
  Quote: "we exclude students identified as Asian from our measure of non-Hispanic student enrollment".
- Relevance to a Mexican-origin account: the authors justify the Hispanic-enrollment proxy by noting
  "more than 80% of unauthorized residents originated in Mexico and other Latin American countries",
  and that most children of undocumented parents are U.S. citizens (79%).
- Adoption timing: 5 counties 2005–2006; 49 counties 2007–2009; 1 in 2010; none 2011. Models by type:
  30 jail-enforcement, 9 task-force, 16 hybrid.

## Design and identification
- **Static DD** (Eq. 1): log(enrollment) on an "Active 287(g) MOA" indicator, county FE, year FE, an
  indicator for the 2009 five- vs seven-category race/ethnicity reporting change, SEs clustered by county.
  Optional county-year controls: log median household income (SAIPE) and unemployment rate (BLS LAUS).
- **Semidynamic DD** (Eq. 2): separate coefficients for the adoption year, 1-year lag, and 2+ year lag.
- **Event study** (Eq. 3): leads 1–5 and lags 0–2+, reference = non-adopters or ±1 year prior; used to
  test parallel pre-trends (F-tests on the leads).
- **Falsification / DDD** (Eq. 4): non-Hispanic enrollment as a placebo; then stacked county-ethnicity-year
  data (N = 3,724) with county-year, county-ethnicity and year-ethnicity fixed effects, so the treatment
  effect is identified *within county-year*, absorbing any county-year shock.
- **Selection control:** the comparison group is restricted to counties that also *applied* for 287(g), so
  the "wanting enforcement" selection is held fixed; a robustness row restricts controls to counties whose
  applications were **denied**. Approval criteria are not public, which is the residual identification worry.
- **Heterogeneous-timing/weighting check:** they implement the Gibbons–Serrato–Urbancic regression-weighted
  estimator and cannot reject equality with the fixed-effects estimate; they also run randomization inference.
  Quote: "we find that we cannot reject the null hypothesis of equivalence between our fixed-effect estimates and the corresponding ATE."
- No instrument, so no first stage.

## Headline estimates
All coefficients are on log enrollment, so a coefficient of −0.076 is a 7.3% reduction. SEs in parentheses,
clustered at the county level. Approximate 95% CIs are computed as coefficient ± 1.96×SE and are marked
[CALCULATION]; the paper reports SEs, not CIs.

| Outcome | Estimate (log points) | SE (95% CI [CALCULATION]) | Table / page | Verbatim quote (≤40 words) |
|---|---|---|---|---|
| Hispanic enrollment, static DD, no controls | −0.076 (−7.3%) | 0.035 (−0.145, −0.007) | Table 2 col (1), p. 16 | "The results in column (1) suggest that ICE partnerships reduced Hispanic student enrollments by a statistically significant 7.3% (i.e., exp(20.076) 2 1)." |
| Hispanic enrollment, static DD, with county-year controls | −0.075 | 0.034 (−0.142, −0.008) | Table 2 col (3), p. 16 | "Active 287(g) MOA 20.076** - 20.075** (0.035) (0.034)" |
| Hispanic, adoption year (semidynamic, no controls) | −0.049 (−4.8%) | 0.027 (−0.102, +0.004), p<.1 | Table 2 col (2), p. 16 | "Adoption year - 20.049* - 20.045*" |
| Hispanic, 1 year after adoption | −0.079 (−7.6%) | 0.034 (−0.146, −0.012), p<.05 | Table 2 col (2), p. 16 | "1-year lag - 20.079** - 20.075**" |
| Hispanic, 2+ years after adoption | −0.102 (−9.7%) | 0.047 (−0.194, −0.010), p<.05 | Table 2 col (2), p. 16 | "21 year lag - 20.102** - 20.104**" |
| Hispanic, adoption/1yr/2+yr **with** controls | −0.045 / −0.075 / −0.104 | 0.026 / 0.033 / 0.046 | Table 2 col (4), p. 16 | "(0.027) (0.026)" ; "1-year lag - 20.079** - 20.075**" ; "21 year lag - 20.102** - 20.104**" |
| Test of constant effect over time | p = .1107 (no controls); p = .0895 (with controls) | — | Table 2, p. 16 | "p value (H0: b1 = b2 = b3) - .1107 - .0895" |
| **Non-Hispanic enrollment, static DD (placebo)** | −0.005 (n.s.) | 0.016 (−0.036, +0.026) | Table 3 cols (3)-(4), p. 17 | "Active 287(g) MOA 20.076** - 20.005 - 20.070* (0.035) (0.016) (0.039)" |
| Non-Hispanic, adoption year / 1yr / 2+yr | −0.003 / −0.007 / −0.006 (all n.s.) | 0.013 / 0.016 / 0.022 | Table 3 col (4), p. 17 | "Adoption year - 20.049* - 20.003 - 20.043" ; "1-year lag - 20.079** - 20.007 - 20.064" ; "21 year lag - 20.102** - 20.006 - 20.103**" |
| Non-Hispanic constant-effect test | p = .6992 | — | Table 3, p. 17 | "p value (H0: b1 = b2 = b3) - .1107 - .6992 - .1733" |
| **DDD (Hispanic vs non-Hispanic within county-year), static** | −0.070 (−6.8%) | 0.039 (−0.146, +0.006), p<.1 | Table 3 col (5), p. 17 | "Active 287(g) MOA 20.076** - 20.005 - 20.070* (0.035) (0.016) (0.039)" |
| DDD, 2+ years after adoption | −0.103 (−9.8%) | 0.051 (−0.203, −0.003), p<.05 | Table 3 col (6), p. 17 | "21 year lag - 20.102** - 20.006 - 20.103**" |
| Hispanic **elementary** (K–5) enrollment, DD | −0.099 (−9.4%) | 0.036 (−0.170, −0.028), p<.01 | Table 4, p. 19 | "Elementary school 20.099*** 20.097*** 20.002 20.001 20.096**" |
| Hispanic elementary, DDD | −0.096 | 0.040 (−0.174, −0.018), p<.05 | Table 4 col (5), p. 19 | "Elementary school 20.099*** 20.097*** 20.002 20.001 20.096**" |
| Hispanic **middle** school (6–8) | −0.056 (n.s.) | 0.035 (−0.125, +0.013) | Table 4, p. 19 | "Middle school 20.056 20.055 0.003 0.003 20.059" |
| Hispanic **high** school (9–12) | −0.057 (n.s.) | 0.037 (−0.130, +0.016) | Table 4, p. 19 | "High school 20.057 20.057 20.013 20.014 20.043" |
| Non-Hispanic elementary (placebo) | −0.002 (n.s.) | 0.018 | Table 4, p. 19 | "Elementary school 20.099*** 20.097*** 20.002 20.001 20.096**" |
| Hispanic, **jail-enforcement** MOAs | −0.099 (−9.4%) | 0.049 (−0.195, −0.003), p<.05 | Table 5, p. 20 | "Jail 20.099** 20.099** 20.002 20.001 20.099*" |
| Hispanic, **task-force** MOAs | −0.050 (n.s.) | 0.063 (−0.174, +0.074) | Table 5, p. 20 | "Task force 20.050 20.038 0.001 0.001 20.047" |
| Hispanic, **hybrid** (jail + task force) MOAs | −0.047 (n.s.) | 0.047 (−0.139, +0.045) | Table 5, p. 20 | "Jail and task force 20.047 20.049 20.014 20.014 20.030" |
| Equality across MOA types | p = .6837 (no controls) | — | Table 5, p. 20 | "p value (H0: b1 = b2 = b3) .6837 .9256 .9256 .9050 .6346" |
| **Pupil-teacher ratio** | +0.267 ratio points (n.s.) | 0.198 (−0.121, +0.655) | Table 6 col (1), p. 21 | "Active 287(g) MOA 0.267 0.277 0.671 0.742" |
| Pupil-teacher ratio, with controls | +0.277 (n.s.) | 0.195 (−0.105, +0.659) | Table 6 col (2), p. 21 | "Active 287(g) MOA 0.267 0.277 0.671 0.742" |
| **% NSLP-eligible** | +0.671 pp (n.s.) | 0.608 (−0.521, +1.863) | Table 6 col (3), p. 21 | "(0.198) (0.195) (0.608) (0.536)" |
| % NSLP-eligible, with controls | +0.742 pp (n.s.) | 0.536 (−0.309, +1.793) | Table 6 col (4), p. 21 | "(0.198) (0.195) (0.608) (0.536)" |
| Event study, Hispanic: 5-year lead | +0.016 (n.s.) | 0.027 | Table A1, p. 24 | "5-year lead 0.016 0.016 20.009 20.009" |
| Event study, Hispanic: 2-year lead | −0.006 (n.s.) | 0.046 | Table A1, p. 24 | "2-year lead 20.006 20.004 20.012 20.012" |
| Event study, Hispanic: 1-year lead | −0.017 (n.s.) | 0.051 | Table A1, p. 24 | "1-year lead 20.017 20.018 20.007 20.007" |
| Event study, Hispanic: adoption year | −0.050 (n.s. in event study) | 0.053 | Table A1, p. 24 | "Adoption year 20.050 20.046 20.008 20.008" |
| Event study, Hispanic: 1-year lag | −0.079 (n.s.) | 0.057 | Table A1, p. 24 | "1-year lag 20.079 20.076 20.013 20.013" |
| Event study, Hispanic: 2+ year lag | −0.102 (n.s. individually) | 0.066 | Table A1, p. 24 | "21 year lag 20.102 20.105 20.011 20.012" |
| Joint test of Hispanic pre-trends (5 leads = 0) | p = .6753 (no controls), .5858 (controls) | — | Table A1, p. 24 | "p value (H0: b1 = b2 = b3 = b4 = b5 = 0) .6753 .5858 .4494 .5510" |
| Robustness: controls = **denied applicants only** | −0.105 (−10.0%), p<.01 | 0.036, N = 1,366 | Table A2, p. 25 | "Deniers only 20.105*** 20.105*** 20.003 20.003 1,366" |
| Robustness: excluding early adopters | −0.059, p<.1 | 0.033, N = 1,814 | Table A2, p. 25 | "No early adopters 20.059* 20.059* 0.004 0.004 1,814" |
| Robustness: excluding Los Angeles County | −0.062, p<.1 | 0.033, N = 1,850 | Table A2, p. 25 | "Exclude Los Angeles County 20.062* 20.062* 20.001 20.000 1,850" |
| Robustness: E-Verify control | −0.081, p<.05 | 0.034 | Table A2, p. 25 | "E-Verify control 20.081** 20.080** 20.007 20.007 1,862" |
| Robustness: Secure Communities control | −0.076, p<.05 | 0.035 | Table A2, p. 25 | "Secure communities control 20.076** 20.075** 20.005 20.005 1,862" |
| Robustness: **enrollment-weighted (WLS)** — Hispanic −19.9 log pts, non-Hispanic −6.5 (significant) | −0.199 / −0.065 | 0.054 / 0.021, p<.01 | Table A2, p. 25 | "Weighted least squares 20.199*** 20.143*** 20.065*** 20.047*** 1,862" |
| Robustness: balanced panel | −0.084, p<.1 | 0.044, N = 1,428 | Table A2, p. 25 | "Balanced panel 20.084* 20.082* 20.017 20.016 1,428" |
| Robustness: treatment dated 1 year earlier | −6.1%, p = .077 | — | Note 19, p. 30 | "we examined our main findings in models that moved the treatment adoption 1 year earlier and found it only attenuated our results modestly (i.e., a 6.1% reduction with a p value of .077)" |
| NSLP event study: adoption year and 1-year lag, with controls | +1.535 pp and +1.519 pp, p<.1 | 0.870 / 0.857 | Table A3, p. 26 | "Adoption year 0.249 0.246 1.292 1.535*" |
| Pupil-teacher ratio event study: 5-year lead | −0.253, p<.05 (a pre-trend flag) | 0.125 | Table A3, p. 26 | "5-year lead 20.253** 20.249* 0.619 0.545" |

### The 300,000 displaced-students calculation
It is a simple back-of-envelope scaling, not an estimated quantity: the pre-policy (2005) Hispanic K–12
base in the adopting counties (~3.2 million) times the 2+-year effect (~10%).
Quote: "we identified the total number of K–12 Hispanic students in the counties that adopted ICE partnerships in 2005 just prior to the onset of the policy as roughly 3.2 million. A 10% reduction from this base implies that these ICE partnerships eventually displaced around 320,000 students."
The abstract and discussion round this to "more than 300,000":
Quote: "We estimate partnerships enacted before 2012 displaced more than 300,000 Hispanic students."
Caveats the authors attach: it is a **net, cross-county** figure only.
Quote: "This is a net estimate and only accounts for cross-county moves observed in annual enrollment data. To the extent that families moved within counties or moved multiple times in a year, this estimate understates the potentially disruptive churn".
[INFERENCE] The counterfactual base is not adjusted for the counterfactual growth of the Hispanic
student population over 2005–2011, and the 10% comes from the coefficient with the widest SE, so the
±1.96 SE band on 0.102 alone spans roughly 30,000 to 620,000 students on that 3.2m base [CALCULATION].

### Out-migration versus non-enrollment (dropout / staying but unenrolled)
The measure cannot separate these by construction; the authors say so and argue from the age gradient.
- Quote: "the displacement observed in our enrollment measure can operate through encouraging threatened families to leave a community, dropping out of school, and discouraging other families from entering."
- Quote: "It is possible that enforcement-induced enrollment declines also reflect students who dropped out of school yet also remained in place (Amuedo-Dorantes & Lopez, 2015, 2017). However, our finding that enforcement effects are concentrated among elementary-school students is more consistent with effects on mobility than on dropout behavior."
- So the paper's own reading is **mobility (out-migration and inhibited in-migration), not dropout**,
  because the effect is in grades K–5 and absent at high school where dropout is possible.
- Where the movers go is not identified. Quote: "it is not clear how to examine this because the location choices of undocumented residents who move are uncertain."
- Spillovers to neighbouring counties were checked and were smaller and insignificant.
  Quote: "While we found suggestive evidence for similar effects in neighboring counties, the corresponding estimates were generally smaller and statistically insignificant."

## What it says about
- **Native wages by skill/education** — not studied.
- **Native employment / crowd-out** — not studied directly. Only cited from others: "there is evidence that 287(g) agreements reduce overall employment and create labor shortages in the agricultural sector".
- **Housing prices, rents** — not studied. Cited only: 287(g) agreements increase "Hispanic housing foreclosures rates" (Rugh & Hall, 2016).
- **Fiscal: taxes, transfers, public services, schooling** — the only fiscal-adjacent outcomes are the two
  school-resource proxies, both null. Pupil-teacher ratio: "We find that ICE partnerships had a small and statistically insignificant effect on the pupil-teacher ratio." The authors read the null as districts shedding staff in step with enrollment, i.e. **school spending adjusts to enrollment rather than leaving a windfall for remaining students**: "the null result with respect to pupil-teacher ratios suggests schools hired fewer teachers as a result of the policy-induced enrollment declines. This finding also indicates that the nonmobile student populations in counties that adopted ICE partnerships were not experiencing increased per-pupil resources". No revenue, per-pupil-dollar, tax or transfer outcome is estimated; there is no school-finance data in the paper beyond staffing and NSLP eligibility.
- **Student composition / poverty share** — null on NSLP eligibility, with a weak opposite-signed hint:
  "our results on the percentage of students who are NSLP-eligible also indicate small and statistically insignificant effects" and "there is some qualified evidence that ICE partnerships increased the share of remaining students whose low household income qualified them for the NSLP."
- **Firms, production, investment, profits** — not studied.
- **Crime** — not studied; only a cited null: "Another study focusing on the 287(g) agreements in North Carolina (Forrester & Nowrasteh, 2018) indicates that these partnerships actually had no effect on crime rates."
- **Mechanism the authors claim** — enforcement makes a county unattractive to mixed-status families, who
  leave and stop arriving: "local partnerships with ICE seemed to create highly unattractive environments for undocumented residents (and perhaps Hispanic citizens as well)". Welfare channel is student mobility: reactive moves and blocked strategic moves. Effect grows with time since adoption, consistent with awareness diffusing.

## Elasticities or parameters a model could transport
Nothing structural; the transportable objects are reduced-form policy semi-elasticities.
1. **Semi-elasticity of county Hispanic K–12 public enrollment with respect to an active local 287(g)
   agreement** = −0.076 log points (−7.3%) on average, rising to −0.102 (−9.7%) at 2+ years after adoption.
   Estimated on 168 applicant counties, 2000–2011, mostly 2007–2009 adopters.
2. The same object by grade span: K–5 −0.099, 6–8 −0.056, 9–12 −0.057 (only K–5 significant). Same population.
3. The same object by enforcement model: jail −0.099, task force −0.050, hybrid −0.047; no significant
   difference across models.
4. **Placebo/leakage parameter:** effect on non-Hispanic (excluding Asian) enrollment = −0.005 (SE 0.016),
   i.e. an upper bound of about 2–3% on any generalized county-level enrollment shock.
5. **Population-weighted version** (weights = 2004–05 enrollment): Hispanic −0.199, non-Hispanic −0.065.
   A DDD-equivalent difference of about −0.134, i.e. the effect is *larger* in big counties, and the
   non-Hispanic placebo fails under weighting. [INFERENCE] This is the single result most in tension with
   the headline and with the placebo logic; the authors handle it by pointing at the DDD difference.
6. **School-staffing response to an enrollment loss:** implied elasticity of teacher FTE to enrollment ≈ 1
   over this horizon, since the pupil-teacher ratio does not move. [INFERENCE] from the null in Table 6;
   the paper states the direction but reports no elasticity.
7. Not transportable: any per-student dollar figure, any wage or price elasticity, any number of adults
   affected. Hispanic enrollment is a proxy for the presence of mixed-status families, not a count of
   undocumented residents.

## Authors' stated limitations and external-validity notes
- Enrollment proxies only part of the exposed population: "school enrollment data by Hispanic ethnicity may be less subject to misreporting and external-validity concerns, they do not, of course, necessarily represent the entire population that might be influenced by ICE partnerships."
- Parallel trends is an assumption, and could bias toward zero if adopters were on a rising Hispanic trend:
  "our estimate of the impact of ICE partnerships would be biased downward if the successful adoption of this initiative were preceded by a comparative increase in Hispanic enrollments".
- Event-study dynamics are imprecise: "These point estimates are not statistically precise (see Table A1)." The constant-effect null is not rejected without controls (p = .1107).
- Anticipation: enrollment fell ~1% per year just before final MOA approval, attributed to communities
  knowing approval was coming; the 1-year-earlier treatment date attenuates the effect to 6.1%.
- Approval criteria unknown, so selection into *approval* among applicants is not directly observable:
  "the exact criteria that DHS used for determining which of these applications to approve are not specified publicly."
- Receiving counties are not studied; destinations of movers are unknown.
- Period-specific: estimated under Bush/Obama-era enforcement; the authors argue Trump-era partnerships are
  harsher, so "the current educational, economic, and social costs may be even more severe" (an extrapolation, not an estimate).
- Data construction involves substantial hand-repair: 376 county-year observations had values replaced from
  external sources and 177 involved at least one linear interpolation, mostly for NSLP eligibility and the
  pupil-teacher ratio. [INFERENCE] This matters most for the two null outcomes in Table 6, which are built
  on the most-repaired variables.
- Race-category reporting changed in 2009 and mechanically raised Hispanic counts; controlled for with a
  dummy, and results hold without it.

## Data availability
No replication package is mentioned. The 287(g) FOIA data were obtained from other researchers:
"Rugh and Hall (2016) acquired these data and generously shared them with us." All other inputs are public
administrative series: NCES Common Core of Data / ElSi, BLS Local Area Unemployment Statistics, Census SAIPE,
plus supplemental state and district education-agency reports used to patch missing values. Funding: IES
grant R305B140009, Stanford Immigration Policy Lab. [INFERENCE] Reconstruction is feasible from public
sources except for the exact FOIA-derived 287(g) application list and the hand-repaired enrollment cells.

## Verification log
All quoted fragments were re-found in the source with `rg -F`. 52 of 60 matched the raw file
directly; the other 8 span a line break in the parsed markdown and were matched against a
whitespace-flattened copy of the same file (`tr '\n' ' ' | tr -s ' '`). 60/60 verified, 0 rows dropped.
Every numeric row in the Headline estimates table carries a verified quote.
