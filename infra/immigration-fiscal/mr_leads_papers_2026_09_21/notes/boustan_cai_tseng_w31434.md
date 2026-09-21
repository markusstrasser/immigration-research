claude-opus-5[1m]

**Verdict:** In above-median-SES California suburban school districts, each additional Asian student
is followed by ~1.5 white student departures (IV −1.470, SE 0.268, F=56.26, Table 1 col 1), and the
authors rule out three alternatives credibly: no correlated Black/Hispanic entry, anti-Asian animus
that *falls* with education (so it cannot explain a high-SES-only effect), and a >1:1 rate that exceeds
the no-construction housing benchmark of Boustan (2010). Evidence level: well-identified shift-share
IV with an unusually thorough GPSS/BHJ control battery (Table 5: 20 specifications, all −1.07 to
−2.09), but the *mechanism* (fear of academic competition) is suggestive only — it rests on a
test-score pattern the authors themselves concede is observationally equivalent to selective exit of
high-ability whites (fn. 6, p.11). **The single most important caveat for transferring this to the
Mexican-origin population: this paper contains no estimate of white flight from Hispanic arrivals.**
Its "Hispanic and Black" coefficients are the effect of *Asian* arrivals *on* Black/Hispanic
enrollment — a placebo, not a comparison. The mechanism it advances (class-rank competition from a
high-achieving arrival group under California's top-percent policy) is precisely the mechanism that
does *not* transfer to a lower-SES arrival population; any cite of this paper for "white flight from
Hispanic immigration" is a misreading.

## Citation and version
Leah Platt Boustan, Christine Cai, Tammy Tseng, "White Flight from Asian Immigration: Evidence from
California Public Schools," NBER Working Paper 31434, July 2023, 38 pp. (JEL R23). Version read:
`_cache/boustan_cai_tseng_w31434.pdf` (pdfinfo: 38 pages, CreationDate 2023-07-04, ModDate 2023-08-03).
**Published as** "JUE Insight: White flight from Asian immigration: Evidence from California Public
Schools," *Journal of Urban Economics* 141 (2024), art. 103541, DOI 10.1016/j.jue.2023.103541.
Published abstract is materially identical to the WP abstract (only "in **these** higher-income
suburbs" added). No numbers appear in either abstract, and the published full text is paywalled, so
table-by-table identity of estimates is **[GAP] not verified**; the JUE "Insight" format is a short
paper, so the published version is likely a condensation of this WP rather than a revision.

## Question, data, sample
Does white public-school enrollment fall when Asian students arrive, and why? Unit = consolidated
California school district × year. Enrollment by race/grade from the CA Dept. of Education; 2000
Census + MABLE Geocorr 2000 crosswalk consolidates 987 raw districts → **415 consolidated districts,
of which 305 suburban, 80 rural, 30 central city** (Data Appendix A–B, pp. 25–26). Analysis sample =
suburban only, split at the median 2000 SES index (API + free/reduced-lunch share): **152 districts /
2,584 obs above-median, 153 / 2,598 below-median** (Table 1). Table notes say "2001-2016" but
2,584 / 152 = 17.0 exactly, i.e. a 17-year panel 2000–2016 — a minor internal inconsistency [INFERENCE].
Instrument inputs: 2000 Census tract-level Asian population by origin group (South Asian, Chinese,
Filipino, Japanese, Korean, Vietnamese = "92.3 percent of the Asian population in California as of the
2018 American Community Survey," p.8) and DHS *Yearbook of Immigration Statistics* annual new-LPR
inflows. Note DHS inflows "exclude the individuals who were already on U.S. soil (e.g., on a temporary
visa) and became permanent resident following an adjustment of status" (fn. 4, p.8) — a material
omission for H-1B-heavy South Asian and Chinese flows. Appendix Fig. 5 notes "Data for 2003, 2004 and
2005 are inexistent in the raw data and have therefore been extrapolated."

## Identification
Card (2001) shift-share. Eq. (2)–(3), pp. 6–7: predicted inflow = baseline national share of origin
group *j* resident in district *d* in 2000 × national flow of *j* in year *t*, summed over *j*, scaled
by the district's 2000 Asian-enrollment-to-Asian-population ratio (mean 0.28); cumulated onto baseline
Asian enrollment to form a predicted *stock* used to instrument actual Asian enrollment. Controls:
district FE, year FE, lagged total enrollment (t−1). Conley spatial-HAC SEs, "adjusted for spatial and
temporal correlation within 1,000 km and 10 decades" (all table notes). First stage above-median SES:
**1.476 (0.196), F = 56.26**; below-median SES: **−0.109 (0.116), F = 0.86** — the authors refuse to
interpret the low-SES IV on this basis (p.9).

Shift-share diagnostics actually run: **BHJ** — controls for 2000 Asian student share and 2000
nationwide Asian resident share, each × year FE, so that "we no longer rely on variation between
districts with high/low Asian shares, but instead leverage variation in high/low inflow
countries-of-origin within the Asian population" (p.12); estimates get *larger* (−1.853, −1.956).
**GPSS** — LASSO over 50+ Census attributes flags BA share, elderly (non-vet 65+) share, average
household size and median rent, each controlled × year FE, plus age-group and income-group controls.
**JRS** — addressed only by collapsing to 5- and 10-year differences, which the authors concede
changes the design rather than solving it: "The relevant variation in this case arises from the
initial shares, rather than the annual shifts, thus underscoring the importance of the added initial
district controls in Panel A" (p.13). **AKM exposure-robust inference: not performed.** **Pre-trends
/ event study: none reported** — the 1990-share instrument (Table 5 B8) is a different instrument, not
a pre-period placebo. Appendix Figs. 6–7 give residualized scatters (first stage 1.476, second stage
−1.470, OLS −0.642, reduced form −2.170) "to confirm that the results are not being driven by outliers."

## Main estimates
| Outcome (units) | Est. | SE | Table/page | Verbatim |
|---|---|---|---|---|
| White students, above-median SES, OLS | −0.642*** | 0.0909 | T1 col 1 p.20 | "the arrival of each Asian student into a high-SES suburban district is associated with 0.6 white departures" (p.9) |
| White students, above-median SES, **IV** | **−1.470*** | **0.268** | T1 col 1 p.20 | "each new Asian student leading to 1.5 white student departures" (p.9) |
| White students, below-median SES, OLS | 0.376* | 0.226 | T1 col 2 p.20 | — |
| White students, below-median SES, IV (F=0.86, uninterpreted) | 12.54 | 12.15 | T1 col 2 p.20 | "we do not interpret the IV estimates for this sub-sample" (p.9) |
| Hispanic+Black students, above-median SES, OLS | −0.0660 | 0.0603 | T1 Panel B p.20 | "no statistical relationship … between Asian arrivals and Black/Hispanic arrivals or departures" (p.10) |
| Hispanic+Black students, above-median SES, **IV** | **0.172** | **0.146** | T1 Panel B p.20 | "suggesting 0.17 arrivals of Black/Hispanic students for every Asian arrival in high-SES districts" (p.10) |
| Hispanic+Black students, below-median SES, OLS / IV | −0.0325 / 0.298 | 0.284 / 2.827 | T1 Panel B p.20 | — |

Units throughout: counts of students (district × year); above-median-SES dep. var. means are 5,472
white and 3,824 Hispanic+Black students. Income split (Appendix Table 1, p.34): white IV −1.896***
(0.419) above-median household income, first stage 0.701*** (0.224), **F = 9.69**; below-median income
IV 3.800* (2.137) with a *negative* first stage −0.428* (0.259), F = 2.70. Hispanic+Black under the
income split: above-median OLS −0.280*** (0.0847), IV −0.394 (0.405).

## Heterogeneity and mechanisms
**Within-above-median terciles (Appendix Table 2, p.35):** bottom tercile IV −4.497*** (1.399, F=5.28);
middle −2.256*** (0.382, F=120.43); **top tercile −0.841*** (0.136, F=97.25)**. OLS falls the same way
(−1.480, −1.291, −0.410).

**By origin group (Appendix Table 3, p.36; recovered from a raster image — see Files covered).**
First stage F: South Asian 197.20, Chinese 37.93, Filipino 14.69, Vietnamese 11.88, Korean 11.53,
Japanese 8.26. Second stage on white enrollment: South Asian −1.623*** (0.304), Chinese −1.747***
(0.294), Filipino −4.054*** (0.850), Vietnamese −2.865*** (0.327), Korean −3.325*** (0.677), Japanese
−3.465*** (0.719). "White flight is present for all groups in Panel B and ranges between 1.6 and 4
departures from every Asian arrival" (p.14).

**Racial animus (Table 2, p.21)** — ruled out by sign, not by measurement; all figures are % of white
respondents by HS-or-less / some college / BA+. GSS 2002 "feeling cool towards Asian Americans"
17.8 / 10.3 / 6.1 (N=2,134). Gallup 2006 opposing a close relative marrying an Asian 19.7 / 11.6 / 6.8
(N=4,570); little or no trust 13.0 / 9.7 / 5.1 (N=8,418). IAT "at most moderately American"
33.6 / 29.7 / 24.4 (2005, N=4,399) and 23.0 / 19.5 / 15.2 (2016, N=6,946). Logic: "this account is not
consistent with the fact that white flight is only observed in high-SES school districts, given that
high-income and more-educated respondents are less likely (rather than more likely) to express
negative attitudes toward Asian Americans" (p.10).

**Housing** — a theoretical benchmark, not an estimate. No house-price or rent regression is run
anywhere in the paper. "The model of white flight in Boustan (2010) suggests that, at the extreme, if
there is no construction response to new inflow, each Asian arrival will prompt exactly one white
departure even under the assumption of no racial preferences… if Asian entry is associated with more
than one-for-one white departures, something beyond housing prices must be the cause" (pp. 10–11).

**Test scores (Table 3, p.22)**, IV of standardized scores on Asian *share*: all students API 6.629***
(2.344), STAR math 12.50*** (4.231), STAR reading 9.814*** (2.651), SEDA math 0.126 (2.826), SEDA
reading 5.899*** (2.243). White students: API 2.526 (2.567), STAR math 19.99 (14.86), STAR reading
12.61 (8.531), SEDA math −0.274 (3.822), SEDA reading −3.304 (3.155) — all insignificant. "a
one-percent increase in Asian share in the district results in a 0.06- to 0.13-standard-deviation
increase in test scores, but no effect for white students alone" (p.11). Framing: relative class rank
of the average white student falls; California's 2001–2011 top-percent UC admissions policy made rank
pecuniary (Bleemer 2021, p.4).

## Robustness and what the authors concede
Table 5 (p.24, raster-recovered): main −1.470 (0.268). Panel A controls × year FE: 2000 nationwide
Asian resident share −1.853 (0.437); 2000 Asian student share −1.956 (0.366); BA+ share −1.588 (0.290);
elderly share −1.455 (0.271); average household size −1.321 (0.237); median rent −1.613 (0.318); age
groups −1.434 (0.247); household income groups −1.585 (0.314); average household income −1.523 (0.277);
average family income −1.503 (0.271); median family income −1.541 (0.284). Panel B: **no lagged
enrollment −1.069 (0.212)**; lagged 5 years −1.230 (0.266); ACS inflows −1.369 (0.250); 5-year
differences −1.467 (0.225); long difference 2000/2010 −1.579 (0.214); grades K-8 −1.319 (0.279);
grades 9-12 −1.852 (0.306); 1990 IV −2.085 (0.506). All *** at 1%.

Conceded: the instrument "will likely over-predict actual entry because our predicted change in
enrollment does not account for graduations or other departures from the district" (p.7); the low-SES
IV is uninterpretable (F=0.86); the high-*income* first stage is weak (F=9.69, p.9); the 1990-share
instrument first stage is "somewhat weaker (F-stat = 17)"; and, critically, fn. 6 p.11: "It is possible
that the null effects on white test scores reflect the net effect of two factors: (a) outflows of the
most gifted white students … and (b) increases in test scores for those students who do remain."

## Threats the authors do not address
- [INFERENCE] **The tercile gradient contradicts the paper's own narrative and partly undoes the
  housing-market exclusion.** Within above-median-SES districts, flight falls monotonically as SES
  rises (−4.497 → −2.256 → −0.841). The best-instrumented cell (top tercile, F=97.25) yields **0.841
  departures per arrival — below the 1:1 no-construction benchmark** the paper uses to conclude
  "something beyond housing prices must be the cause." The text reports only that the top two terciles
  have strong F-stats (p.9) and never confronts the gradient. The >1:1 inference is carried by the
  weakly-instrumented bottom tercile (F=5.28).
- [INFERENCE] **Group-specific LATEs diverge by 2.5×** (−1.623 South Asian to −4.054 Filipino). Under
  a single homogeneous "Asian student" treatment these should agree; the spread is evidence of
  instrument-specific exclusion violations or strongly heterogeneous effects. No overidentification
  test is reported, and the largest coefficients sit on the weakest instruments (Japanese F=8.26).
  Filipino and Vietnamese arrivals are also not high-SES groups, which strains the competition story.
- [INFERENCE] **Lagged total enrollment is a partial bad control.** Conditioning on total enrollment
  pushes the regression toward a composition identity in which an extra Asian student must displace
  someone. Dropping it moves the estimate from −1.470 to −1.069, a 27% fall — the headline uses the
  specification with the strongest mechanical channel, and −1.069 is barely above the 1:1 benchmark.
- [INFERENCE] **No AKM exposure-robust inference and no pre-trend test.** With 152 districts, a few
  high-exposure districts (Cupertino, Fremont, San Jose-area) plausibly dominate; Conley SEs at
  1,000 km do not address shift-share exposure clustering.
- [INFERENCE] **DHS new-LPR flows miss adjustment-of-status**, the dominant channel for H-1B-origin
  South Asian and Chinese arrivals in exactly the ethnoburbs driving the first stage; the "ACS inflows"
  robustness row (−1.369) partially covers this.
- [INFERENCE] **Displacement vs. never-arriving is not separated.** Table 4 col 3 uses only Census 2000
  and 2010 household counts, so "departure" includes whites who never moved in. Policy meaning differs.

## Answers to the repo's questions
1. **Design/sample/headline.** Card shift-share IV (construction in *Identification* above): 2000
   tract settlement shares of six Asian origin groups × DHS national inflows, scaled by the district's
   2000 Asian enrollment/population ratio, cumulated into a predicted stock. Sample = 152
   above-median-SES suburban California districts, 2,584 district-years, 2000–2016. Headline **IV
   −1.470, SE 0.268** (Table 1 col 1, p.20); first stage 1.476 (0.196), F = 56.26; OLS −0.642 (0.0909).
   "each new Asian student leading to 1.5 white student departures" (p.9).
2. **Hispanic and Black.** The paper **does not estimate white flight from Hispanic or Black arrivals
   at all.** Its Hispanic/Black regressions put Hispanic+Black enrollment on the *left* side with Asian
   enrollment on the right, as a test that Asian entry is not proxying for minority entry: above-median
   SES OLS **−0.0660 (0.0603)**, IV **0.172 (0.146)**; below-median SES OLS **−0.0325 (0.284)**, IV
   **0.298 (2.827)** (Table 1 Panel B, p.20). Under the income split (Appendix Table 1, p.34):
   above-median OLS **−0.280*** (0.0847)**, IV **−0.394 (0.405)**; below-median OLS **−0.0147 (0.257)**,
   IV **−0.921 (0.798)**. "there is no statistical relationship, either in OLS or in IV, between Asian
   arrivals and Black/Hispanic arrivals or departures in either low- or high-SES districts" (p.10).
   The only Hispanic/Black *comparison* is to outside literature: "The estimates of white/native flight
   from the most closely related studies range from 1.4 to 2.7 white departures for each minority
   arrival. Our estimate of white flight from Asian arrivals falls on the low end of this range" (p.3),
   and in conclusion "a rate of white flight that is somewhat lower but not too dissimilar from flight
   from Black/Hispanic populations documented in different settings" (p.14).
3. **Where the white students go — out of the district, not into private or charter** (Table 4, p.23).
   White students in charter schools IV **−0.0699*** (0.0409), OLS −0.151*** (0.0531), F=63.21, N=889
   over 46 districts. All students in private schools IV **−0.400**** (0.178), OLS −0.0806 (0.0610) —
   private enrollment *falls* too. White households with kids (Census 2000 and 2010 only, N=304) IV
   **−1.493*** (0.184)**, OLS −0.766*** (0.0626), F=202.88. "white students were most likely to leave
   districts entirely as Asian students arrive" (p.11). Consistency check, fn. 7 p.12: "the average
   white household with children at home in California had 1.25 children of school age… Around 90
   percent… enrolled in public school. The implied departure rate of white children from public school
   (1.5 x 1.25 x 0.9 = 1.68) is very close to our baseline estimate."
4. **Mechanisms** (full coefficients under *Heterogeneity* above). Academic competition is favoured
   but *not identified*: all-student scores rise while white-student scores are flat (Table 3, p.22),
   so the average white student's relative rank falls — but fn. 6 concedes selective exit of gifted
   whites produces the same pattern. Attitudes (Table 2, p.21) run the wrong way across education
   (~3:1 more negative among HS-or-less), so animus cannot explain a high-SES-only effect. Housing is
   excluded by the >1:1 Boustan (2010) benchmark, **not by any price estimate**. Correlated
   Black/Hispanic entry excluded by Table 1 Panel B.
5. **Fiscal and house-price implications: the authors state none.** No fiscal or revenue analysis
   appears anywhere. No house-price or rent regression is estimated; housing enters only as the
   theoretical 1:1 threshold. [INFERENCE] Any fiscal reading is ours, not theirs — and note the paper
   implies near-total *enrollment* replacement in these districts rather than enrollment loss, so
   per-pupil-funded district revenue is roughly held while composition changes.

## Files covered / skipped
Read in full: `_cache/boustan_cai_tseng_w31434.txt` (1,315 lines = all 38 PDF pages) — cover/abstract,
body §I–VII (pp. 1–14), references (pp. 15–19), Tables 1–5 (pp. 20–24), Data Appendix A–B (pp. 25–26),
Appendix Figures 1–7 (pp. 27–33), Appendix Tables 1–3 (pp. 34–36).
**Re-extracted:** Table 5 (p.24 = PDF p.26) and Appendix Table 3 (p.36 = PDF p.38) are embedded raster
images with no text layer — `pdftotext -raw` returned titles and notes only. Recovered via
`pdftoppm -r 240 -png` and read visually; every Table 5 / Appendix Table 3 number above comes from that
image read, not from the text layer or from memory.
Skipped: Appendix Figs. 1–5 and Data Appendix Table 1 (graphics/administrative lists, no estimate used
here); Figs. 6–7 slopes were legible in the text layer and are reported. Not obtained: the paywalled
JUE published PDF ([GAP], above).
