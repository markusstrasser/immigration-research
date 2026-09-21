claude-opus-5[1m]

**Verdict:** Credible IV evidence that growth in the local working-age foreign-born **stock** raises the local health-care
workforce (+173 workers of any origin, +142 foreign-born per 1,000 immigrants in the average state-MSA) and lowers annual
mortality in a fixed 2008 cohort of Medicare beneficiaries 65+ (−9.8 deaths per 1,000 immigrants, −0.148% off a 5.6% base),
with reduced skilled-nursing-facility use (−17.3 users per 1,000) as the named mechanism. Evidence level: contested-to-good
causal. The design is clean on elder mobility (2008 locations fixed, static population) and passes a demographic balance test
plus a Goldsmith-Pinkham–Sorkin–Swift decomposition, but first-stage F is only 21.2, inference is plain state-MSA clustering
rather than Adão–Kolesár–Morales shift-share SEs, and Jaeger–Ruist–Stuhler is never mentioned. **The caveat that governs
transfer to the Mexican-origin population: the effect is identified entirely off origins with high health-occupation
propensity, and the paper itself reports 14% of Philippine immigrants versus 1.2% of Mexican immigrants working as an
aide/nurse/doctor (p.16).** Africa, India and the West Indies carry 68% of the absolute Rotemberg weight; Mexico is not in the
top five. The paper's own placebo — the same instrument weighted by *non*-health-care work propensity — yields an
insignificant, three-times-smaller mortality effect (−0.00252, SE 0.00370) that flips wrong-signed when both instruments are
entered together. That placebo column, not the headline, is the estimate that transfers to a Mexican-origin inflow.

## Citation and version
David C. Grabowski (Harvard Medical School), Jonathan Gruber (MIT, NBER), Brian E. McGarry (Rochester, NBER), "Is Immigration
Good for Health? The Effect of Immigration on Older Adult Mortality in the United States," NBER WP 34791, February 2026, JEL
I18/J61. 49 PDF pages: body pp.1–27, references pp.28–32, Tables 1–7 pp.33–39, Figures 1–4 pp.40–43, Appendix pp.44–48. NIA
grant R01AG070040. Not peer-reviewed; no later version. The predecessor NBER w30960 (Feb 2023) is published as Grabowski,
Gruber & McGarry (2025), *American Journal of Health Economics*, doi:10.1086/737645 (ref. list p.30) — a different study, not
a revision (Q7).

## Question, data, sample
- Immigration/labor supply: **ACS 2000–2019** microdata via IPUMS, ~70 birthplace regions, respondent weights. Ends 2019 "to
  avoid the confounding impacts of the COVID-19 pandemic" (p.12).
- Health outcomes: **Medicare 2008–2019** — Master Beneficiary Summary File (demographics, death dates), MedPAR (100% of TM
  and ~90% of MA hospital stays), Minimum Data Set (all certified nursing-home stays), OASIS (all Medicare home-health
  episodes), chosen so use measures are not biased by TM↔MA switching (pp.12–13).
- Geography: **276 state-MSAs**, split at state lines because "states may vary along a number of dimensions that could affect
  older adults' health including Medicaid eligibility" (pp.11–12). 4,020 state-MSA-year cells in workforce regressions.
- Sample (p.18): "18,017,453 unique Medicare beneficiaries aged 65 and older residing in 276 state-MSAs. The sample reflects
  170,681,480 beneficiary years. Across all study years, the mean annual mortality rate is 5.6%." TM-only subsample
  112,012,759 beneficiary-years (~65%); spending subsample 22,417,726.

## Identification
Card (2001) shift-share **re-weighted by health-occupation propensity**. Eq. 2 (p.16): `Î_m,t = Σ_e (S_t,e × I_m,e,2005) ×
W_e,2005`, with `S_t,e` the national ethnicity-*e* stock in *t* relative to 2005, `I_m,e,2005` the 2005 local stock, and
`W_e,2005` the ethnicity's 2005 share working as aide/nurse/doctor divided by the all-immigrant share. Aides = nursing,
psychiatric, home health, personal care aides (fn.6); nurses = LPN+RN (fn.7); doctors = PAs, pharmacists, physicians and
surgeons, other diagnosing/treating practitioners (fn.8).
- **First stage (Table 1, p.33):** 0.907\*\*\* (0.197), Obs 4,020, endogenous-variable mean 1.114, **F = 21.17**.
- **Elder-mobility fix (p.17):** "we use a sample of elders already enrolled in Medicare in 2008, and follow them for the next
  decade. We hold their location fixed at their 2008 location even if they move." Motivated by a real first-order problem:
  "a one unit increase in the number of immigrants per 65 and older population results in 0.571 (se=0.122) additional Medicare
  beneficiaries… 1000 additional immigrants increases the Medicare 65 and older population in an MSA by 0.5%" (fn.9).
- **Pre-trends:** reduced-form distributed-lag event studies (Schmidheiny–Siegloch), leads/lags t−3…t+3, cumulated and
  normalized at t=−1 (Eq. 3, p.16). Figures 1–4, A1.
- **Balance placebo (Table A2, p.46):** instrument vs. *predicted* mortality from age/sex/race/Medicaid = **0.0000365
  (0.000271)**, against −0.00921\*\*\* (0.00152) for actual mortality.
- **Shift-share diagnostics:** GPSS Rotemberg decomposition (A3) and a positive/negative-weight split (A5).
  **Borusyak–Hull–Jaravel, Adão–Kolesár–Morales and Jaeger–Ruist–Stuhler are never cited or implemented.** SEs cluster on
  state-MSA only.

## Main estimates
Paper's conversion: "per 1,000 immigrants" = coefficient × 1,000 (staffing) or × ~1,290 (beneficiary-level outcomes — the
ratio of the sample-average 65+ population to the fixed 2005 denominator). Bracketed CIs are mine, ±1.96·SE on that scale.

| Outcome | Estimate (SE) | per 1,000 immigrants | % of mean | Table/page | Verbatim |
|---|---|---|---|---|---|
| Total health workers, 2SLS | 0.174\*\*\* (0.0422) | +173.5 [+91, +256] | +0.402% | T2 Panel B c1, p.34 | "an additional 1,000 immigrants result in an additional 173 health care workers, representing a 0.4% increase relative to the sample mean" (p.18) |
| Foreign-born health workers | 0.143\*\*\* (0.0208) | +142.7 [+102, +183] | +1.609% | T2B c2 | "an additional 1,000 immigrants result in 142 additional foreign workers, or a 1.6% increase" (p.18) |
| **Domestic health workers** | **0.0436 (0.0489)** | **+43.6 [−52, +139]** | +0.127% | T2B c3 | "We find no significant change in the number of domestic health care workers, suggesting that immigrants do not crowd out native health care workers" (pp.18–19) |
| Total health workers, OLS | 0.121\*\*\* (0.0225) | +120.6 | +0.279% | T2 Panel A c1 | "1,000 additional immigrants (a 1.1% increase in the size of the immigrant population in the average state-MSA) result in 120 additional health care workers" (p.18) |
| Aides / nurses / doctors-APPs, any origin | 0.0290\*\* (0.0136) / 0.0498\*\*\* (0.0158) / 0.0196\*\*\* (0.00389) | +28.96 / +49.85 / +19.65 | +0.293 / +0.457 / +0.488% | T3 c1–c3, p.35 | "an increase of 1,000 immigrants results in an additional 28 aides (0.3%), 49 nurses (0.5%) and 19 doctors (0.5%) of any origin, and 33 aides (1.1%), 32 nurses (1.6%) and 13 doctors (1.2%) of foreign origin" (p.19) |
| Foreign aides / nurses / doctors | 0.0331\*\*\* (0.00896) / 0.0328\*\*\* (0.00709) / 0.0134\*\*\* (0.00203) | +33.12 / +32.80 / +13.44 | +1.121 / +1.604 / +1.173% | T3 c4–c6 | ditto |
| **Domestic aides / nurses** | **−0.00487 (0.0104) / 0.0139 (0.0167)** | **−4.87 [−25.2, +15.5] / +13.92 [−18.8, +46.5]** | −0.071 / +0.157% | T3 c7–c8 | table rows, no text |
| Domestic doctors | 0.00649\*\* (0.00296) | +6.49 [+0.7, +12.3] | +0.226% | T3 c9 | "an additional 1,000 immigrants result in 6 domestic physicians (0.2%). This crowd-in effect may reflect health systems' ability to expand capacity" (p.19) |
| Non-aide/nurse/doctor health workers: total / foreign / domestic | 0.078\*\*\* (0.0172) / 0.0455\*\*\* (0.00766) / 0.0298 (0.0223) | +78.4 / +45.5 / +29.8 | +0.43 / +1.64 / +0.19% | T A1, p.45 | table rows |
| **Mortality, 2SLS** | **−0.00761\*\*\* (0.00208)** | **−9.82 deaths [−15.1, −4.6]** | −0.148% | T4 c2, p.36 | "each additional 1,000 immigrants result in 9.8 fewer deaths in the average sample MSA, a 0.15% reduction relative to the sample mean" (p.20) |
| Mortality, OLS | −0.00154\* (0.00060) | −1.94 | −0.029% | T4 c1 | "1,000 additional immigrants result in 0.03% decline in mortality" (p.20) |
| **Mortality, NON-health-weighted instrument** | **−0.00252 (0.00370)** | **−3.25 [−12.6, +6.1]** | −0.049% | T4 c3 | "This instrument yields results that are much smaller and insignificant – but not significantly different from the weighted estimate" (pp.20–21) |
| Mortality, both instruments (health / non-health) | −0.0105\*\*\* (0.00338) / +0.00836 (0.00581) | −13.58 | −0.204% | T4 c4 | "a stronger effect from our health care weighted measure and a wrong-signed and insignigificant effect for the unweighted measure" (p.21) |
| **SNF use (any, in year)** | **−0.0134\*\*\* (0.00476)** | **−17.33 users [−29.3, −5.3]** | −0.215% | T5 c1, p.37 | "1,000 additional immigrants result in 17.3 fewer older adults using a SNF for any duration in the typical MSA. This represents a 0.22% reduction relative to the sample mean" (p.21) |
| Hospital use / home health use (any) | 0.00104 (0.00616) / −0.00513 (0.0109) | +1.35 / −6.62 | +0.006 / −0.055% | T5 c2–c3 | "we find no significant effects on the rates of hospitalizations and home health care use" (p.22) |

**Table 5's row labels are shifted in the source PDF** — "Sample Average" carries the per-1,000 effects and "Percent Change"
repeats the coefficients. I re-extracted page 38 with `pdftotext -f 38 -l 38 -raw`; the defect is in the PDF, not the
conversion. The mapping above follows the body text (17.3 fewer SNF users, 0.22%), which is internally consistent.

**TM-only replication (Table 6, p.38; Obs 112,012,759):** mortality −0.00706\*\*\* (0.00228) = −9.12 deaths (−0.131%); SNF
−0.0121\*\*\* (0.00446) = −15.62 (−0.188%); hospital 0.00207 (0.00759); home health −0.000716 (0.0116); ED treat-and-release
0.00126 (0.0117); outpatient 0.0248 (0.0150) = +31.95; hospice −0.00298 (0.00253) = −3.85 — the last five all insignificant.
**Spending (Table 7, p.39; Obs 22,417,726):** winsorized dollars 3207.1 (3666.0), insignificant, implying $4,138,749 per
1,000 immigrants at MSA level (+0.073%); inverse-hyperbolic-sine 0.263\*\*\* (0.0836), +0.0297%.

**Event studies** (raster figures; rendered at 110 dpi with `pdftoppm` and read visually, so coordinates are approximate).
Fig. 1 staffing: leads −0.015, −0.055, −0.025, 0 at t=−4…−1; post −0.015, +0.047, +0.122, +0.196, with t=+2/+3 CIs excluding
zero. Fig. 2 mortality: leads +0.002, +0.0013, −0.0005, 0; post −0.0027, −0.005, −0.0101, −0.0118, all four CIs excluding
zero. Fig. 3: panel (b) nursing-home use (mean 0.066) leads −0.001, +0.0035, +0.003, 0, post −0.004, −0.013, −0.018, −0.0235;
panel (a) hospitalization (mean 0.188) dips to ≈−0.015 at t=0/+1 and returns to 0 by t=+3 with wide CIs; panel (c) home care
(mean 0.098) rises from −0.027 at t=−4 to 0 at t=−1, then falls to −0.046 at t=+3 (CI touching 0). Fig. 4: raw-dollar spending
flat with very wide CIs; the IHS panel rises from −0.34 at t=−4 to 0 at t=−1 and is flat after — the pre-trend the authors
themselves invoke. Fig. A1: the domestic-worker band is flat and wide (≈±0.10 in every post period); the foreign panel rises
cleanly.

## Heterogeneity and mechanisms
**No heterogeneity by immigrant education, legal status or sex, and none by beneficiary subgroup** (race, income, Medicaid,
rurality). Origin enters only through the instrument:
- **Rotemberg weights (T A3, p.47),** 73 ethnicities, total absolute weight 1.1792: Africa 0.4958 (42.0% of absolute weight),
  India 0.2336 (cum. 61.9%), West Indies 0.0723 (cum. 68.0%), Central America 0.0527 (cum. 72.4%), China 0.0517 (cum. 80.9%).
  "immigrants from Africa, India and the West Indies drive our results, accounting for 68% of the absolute weight in the
  estimator" (p.24). **Mexico is not in the top five.** Propensity weights (T A4): Philippines 3.522, Africa 2.794, West
  Indies 2.787. Mexico comparison (p.16): "we estimate, using the ACS, that 14% of immigrants from the Philippines work in one
  of these occupations compared to just 1.2% of immigrants from Mexico."
- **Positive/negative weights (T A5, p.48):** foreign health-worker staffing 0.1517 = 0.1676 positively-weighted + (−0.0158)
  negatively-weighted; foreign aide/nurse/doctor staffing 0.0965 = 0.1063 + (−0.0098). "even under treatment effect
  heterogeneity our estimates would retain a LATE-like interpretation" (pp.24–25).
- **Mechanism (p.26):** reduced SNF use, argued as aging-in-place via in-home aides plus better staffing inside nursing homes
  — the latter carried entirely by the 2025 AJHE paper, not re-estimated. Explicitly unidentified: "Further research is needed
  to isolate the mechanisms" (p.25); "Further research with data that captures the actual receipt of in-home personal care,
  which is not covered by Medicare, is needed" (p.26).
- **Policy scaling (p.25):** "the same mortality reduction could be achieved with an increase in immigrant health care workers
  of only 55,000, or a 0.03% rise in the US workforce."

## Robustness and what the authors concede
Run: demographic balance placebo (A2, passes); GPSS decomposition (A3); positive/negative weight split (A5); non-health-weighted
instrument placebo (T4 c3) and horse race (c4); event studies for every headline outcome; TM-only replication (T6).
Conceded: spending is pre-trend-driven — "Figure 4 shows evidence that pre-trends likely drive the 2SLS results for inverse
hyperbolic sine transformed spending. As such, we collectively interpret the spending results to indicate that immigration
does not meaningfully affect Medicare spending" (p.23); home-health use has pre-trends (p.22); mechanisms are unidentified
(pp.25–26); the earlier paper "did not detect significant mortality effects within the nursing home population, but our study
design may have been underpowered for this outcome" (p.27); and the placebo they most want to pass is itself underpowered —
the non-health-weighted estimate is "not significantly different from the weighted estimate" (pp.20–21).

## Threats the authors do not address
- [INFERENCE] **The abstract's "25% increase in the steady state flow" is not what fn.12 computes.** The regressor is a
  **stock** — "the annual number of immigrants age 54 or younger per 65 and older population in a state-MSA (fixed in 2005)",
  mean **1.114**, a stock-to-elderly ratio, not a flow ratio. Fn.12 applies the stock coefficient to a **one-year** flow
  increment: "A national increase of 325,000 immigrants translates to a 0.01 unit increase in the rate… We multiply this unit
  change by our 2SLS effect estimate… (ie, −0.00008). We scale this estimate by the size of the 65 and older population in
  2024 (roughly 60 million)." A permanently 25%-higher *flow* raises the steady-state *stock* by ~25%, i.e. ~0.28 units rather
  than 0.01, implying order-100,000 averted deaths under the same coefficient. The 5,000 figure is the first-year effect of one
  extra cohort, mislabeled as steady-state — conservative by roughly an order of magnitude if the stock coefficient is taken
  literally, and in any case not the estimand the abstract names.
- [INFERENCE] **Denominator mixing.** The treatment rate is normalized by the **2005** 65+ population while deaths are scaled
  by the contemporaneous (≈1.29×) or 2024 (≈1.85×) 65+ population. The bare coefficient implies −7.6 deaths per 1,000
  immigrants; −9.8 and 5,000 both embed population-growth inflation. Defensible as projection, but the headline moves with
  whichever elderly population you pick.
- [INFERENCE] **Inference is not shift-share-robust.** SEs cluster on 276 state-MSAs, but the identifying variation is 73
  ethnicity shocks × 12 years, and two origins (Africa, India) carry 62% of the absolute weight. Adão–Kolesár–Morales show
  this materially understates uncertainty; with F already only 21.2, corrected inference could land in weak-instrument
  territory and the mortality CI would widen well beyond [−15.1, −4.6].
- [INFERENCE] **Jaeger–Ruist–Stuhler is untouched.** One 2005 share vector drives 12 years of year-to-year variation,
  conflating contemporaneous and lagged responses. The growing event-study coefficients the authors read as "training and
  licensing requirements" (p.19) are exactly the pattern JRS attribute to serially correlated shocks.
- [INFERENCE] **The balance test checks demographics, not economics.** A2 predicts mortality from age/sex/race/Medicaid only.
  The plausible violation is that 2005 African/Indian settlement predicts metro income and industry growth; only the
  unemployment rate is controlled.
- [INFERENCE] **Mild same-signed pre-trends in both headline figures.** Mortality leads run +0.002 → 0 over t=−4…−1; staffing
  leads run −0.055 → 0. Small relative to post-shock slopes, but "the absence of pre-trends" (p.19) overstates flat.
- [INFERENCE] **"No crowd-out" is an imprecise zero.** Domestic health workers 95% CI [−52, +139] per 1,000 immigrants; the
  lower bound cancels 37% of the +142.7 foreign gain. Domestic aides [−25.2, +15.5] against +33.1 foreign aides — up to 76%
  offset. Only the small physician crowd-in is precise. Labor supply is headcount of people with positive hours, not FTEs or
  hours, and no wage outcome is reported, so crowd-out operating on wages or hours is invisible by design.
- [INFERENCE] **Internal arithmetic does not fully reconcile.** Foreign 142.7 + domestic 43.6 = 186.3 ≠ the reported total
  173.5. The intro's "88 new aides, nurses and doctors" of foreign origin (p.4) matches neither Table 3's 33.1+32.8+13.4 =
  79.3 nor Table A5's 96.5; "96… of any origin" vs. Table 3's 98.5. Table 2 Panel A's Sample Average row (0.467/0.268/0.199)
  contradicts Panel B's (0.467/0.0959/0.37) for the same columns and sample; 0.268 and 0.199 are the NAD and non-NAD means
  (0.107+0.118+0.0435 = 0.2685; T A1 non-NAD mean 0.199), so Panel A's row looks mislabeled. Panel B's split is the one
  consistent with the paper's own "18% of health care workers are immigrants" (0.0959/0.467 = 20.5%).
- [INFERENCE] **No dose-response on the mechanism.** The mortality effect is never shown to be larger where baseline SNF use
  or nursing-home supply is higher, nor among beneficiaries at risk of SNF admission. "Any SNF use" pools 3-day post-acute
  rehab with permanent residence — conceded (p.22) but never split.
- [INFERENCE] **Differential survival changes cohort composition.** Following a fixed 2008 cohort for 12 years means
  higher-immigration MSAs retain more (frailer) survivors, attenuating later-year mortality effects — conservative, but it
  makes the rising event-study profile harder to read as a pure dose effect.

## Answers to the repo's questions
**1. Treatment, geography, years, data; the 1,000 → 142 derivation; occupation split.** Treatment is the **stock of all
foreign-born residents aged 17–54**, per 2005 65+ population — not a flow, not education-restricted, not legal-status-restricted:
"The ACS does not gather information about respondents' legal status in the US… estimates on immigration obtained from these
data are inclusive of both the documented and undocumented populations" (p.12). Under 55 by construction "to ensure that
immigrants do not directly impact our health outcomes which we measure among those 65 and older" (p.12). 276 state-MSAs; ACS
2000–2019, Medicare 2008–2019, base year 2005. The 142 is Table 2 Panel B col 2 (0.143\*\*\*, SE 0.0208) converted as
coefficient × 1,000 — "the implied expected change in staff (in levels) from 1,000 new immigrants arriving in the average
state-MSA" (T2 note). Occupation split per 1,000 (Table 3): any origin aides +28.96, nurses +49.85, doctors/APPs +19.65;
foreign aides +33.12, nurses +32.80, doctors +13.44; native aides −4.87 (ns), nurses +13.92 (ns), doctors +6.49\*\*. RNs are
**not** separable from LPNs (fn.7) and physicians are pooled with PAs, pharmacists and other diagnosing/treating practitioners
(fn.8). Non-NAD health workers add +78.4 (T A1).

**2. Mortality: estimate, units, SE, ages; the 5,000-deaths computation.** −0.00761 (SE 0.00208), p<0.001, on a **binary
indicator of death in a calendar year** for beneficiaries **65+ as of 2008** (so 65+ ageing to 76+ by 2019), per one unit of
immigrants-per-2005-65+-population; base rate 0.056; reported as −9.821 deaths per 1,000 immigrants in the average state-MSA
(−0.148%). TM-only −0.00706 (0.00228) = −9.116. The 5,000 is fn.12, p.21: 0.01 unit × 0.00761 = 0.0000761, × 60M (2024 65+) =
4,566 → "roughly 5000"; the 25% is of the 1.3M net inflow in 2023 (Macrotrends). Propagating the SE alone gives ≈2,300–7,700
before any shift-share SE correction. See the stock-vs-flow and denominator flags above.

**3. Nursing-home use: long vs short stay, Medicaid-financed stays, staffing, quality.** One estimate only — **any SNF use in
the year** (MDS-based, administratively complete): −0.0134 (0.00476) = −17.33 users per 1,000 immigrants, −0.215% of the mean;
TM-only −0.0121 (0.00446) = −15.62; event study (Fig. 3b, mean 0.066) grows monotonically to −0.0235 by t=+3. **No
long-stay/short-stay split, no Medicaid-financed-stay analysis, no staffing ratios and no quality measures anywhere in this
paper.** Stay types are explicitly pooled: "our estimates include SNF use that is rehabilitative (i.e., short stays) rather
than exclusively focusing on long-stay residential placement in a nursing home" (p.22). All staffing and quality evidence
(pressure ulcers, restraints, hospitalizations from within nursing homes) is cited from the 2025 AJHE paper (pp.26–27), not
re-estimated. Benchmarks (pp.21–22): Huh et al. (2024) imply −0.13% institutionalized per 1,000 immigrants, Butcher et al.
(2022) imply −0.6%; this paper's −0.215% "lies between these two papers."

**4. Spending.** Only **total traditional-Medicare spending** (CMS Cost and Use file; Table 7 above). The authors discount the
significant IHS result as pre-trend-driven and conclude "immigration does not meaningfully affect Medicare spending,
suggesting that reductions in SNF spending are likely offset by increases in spending in other areas and the mechnical
increase in spending that likely results from reduced mortality" (p.23). **No Medicaid spending, no out-of-pocket spending, no
service-line decomposition, no fiscal accounting of any kind.**

**5. Crowd-out: tight zero or imprecise zero? — imprecise.** Domestic health workers 0.0436 (0.0489), 95% CI ≈ [−52, +139] per
1,000 against a foreign gain of +142.7. Domestic aides −0.00487 (0.0104), CI ≈ [−25.2, +15.5] against +33.1 foreign aides.
Domestic nurses 0.0139 (0.0167), CI ≈ [−18.8, +46.5]. Domestic non-NAD 0.0298 (0.0223). Only domestic doctors are precise:
+0.00649 (0.00296), CI ≈ [+0.7, +12.3] — a genuine but small crowd-**in**. Appendix Fig. A1 panel (a) confirms visually: the
domestic band is ≈±0.10 in every post period, wide enough to contain both complete offset and large crowd-in. "Without
evidence of crowd out" is accurate about significance and weak about economics.

**6. Heterogeneity by origin/education; Latin America and Mexico; origin shares of the foreign-born health workforce.** No
education split, no origin-stratified treatment effects. Origin enters only through the instrument: Rotemberg weights Africa
0.496, India 0.234, West Indies 0.072, **Central America 0.053**, China 0.052 (T A3, top three = 68% of absolute weight);
propensity weights Philippines 3.52, Africa 2.79, West Indies 2.79 (T A4). The decisive number for this repo is p.16: **14% of
Philippine immigrants versus 1.2% of Mexican immigrants work as an aide, nurse or doctor.** [INFERENCE] T A4's scaling implies
an all-immigrant NAD share of 14/3.522 ≈ 3.98%, so Mexico's relative propensity weight is ≈ 1.2/3.98 ≈ **0.30** — about a
twelfth of the Philippines' — and Mexico is absent from the top-five Rotemberg list despite being the largest origin group.
The paper gives **no origin shares of the foreign-born health workforce**; it reports only immigrant shares of occupations,
citing Migration Policy Institute (2023): 18% of 15M health care workers, 26% of physicians and surgeons, 40% of home health
aides, 28% of personal care aides, 21% of nurse assistants (p.8), plus "Roughly 1 in 5 frontline nursing home workers are
immigrants, nearly 1 in 3 home care workers" (p.3). The only Hispanic-specific result in this literature sits in the 2023/2025
predecessor ("particularly for immigration of Hispanic staff") — that paper, not this one, is where a Mexican-origin transfer
should start. For this paper the honest transfer is Table 4 column 3: the non-health-weighted instrument gives **−0.00252
(0.00370)**, −3.25 deaths per 1,000 [CI −12.6 to +6.1], flipping to **+0.00836 (0.00581)** when entered alongside the
health-weighted instrument.

**7. 2026 vs 2023 (abstract pages only).** w30960 (Feb 2023; published 2025, AJHE, doi:10.1086/737645) is a
**nursing-home-sector study**: "We merge a variety of data sets on immigration and nursing homes and use a shift-share
instrumental variables analysis to assess the impact of increased immigration on nursing home staffing and care quality. We
show that increased immigration significantly raises the staffing levels of nursing homes in the U.S., particularly in full
time positions. We then show that this has an associated very positive effect on patient outcomes, particularly for those who
are short stayers at nursing homes, and particularly for immigration of Hispanic staff." w34791 is a **new, population-level
study, not a revision**: the outcome is all-cause annual mortality for the whole 65+ Medicare population rather than
nursing-home residents; the unit is the state-MSA-beneficiary rather than the facility; the instrument is newly re-weighted by
health-occupation propensity; and the 2026 paper cites the earlier one as established prior work (pp.3, 10, 26–27). They share
no estimates. The 2026 paper also notes the earlier design "did not detect significant mortality effects within the nursing
home population, but our study design may have been underpowered for this outcome" (p.27), so the mortality result is
genuinely new. The Hispanic-staff heterogeneity of the 2023/2025 paper has **no counterpart** in the 2026 paper.

## Files covered / skipped
Read in full: `_cache/grabowski_gruber_mcgarry_w34791.pdf` (49 pages; 1,912-line `-layout` text) — body pp.1–27, all of Tables
1–7 (pp.33–39) and Appendix Tables A1–A5 (pp.45–48). References pp.28–32 skimmed only for the Grabowski/Butcher/Huh/Jung
entries. Figures 1–4 and A1 are raster images with no extractable data; PDF pages 41–44 and 46 rendered at 110 dpi with
`pdftoppm` and read visually, so plotted coordinates are approximate to the nearest gridline. Table 5 re-extracted with
`pdftotext -f 38 -l 38 -raw` after the row-label defect appeared under `-layout`. w30960: NBER landing-page abstract only
(`_cache/w30960_abstract.html`), per instructions; its PDF was not downloaded. No search for a published version of w34791
(Feb 2026 working paper; none expected).
