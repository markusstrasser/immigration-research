claude-opus-5[1m]

**Verdict:** A careful, honestly-reported shift-share IV showing that CZs with more less-educated foreign-born
working-age residents have materially lower institutionalization of the **U.S.-born** elderly (−1.5 pp at 65+, −3.8 pp
at 80+ per 10 pp of immigrant share; 26–29% of the mean), with a coherent mechanism: aide wages fall, aide employment
and hours rise, RN employment falls. Evidence level: **credible quasi-experimental, single design, not replicated on
other data** — the authors concede they cannot separate short- from medium-run effects (Jaeger et al.), that the
result vanishes under year×state effects (−0.061, ns, F=4.85), and that dropping California nearly halves it (−0.090,
F=9.22, below the Stock–Yogo cutoff). For transfer to the Mexican-origin resident population the decisive caveat is
that **the paper never decomposes by origin**: treatment is all-origin less-educated foreign-born share, the 1980–2000
identifying variation is visibly dominated by Mexican settlement (the instrument's extreme value is a Texas border CZ
at a predicted 211% share; dropping California guts it), yet no Rotemberg/GPSS decomposition is run — so "how much of
this is Mexican immigration" is asserted by geography, not measured. Second: the paper produces **no dollar figure at
all** — no Medicaid, Medicare or private saving, no mortality, no care-quality outcome. Monetizing it requires
entirely outside inputs.

## Citation and version

Kristin F. Butcher (Wellesley/Brookings/NBER), Kelsey Moran (MIT), Tara Watson (Williams/NBER), "Immigrant Labor and
the Institutionalization of the U.S.-born Elderly", NBER Working Paper 29520, November 2021, 58 pp. (PDF internal
title `immig_elderly_draft_R&R_111821` — this is the R&R draft.) Funding: NIA 1R03AG051861-01 and the **Peterson
Foundation's Project 2050** (p.2); NSF GRFP for Moran.

Published: *Review of International Economics* 30(5), Nov 2022, pp. 1375–1413, DOI 10.1111/roie.12607, first published
21 Mar 2022, special issue "Immigration to OECD countries". The published abstract is **word-for-word identical** to
the NBER abstract, all four headline numbers included (1.5 pp, 3.8 pp, 26–29%, 0.5 pp / 10%) — the headline estimates
did not change. [INFERENCE] the Wiley PDF is paywalled, so table-level changes cannot be excluded; the abstract match
makes a material change unlikely.

## Question, data, sample

Does local less-educated immigrant labor supply causally reduce the probability that U.S.-born elderly live in an
institution? Data: IPUMS decennial Census 1980/1990/2000 (primary), 1970 Census (instrument base year and elderly
internal-migration base), ACS 2010 and 2017 (extended sample). Unit of geography: **commuting zone** (Autor–Dorn
crosswalk; each microdata record is replicated across up to 722 CZs with fractional weights, p.11 fn.10 — this is why
N ≫ unique N).

Primary sample, 65+, 1980–2000: **7,286,430 observations / 4,294,262 unique**; 80+: 1,684,781 / 972,848 (Table 2 Panel
A col 1; Table 3 Panel B). Outcome means 0.0515 and 0.148. Composition (App. T2 col 1): age 74.2, female 0.594,
married 0.539, NH white 0.887, NH black 0.085, Hispanic 0.017. Outcome caveat the authors state themselves (p.10):
*"Our primary analyses use decennial U.S. Censuses, which do not allow us to identify the type of institution in which
an individual resides. In other words, prisons, nursing homes, and other types of institutions are
indistinguishable."*

## Identification

Shift-share (Bartel/Altonji–Card). Base share = CZ share of the 1970 U.S. stock of each of **39 country-of-origin
groups** (from Jaeger, Ruist & Stuhler; Jaeger supplied the definitions, p.2); shift = national count of less-educated
working-age immigrants from group *j* in year *t*; predicted counts summed over *j* and divided by CZ working-age
population (eqs. 2–4, pp.12–13). Endogenous regressor = observed share. Individual-level first and second stage, CZ
FE, year FE, birth-state×race, year×age×race, gender×marital-status FE, education in 4 categories. SEs clustered on
CZ. First stage (T2 Panel B col 1): **0.324*** (0.061)** — *"a 10 percentage point increase in the instrument … is
associated with approximately a 3.2 percentage point higher share"* (p.17–18). **Kleibergen–Paap rk Wald F = 28.31**
vs Stock–Yogo **23.1** (p.18, fn.13; they explicitly reject the Staiger–Stock rule of 10 as invalid under clustering).

Shift-share problems addressed:
- **Jaeger–Ruist–Stuhler serial correlation: addressed and conceded.** Table 6 col (2) instruments
  current and lagged share jointly: coefficients −0.039 (0.352) and −0.099 (0.304), **F = 0.390**,
  under-ID LM p = 0.412. p.23–24: *"we lack the power to separately identify the effect of current
  and lagged immigration, consistent with the key finding of Jaeger et al. (2018)."* Excluding 1980
  (col 4) gives F = 0.00583. In the longer 1980–2017 sample (Appendix Table 6 col 2) the split *is*
  estimable (F = 12.88) and the **lag** carries the effect: current −0.076 (0.061) ns, lagged
  −0.083** (0.040); 80+ lagged −0.243*** (0.072). That supports their medium-run reading.
- **Base-year trends:** Table 7 cols (2)–(3) interact initial 1970 immigrant share with linear and
  year-specific trends: −0.162** (0.082) and −0.182** (0.080), F falls to 10.15 / 8.20. Magnitude
  survives, instrument strength does not.
- **Goldsmith-Pinkham–Sorkin–Swift (Rotemberg weights), Borusyak–Hull–Jaravel, Adão–Kolesár–Morales:
  not implemented, not cited.** No exposure-robust or shift-level inference anywhere in the paper.
  **Pre-trends / placebo on the outcome: none run** (no pre-1980 trajectory test).
- **Selective migration of the elderly: addressed two ways**, neither of which moves the coefficient.
  (a) Alternative instrument from 1970–80 birth-state→CZ retirement probabilities × predicted
  immigrant share, varying at birth-state×year (eq. 5, p.20; Table 4). (b) Lagged cohort
  institutionalization rates as health proxies (Table 5).

## Main estimates

Coefficients are per **one unit** of share (0→1), i.e. divide by 10 for a 10 pp change.

| Outcome / spec | Estimate (SE) | Units | Table/page | Verbatim |
|---|---|---|---|---|
| 65+ institutionalized, **OLS** 1980–2000 | −0.076*** (0.019) | pp inst. per unit share; mean 0.0515 | T2 Panel A col 1 | *"a 10 percentage point increase in immigrant share is associated with a 0.76 percentage point reduction in the probability of living in an institution, on a base of 5.2 percent"* (p.16–17) |
| 65+ institutionalized, **2SLS** 1980–2000 (preferred) | **−0.151*** (0.027)**, F=28.31 | same | T2 Panel C col 1 | *"a 1.5 percentage point decline in the probability of an elderly person being institutionalized, on a base rate of 5.2 percent"* (p.18–19) |
| **80+ institutionalized, 2SLS** 1980–2000 | **−0.380*** (0.074)**, F=33.44 | mean 0.148 | T3 Panel B col "All" | abstract: *"1.5 and 3.8 percentage points for those aged 65+ and 80+"* |
| 65+, **alternative (birth-state) IV** | −0.161*** (0.038), F=60.19; 1st stage 0.489*** (0.063) | mean 0.0515 | T4 | *"Point estimates are highly significant and larger in magnitude than those using the standard instrument"* (p.21) |
| 80+, alternative IV | −0.522*** (0.114), F=57.12 | mean 0.148 | T4 | — |

Other windows, all same units: 65+ long difference 1980–2000 excluding 1990, −0.148*** (0.022), F=23.91 (T2 Panel C
col 2); 65+ over 1980–2017, −0.310*** (0.113), F=35.01 (col 3) and its long difference −0.328* (0.181), F=17.35 (col
4); 80+ over 1980–2017, −0.815*** (0.243), F=45.06 (App. T3 Panel B). Extending to 2010/2017 roughly doubles the
coefficient on a lower base.

Decade-by-decade 2SLS (T2 Panel C cols 5–8): 1980–90 −0.145*** (0.055) F=7.53; 1990–2000 −0.159** (0.077) F=31.97;
**2000–10 +0.224 (0.194) with a wrong-signed first stage −0.393* and F=2.93**; 2010–17 −0.106 (0.104) F=7.99 — why the
preferred window stops at 2000 (p.18). On IV ≈ 2× OLS (p.19): *"consistent with the notion that immigrants are moving
into commuting zones where unobserved factors are tending to increase (or, more accurately, slow the secular decline
in) the institutionalization among the elderly. Alternatively, the variation exploited by our instruments … may have a
different local average treatment effect."*

## Heterogeneity and mechanisms

**Subgroups (Table 3, 1980–2000).** 65+: NH white −0.160*** (0.026); NH black −0.108** (0.050); **Hispanic −0.562
(0.403), F=2.808 — uninformative**; no college −0.137*** (0.031); some college+ −0.133*** (0.028); female −0.183***
(0.032); male −0.090*** (0.021). 80+: white −0.409*** (0.073); black −0.438*** (0.162); Hispanic +0.007 (1.094),
F=3.224; no college −0.387*** (0.085); some college+ −0.258** (0.110); female −0.457*** (0.089); male −0.211**
(0.084). p.19: *"We see only modest differences by race/ethnicity, educational attainment, or gender."*

**Labor market (Table 8, CZ-year 2SLS, 1980–2000; log outcomes, coefficient per unit share).** The authors' own
scaling is ×0.033 (the 1980–2000 mean increase): *"median wages for nursing and health aides would have been about 8
percent higher in the year 2000 if immigration had remained at 1980 levels"* (p.27). Per 10 pp the same coefficient is
≈ −22%.

| Occupation | log median FTFY wage | wage rel. to CZ median | log employment | emp / working-age pop | log annual hours | share of CZ hours |
|---|---|---|---|---|---|---|
| Nursing & non-nursing health aides | −2.4740*** (0.329) | −1.1812*** (0.348) | +2.1675** (0.973) | +0.0437* (0.025) | +1.7752** (0.904) | +0.0414* (0.024) |
| — Home health aides | −3.2055*** (0.518) | −0.6298 (0.509) | +3.9066*** (1.419) | +0.0548** (0.024) | +3.5310* (1.828) | +0.0516* (0.027) |
| — Nursing-home aides | −2.2418*** (0.281) | −1.2995*** (0.173) | +3.0369** (1.376) | 0.0034 (0.003) | +3.5207** (1.456) | −0.0022 (0.003) |
| — Other health aides | −0.7055*** (0.227) | −0.5904*** (0.171) | −2.1713** (0.903) | −0.0145*** (0.004) | −1.4624* (0.793) | −0.0079 (0.005) |
| Licensed practical nurses | −0.7802** (0.396) | −0.2150 (0.386) | −1.4593 (1.030) | −0.0086*** (0.003) | −1.0365 (0.977) | −0.0072** (0.004) |
| Registered nurses | +0.2607 (0.552) | **+1.2019** (0.557)** | **−3.0826*** (1.000)** | −0.0439*** (0.005) | −3.0044*** (0.940) | −0.0429*** (0.009) |
| Housekeepers & gardeners | −2.0309*** (0.274) | −1.4991*** (0.368) | −0.3011 (1.115) | +0.0201*** (0.007) | 0.3715 (1.413) | 0.0074 (0.007) |
| Construction workers | −1.7887*** (0.329) | −1.7210*** (0.492) | −2.5875*** (0.628) | −0.0466*** (0.013) | −0.7819 (0.701) | −0.0152 (0.015) |
| All other, no college | −1.0794*** (0.207) | −0.1464 (0.122) | −0.2813 (0.805) | +0.7088*** (0.146) | 0.4950 (0.785) | +0.6165*** (0.172) |
| All other, all education | −0.2500 (0.336) | 0.0442 (0.047) | −0.9221* (0.499) | 0.0352 (0.032) | −0.4492 (0.481) | 0.0163 (0.033) |

(The nursing-home-aide relative-wage SE is printed in the source as `-0.173`, unparenthesised and signed, where every
other cell uses `(0.173)` style; I re-extracted PDF page 50 with `-raw` to confirm it is the paper's own formatting
slip, not an extraction artifact. Read it as SE = 0.173.)

**Mechanisms ruled out by the authors.** Housing costs: T7 cols (8)–(9) add CZ median 2BR rent (−0.151***) and median
property tax + insurance (−0.166***) — no movement. Wealth effects and social norms: argued away from the absence of
subgroup differences (p.28), conceding *"our subgroup analysis lacks statistical power and we do not have information
on social networks."*

## Robustness and what the authors concede

Table 7 (65+, 1980–2000), baseline −0.151***: region linear trends −0.150*** (0.026); **year×region −0.076** (0.036),
F=18.36 — halves**; state linear trends −0.152*** (0.027); **year×state −0.061 (0.058), ns, F=4.847**; median rent
−0.151***; property tax/insurance −0.166***; **drop California −0.090** (0.045), F=9.217**; drop all demographic
controls −0.081* (0.048); drop all but age −0.111*** (0.032).

The year×state concession is explicit (p.25): *"After controlling for state\*year effects, there is no statistically
significant association and the instrument is weak … Therefore, we cannot rule out the possibility that unobserved
state-specific or locality-specific policy variation correlated with immigrant location patterns has a direct effect
on institutionalization."* Their summary claim (p.26): *"we conclude that the negative association … is robust, with
47 of 48 coefficients in Appendix Table 7 showing a negative point estimate."* I verified it — the single positive
cell is 80+, 1980–2000, year×state = +0.062 (0.147).

Lagged cohort health proxies (Table 5): baseline −0.151*** → −0.146***, −0.148***, −0.152***, −0.152***; 80+ −0.380***
→ −0.356***/−0.357***/−0.376***/−0.381***. The proxies themselves are strongly predictive (CZ 10-yr lag 0.251***;
birth-state 10-yr lag 0.522***) yet change nothing.

**Internal inconsistency:** the conclusion (p.29) states *"institutionalization rates in 2000 would have been 0.5
percentage points (10 percent) lower if immigration had remained at 1980 levels"* — the sign is backwards relative to
the abstract and p.19 (should be *higher*). A drafting error in the NBER draft, not an estimate difference.

## Threats the authors do not address

- [INFERENCE] **Group-quarters classification drift.** Census GQ coding of "institutionalized" is not
  constant across 1980/1990/2000; board-and-care and assisted-living facilities sit on the
  institutional/non-institutional boundary and their treatment shifted. Assisted living grew fastest
  in the Sunbelt over exactly 1980–2000 — the CZs the instrument loads on. Reclassifying the same
  elderly person from "institution" to "community" reproduces this result with zero change in care.
  The paper never tests GQ-code stability.
- [INFERENCE] **Medicaid HCBS waivers are the missing confounder.** §1915(c) home- and
  community-based waivers expanded from 1981 onward, are set at **state** level, and directly shift
  the elderly out of nursing homes — exactly the variation absorbed by year×state effects, where the
  coefficient dies. The authors name "state-specific policy variation" generically but never name or
  control waiver generosity, the one policy whose mechanism is identical to their outcome.
- [INFERENCE] **No pre-trend or placebo on the outcome.** Trend controls are on the 1970 immigrant
  *share*, not on prior institutionalization *trajectories*; the available placebo (instrument from
  post-1970 shifts predicting 1960→1980 change) is not run.
- [INFERENCE] **Survivorship in the denominator.** Institutionalization is a share of *surviving*
  elderly, so any CZ-level difference in elderly mortality (or in where death occurs) moves it
  mechanically. No mortality outcome is reported anywhere.
- [INFERENCE] **Inference is likely too tight.** SEs cluster on CZ only. AKM show shift-share SEs
  clustered on the unit of geography are materially understated when exposure shares are spatially
  correlated — here extremely so (Mexican base shares concentrated on the border). With F = 28.31
  against a 23.1 cutoff, an exposure-robust correction could plausibly push the preferred
  specification into the weak-instrument region.
- [INFERENCE] **Welfare sign is assumed, not measured.** The interpretation rests on a stated
  preference for aging in place (Binette & Vasold); no health, functional-status, care-quality,
  out-of-pocket-cost or family-burden outcome is measured. Care bought at a 22% lower aide wage is
  cheaper care, not demonstrably better care.

## Answers to the repo's questions

**1. Treatment definition, geography, years, data.** Share of the **working-age (16–64) population** — *not* the labor
force, despite the abstract's "labor force share" wording — that is foreign-born **and** less-educated, where
less-educated = *"completing less than one year of college"* (p.11). **All origins** (39 country-of-origin groups from
Jaeger–Ruist–Stuhler, ≥5,000 obs in the 1990 Census). Geography: **commuting zones** (Autor–Dorn), not MSAs. Years:
1980, 1990, 2000 Census (preferred); 1970 Census for the instrument base; 2010/2017 ACS in extended appendix samples.
Elderly sample is **U.S.-born only**, ages 65+ (and 80+ subsample). N = 7,286,430 (4,294,262 unique).

**2. IV, OLS, first stage, splits.** 65+ IV **−0.151*** (0.027)** vs OLS **−0.076*** (0.019)** — IV ≈ 2× OLS. 80+ IV
**−0.380*** (0.074)**; no 80+ OLS is reported. First stage 0.324*** (0.061), **Kleibergen–Paap F = 28.31** (65+) /
33.44 (80+) vs Stock–Yogo 23.1. Splits exist for **race/ethnicity, education and sex** only (T3, numbers under
Heterogeneity above), uniformly modest at 2–4% of the mean per pp; the **Hispanic** cells are useless (F = 2.8 / 3.2,
SEs 0.40 / 1.09); female effects run ~2× male, tracking women's higher base rate (0.0634 vs 0.0341). **No
marital-status split** — it enters only inside the gender×marital-status fixed effects.

**3. The 0.5 pp / 10% counterfactual.** Preferred coefficient × the **mean increase in less-educated immigrant share
1980→2000 of 3.3 pp**: 0.151 × 0.033 = 0.00498 ≈ 0.5 pp, against the year-2000 mean rate of 0.050 (T1) → 10%. Year:
**2000**. Verbatim (p.19): *"Given the average increase of 3.3 percentage points in less-educated immigrant share
between 1980 and 2000, this implies that a typical U.S-born individual over age 65 in the year 2000 was 0.5 percentage
points (10 percent) less likely to be living in an institution than would have been the case if immigration had
remained at 1980 levels."* T1 puts the CZ mean at 0.039 → 0.071, i.e. 3.2 pp, so 3.3 is their elderly-weighted figure.
**No implied headcount is reported.** [INFERENCE] with ~31–32 M U.S.-born 65+ in 2000 (external input), 0.5 pp ≈
**155,000–160,000 fewer institutionalized elderly**.

**4. Mechanism estimates.** Full grid in the Table 8 block above. Pattern: aide wages fall sharply and aide
employment/hours rise — health aides −2.474*** log points per unit share (≈ −8% at the 1980–2000 shift, ≈ −22% per 10
pp), home health aides −3.206*** with log employment +3.907***; housekeepers and gardeners −2.031***; construction
−1.789***. RNs move the opposite way: relative wage +1.202** with employment −3.083*** — the capital/skill-intensive
input contracts, which is the production-technology story's sharpest confirmation. **No price series for home services
is used** — cost is inferred entirely from occupational wages (Cortes 2008 is cited for prices; nothing is estimated).
**Effects on native workers in those occupations are explicitly NOT estimated** (p.27): *"we have not attempted to
answer how immigrant inflows affect wages of U.S. natives, and the wage effects we see could be driven by
compositional impacts."* The nearest native-relevant row, "All other (no college)" at −1.0794*** (≈ −3.6% over
1980–2000), also pools natives and immigrants.

**5. Cost savings, quality, mortality, family caregiving.** **No cost-saving estimate of any kind** — not Medicaid,
not Medicare, not private. The only spending number in the paper is national context (p.3): *"8 percent of total U.S.
healthcare spending—or $286.2 billion—was spent on nursing facilities and home health care in 2019 (CMS 2020)."* **No
mortality outcome, no care-quality outcome**; quality enters only as citations (Miller et al. 2009 on nursing-home
mortality in tight labor markets; Furtado & Ortega 2020 on falls; Grabowski–Gruber–McGarry 2020 on staffing/quality).
**Family caregiving is descriptive only** (App. T1, HRS 2002/2004, native-born 55–90 receiving help; ADL / IADL
shares): spouse 0.496 / 0.420, daughter 0.253 / 0.322, son 0.104 / 0.165, daughter-in-law 0.036 / 0.052, other
relative 0.161 / 0.185, non-relative 0.265 / 0.197 (N = 2,138 / 3,294). No causal estimate on family care.

**6. Mexican / Latin American separation.** **None.** No origin-specific treatment, no origin-split estimate, no
Rotemberg decomposition of which country groups identify the effect, and no origin composition of the direct-care
workforce (App. Fig. 2 gives foreign-born share by occupation, not origin). Mexico appears only as one of 39
base-share groups — Figure 3 Panel A shows it concentrated *"in CZs along the U.S.-Mexico border"* — and implicitly
through geography (p.13): *"the origin groups that arrived in subsequent decades are predicted to be largely
concentrated in the Southwest and West. The largest increase in the predicted share occurs in a CZ in Texas, where the
predicted share … increased from 45% in 1980 to 211% in 2000."* A predicted share above 100% is a mechanical artifact
of the construction, and it tells you the instrument's tail is Mexican-origin border CZs. The closest thing to an
origin robustness test is dropping California (T7 col 10): −0.151*** → **−0.090** (0.045), F = 9.217** — roughly 40%
of the effect and all of the instrument strength lived in the largest Mexican-destination state. The elderly
"Hispanic" subsample concerns the *elderly person's* ethnicity, not the immigrants', and is far too imprecise to use.

## Files covered / skipped

Read in full: all 58 pages via `pdftotext -layout` (1,957 lines) — body pp.3–30, references pp.31–33, Figures 1–5 and
Appendix Figures 1–2 pp.34–42, Tables 1–8 through PDF page 50, Appendix Tables 1–8 on pages 51–58. Table 8
re-extracted with `-raw` (page 50) to check a malformed SE. All figures are raster; their axes and notes were read but
**no number above is taken from a figure**. Nothing skipped. Not obtained: the published *RoIE* PDF (paywalled;
abstract compared via Wiley/RePEc/NBER "Published Versions" — identical headline numbers). 1 web search used. Cache:
`_cache/butcher_moran_watson_w29520.{pdf,txt}`.
