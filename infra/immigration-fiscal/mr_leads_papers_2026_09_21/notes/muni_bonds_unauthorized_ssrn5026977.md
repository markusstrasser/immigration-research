claude-opus-5[1m]

**Verdict:** A finance working paper asking a useful question — does local fiscal strain from unauthorized arrivals show up in the price of municipal debt? —
answered by regressing bond spreads and local-government accounts on *quintiles of a push-predicted shift-share index*. Evidence level: **contested / weak-causal**.
The unconditional yield effect is a null (Table IV); every headline runs through interactions with a non-standard "structurally tight" indicator and a Center for
Immigration Studies sanctuary flag. Shares are lagged one year and time-varying, not a fixed base year, so the Jaeger–Ruist–Stuhler critique the authors cite applies
directly and is never addressed; no first-stage F, Rotemberg weights, AKM/BHJ exposure-robust SEs, pre-trends or placebos appear anywhere. The fiscal result is
weaker than the abstract says: **no total-expenditure outcome is ever estimated**, so "spending rises, revenue doesn't" compares a few significant category
coefficients (+2.0% education, +10.3% welfare cash assistance, +12.7% general construction at Q5) against an insignificant total-revenue coefficient whose 2-year 95%
CI (≈ −1.8% to +2.2%) contains every expenditure effect reported. **Transfer caveat: identifying variation is a recent-arrival NTA flow over 2010–2023 dominated by
the post-2021 Venezuela/Haiti/Nicaragua/West-Africa surge, measured only against *local* accounts (state issuers, special districts and the federal side all absent).
It says nothing about a settled, largely US-born G2/G3+ Mexican-origin population, and the paper runs no origin-specific estimate despite promising one.**

## Citation and version

Jess Cornaggia (Penn State), Kimberly J. Cornaggia (Penn State), Ryan D. Israelsen (Michigan State, corresponding). "Unauthorized Immigration and Local Government
Finances." Working paper, **January 2025**, 69 pp (body 1–27, refs 27–36, tables 37–62, Internet Appendix 63–66). JEL H71, H74, J15, J61, G12, R23, H75.

- SSRN abstract 5026977 (posted Oct 2024; MR write-up 2024-11-30). **SSRN returned HTTP 403 on both the abstract page and `Delivery.cfm`**; the PDF read here is the
  author copy via Israelsen's site → Dropbox, cached at `_cache/muni_bonds_unauthorized_ssrn5026977.pdf`. **Version discrepancy:** the author page labels the entry
  "September 2025", but the served file has a January 2025 title page and CreationDate 2025-01-26; [UNVERIFIED] whether a real Sept-2025 revision exists.
- **Estimates unchanged Jan → Jul 2025.** The Brookings Municipal Finance Conference deck (2025-07-22, cached as `_cache/brookings_slides.pdf`) reproduces Table IV
  Panel A verbatim: "Pred. imm. quint. 2 0.0187 0.0274* 0.0113 0.0213 0.0274 0.0172 0.0113 0.0321 -0.0166". The deck also states TRAC coverage "1991–2025", which the
  paper never gives. No published version; *Management Science* (10.1287/mnsc.2023.02674) cites it as a Penn State WP.

## Question, data, sample

**Immigration:** Syracuse TRAC **Notice to Appear (NTA)** records — country of origin, state/county, time since entry, filing year-month; affirmative asylum seekers
at ports of entry excluded (fn. 4). **Shares:** ACS 5-year 2009–2022, county × country of birth. **Bonds:** Mergent + S&P IPREO iDeal + MSRB EMMA, new issues
**2010–2023**; state issuers and multi-county issuers (mostly special districts) dropped; issuer→county via IPREO **with OpenAI GPT-3.5 Turbo queried to fill missing
county names** (p. 11); remainder "mostly counties, cities, and school districts". **Treasuries:** Bloomberg/Refinitiv strips, interpolated zero-coupon curve,
duration-matched → spread. **Local finance:** Government Finance Database (Willamette standardization of the Census of Governments); the Census covers all units only
in years ending 2 or 7, so **off-year values for small issuers are linearly interpolated**, then aggregated to county. **Labor:** BLS county monthly. **Sanctuary:**
CIS map — county flagged if the state, the county, *or any city in it* is designated; 545 counties by end of sample. **Push factors:** World Bank death rate, GDP
growth, inflation, labor force participation, political stability percentile. Samples: bond issues N = 1,035,486 (Panel I.A) but **1,034,693 in every regression, 793
lost unexplained**; employment county-month N = 32,164 (Panel I.B) but **25,733 in Table VII**; local finance county-year 25,090.

## Identification

Two stages, but **the main specifications are not 2SLS** — the index enters directly as quintile dummies.

1. **Push model** (Table III, p. 43): log country-year immigration on World Bank push factors, top-20 origins (">93% of total unauthorized immigration"). Preferred
   col 7 = 3-year trailing averages, country FE, **no year FE**, adj. R² 0.70. The list names only **18** countries while claiming twenty, misspells Colombia, and says
   "Data are from the World Bank" though the dependent variable is TRAC.
2. **Shift-share**, eq. (2) p. 17: `Predicted imm_{j,t} = Σ_i Push_imm_{i,t} × FBshare_{i,j,t−1}`, divided by county population, cut into **within-month quintiles**
   ("This within-month design holds constant U.S. immigration enforcement efforts"). **Shares are `t−1` and rolling, not a fixed base year.**

**First-stage F: never reported.** The only validation is Table II (p. 42): actual NTA counts on the shift-share prediction, **0.9143 (SE 0.0100), R² 0.8699, N
54,128** county-year-months, implied t ≈ 91. But Table II validates **equation (1)** (shares × *actual* country NTA totals); Tables IV–IX use **equation (2)**
(shares × *push-predicted* totals). **No validation of equation (2) against actual immigration is reported**, so the object carrying the results is never shown to
track real flows, in levels or logs.

**Shift-share diagnostics performed: none.** One paragraph (p. 15) cites Goldsmith-Pinkham–Sorkin–Swift (2020), Jaeger–Ruist–Stuhler (2018) — "highlight the
importance of accounting for dynamic adjustments when using shift-share instruments in immigration research" — and Borusyak–Hull–Jaravel (2022), then nothing
follows: no Rotemberg weights, share-balance table, exposure-robust SEs, JRS lagged-instrument correction, pre-trend, placebo or leave-one-country-out. SEs
county-clustered only; **no robustness section and no appendix tables** (the Internet Appendix is a TRAC screenshot and three share maps). FE labels are
inconsistent: Table IV says "Issuer FE", Tables V–VI say "County FE" while their notes say "issuer and year-month fixed effects".

## Main estimates

Spreads in **percentage points** (mean spread 0.166 pp = 16.6 bp); ×100 for bp. Treatment is always **quintile of predicted immigration vs. quintile 1**.

| Outcome | Estimate | SE | Units | Table/page |
|---|---|---|---|---|
| Spread, all issuers/all bonds, Q5 (no interaction) | 0.0137 | 0.0165 | pp | IV.A, p. 44 |
| Spread, city/all, Q5 (no interaction) | 0.0334* | 0.0202 | pp | IV.A, p. 44 |
| Spread, continuous measure, county GO | 27.94*** | 7.295 | pp per unit rate | IV.B, p. 46 |
| Spread, all/all, Q5, **non-tight base** | 0.0394** | 0.0177 | pp (3.94 bp) | V.A, p. 48 |
| Spread, city/REV, Q5, non-tight base | 0.100*** | 0.0381 | pp (10.0 bp) | V.A, p. 48 |
| Tight × Q5, all/all | −0.0961*** | 0.0237 | pp | V.A, p. 48 |
| **Net in tight markets, all/all, Q5** | **−0.0567**\*\* | 0.0238 | pp (−5.67 bp) | V.B, p. 49 |
| Sanctuary base, all/all | −0.0950** | 0.0480 | pp | VI.A, p. 51 |
| **Net in sanctuary, city/GO, Q5** | **0.253**\*\*\* | 0.0751 | pp (25.3 bp) | VI.B, p. 52 |
| Unemployment t+1 (2-yr avg), Q5 base | 0.0853** | 0.0394 | **pp** | VII.A, p. 54 |
| Unemployment, net in tight / sanctuary, Q5 | 0.291*** / 0.656*** | 0.0500 / 0.108 | pp | VII.B, p. 55 |
| Labor force per capita, net in tight, Q5 | −0.127 | 0.768 | pp | VII.B, p. 55 |
| Structurally tight t+1, net in tight, Q5 | −0.0827*** | 0.0219 | prob. | VII.B, p. 55 |

Verbatim rows — V.A p. 48: "Pred. imm. quint. 5 0.0394** 0.0418* 0.0419 0.0693*** 0.0575** 0.100*** 0.0230 0.0465 -0.00874" / "Tight × PI quint. 5 -0.0961***
-0.0862*** -0.0862** -0.130*** -0.109*** -0.148** -0.0663* -0.0293 -0.125*". V.B p. 49: "PI quint. 5 + Tight × PI quint. 5 -0.0567** -0.0444 -0.0442 -0.0605**
-0.0516 -0.0477 -0.0433 0.0172 -0.134*". VI.B p. 52: "PI quint. 5 + Sanctuary × PI quint. 5 0.0857* 0.1000 0.127** 0.179*** 0.253*** 0.0385 0.0970 0.122 0.126".
VII.B p. 55: "PI quint. 5 + Category × PI quint. 5 0.291*** 0.656*** -0.127 -0.466 -0.0827*** -0.0617*".

**Revenues (Table VIII, p. 56)**, log outcomes, county-year, Q5, 1-yr / 2-yr: total revenue 0.007 (0.010) / 0.002 (0.010); total taxes 0.000 (0.011) / −0.001
(0.011); property tax 0.003 (0.011) / −0.001 (0.011); **total selective sales tax −0.101** (0.049) / **−0.124*** (0.047)**. Verbatim: "Pred. imm. quint. 5 0.007
0.002 0.000 -0.001 0.003 -0.001 -0.101** -0.124***". R² 0.935–0.996. **Intergovernmental transfers received are not an outcome.**

**Expenditures (Table IX, pp. 58–62), Q5, 1-yr / 2-yr:**

| Panel / outcome | 1-yr | 2-yr |
|---|---|---|
| IX.A Public welf cash asst | 0.103* (0.056) | 0.037 (0.046) |
| IX.A Welf categ total exp (SSI/TANF/Medicaid) | 0.103** (0.049) | 0.042 (0.045) |
| IX.A Welf categ ig to state | 0.038*** (0.015) | 0.008** (0.004) |
| IX.B (headers unreliable, see below) | 0.131** / 0.112** / 0.135** | 0.134** / 0.119** / 0.058 |
| IX.C General construction | 0.127** (0.057) | 0.090* (0.051) |
| IX.C Gen capital outlay other | 0.088** (0.043) | **−0.026** (0.034) |
| IX.D Total educ total exp | 0.020 (0.016) | 0.020** (0.010) |
| IX.D Total educ direct / current exp | 0.016 / 0.012 | 0.023** / 0.020** |
| IX.E Police prot ig to state | 0.023* (0.014) | 0.015 (0.011) |
| IX.E Police prot cap outlay | 0.146* (0.075) | 0.109 (0.069) |

Verbatim — IX.A: "Pred. imm. quint. 5 0.103* 0.037 0.103** 0.042 0.095* 0.042 0.038*** 0.008**"; IX.C: "0.127** 0.090* 0.088** -0.026 0.041 0.048* 0.060** 0.059*
0.074 0.099*"; IX.D: "0.020 0.020** 0.016 0.023** 0.012 0.020**"; IX.E: "0.023* 0.015 0.146* 0.109".

**Defect — Table IX Panel B column headers are wrong.** Panel B is titled "Welfare Institutions Expenditures and Federal Cash Assistance", but its three outcome
labels are verbatim copies of Panel A's first three ("Public welf cash asst / Welf categ total exp / Welf categ cash assist"). Coefficients and R² differ from Panel
A, so different regressions were run; only the headers were copy-pasted (confirmed by re-extracting PDF pages 61–62 with `pdftotext -raw`). From Table I the intended
outcomes are presumably `Welfare ins total exp` / `Welfare ins current exp` / a federal categorical series, but **which column is which cannot be determined** — do
not cite Panel B numbers by outcome name.

**Units ambiguity.** Table VIII's note says "Panel A uses logged values as dependent variables. Panel B uses per capita values" — Table VIII **has no panels**. Table
IX's note says "Panels A and B use logged values... Panel C uses per capita values" and is silent on D and E. Read literally, Panel IX.C's 0.127 would be **12.7
cents per capita**; logs are the only reading consistent with the text and magnitudes. **Treat all Table VIII/IX coefficients as logs [INFERENCE]; the per-capita
note is stale boilerplate.**

## Heterogeneity and mechanisms

"Structurally tight" = 2-yr trailing average unemployment **and** 2-yr trailing average labor force-per-capita **both below sample means** (fn. 8: "The mean labor
force per capita in our sample is 46.8%. The mean unemployment rate is 5.6%" — employment-sample means, not the bond sample's 4.878 / 51.179). 21.6% of bond and
28.0% of employment observations qualify. Motivated as a proxy for Barnichon–Shapiro's V–U ratio given no county vacancy data. Note *low* participation
conventionally signals a weak or elderly labor market; the authors raise the retiree/disability confound and answer it only with fixed effects ("To the extent that
the presence of, for example, retirees or disabled persons are stable through time, these alternative characteristics will not explain our results", p. 20).

The mechanism chapter is least consistent. The introduction claims that in tight markets immigration "predicts future increases in labor force participation and
reduced labor market tightness" (p. 3). The tightness half holds (Tight × Q5 = −0.147***, net −0.0827***). **The participation half does not**: Table VII col 5 Tight
× Q5 = 0.780 (SE 0.491), insignificant, and the *summed* effect is **−0.127 (SE 0.768)** — wrong sign, insignificant; only Q2–Q4 interactions reach 10%. Relatedly,
unemployment rises most where yields *fall*: +0.291 pp net in tight counties (spreads −5.67 bp) vs +0.656 pp in sanctuary counties (spreads +8.57 bp), and the paper
reads the same sign as "alleviating tightness" in one case and "fiscal strain" in the other. The text also writes "0.16 percent" and "0.615%" for percentage-point
moves in an unemployment rate whose mean is 5.553 — a ~12% relative rise at Q5 in sanctuary counties.

## Robustness and what the authors concede

Conceded: the positive GDP-growth push coefficient is "somewhat counterintuitive" (explained via Bertoli–Fernandez-Huertas–Ortega 2013 emigration-cost liquidity);
tightness may proxy for retirees or disability; the sales-tax decline is speculated to reflect "increased cash transactions for some reason". One robustness claim is
asserted with no table: "the results that follow are robust using any specification from Table III" (p. 17). Not conceded, and absent: **any limitations paragraph**
— the conclusion moves from findings straight to policy implications and future research.

## Threats the authors do not address

- [INFERENCE] **Reverse causality through enforcement, not migration.** NTA *filings* are a DHS enforcement output; a county with more ICE/DHS activity generates
  more NTAs at the same true immigrant stock. Within-month quintiles hold *national* enforcement fixed, not local intensity — plausibly correlated with sanctuary
  status, the paper's own moderator.
- [INFERENCE] **The sanctuary result may be an artifact of the flag.** A county is sanctuary if the *state* is, so entire states (CA, IL, NJ…) flip at once and 33.2%
  of bond observations carry it; the interaction then partly identifies off state-level fiscal shocks coinciding with state sanctuary laws, absorbed by neither issuer
  nor year-month FE.
- [INFERENCE] **Interpolated off-year finance data** mechanically smooths the dependent variable toward its own trend, biasing year-over-year effects toward zero — a
  live alternative explanation for the revenue nulls.
- [INFERENCE] **No total-expenditure outcome exists**, so the budget-constraint claim is untested. Local budgets balance; if categories rise and revenue does not,
  something must fall. The one category that does fall (gen capital outlay other, 2-yr −0.026) goes unremarked.
- [INFERENCE] **Significance-vs-nonsignificance error in the headline.** Education 2-yr Q5 = 0.020 (SE 0.010, CI ≈ [0.000, 0.040]) is called an effect; total revenue
  2-yr Q5 = 0.002 (SE 0.010, CI ≈ [−0.018, 0.022]) is called no effect. The CIs overlap almost entirely, and revenue's base ($572.7M) is 2.4× education's ($240.9M), so
  revenue's CI upper bound (+2.2% ≈ +$12.6M) exceeds the education point estimate (+$4.8M).
- [INFERENCE] ~50 quintile × outcome × horizon coefficients in Tables VIII–IX with **no multiple-testing correction**, most Q5 results at 5–10%; and **GPT-3.5 Turbo
  assigns counties to bond issuers** with no reported accuracy audit, while county assignment defines both treatment and fixed effects.

## Answers to the repo's questions

**1. Measure.** TRAC **Notice to Appear** records — immigration-court charging documents, not border encounters and not a population stock. The regressor is a
**12-month flow**, push-predicted and share-allocated, divided by county population — **a rate, not a count** — entered as **within-month quintiles**. Geography is
the **county**; issuers mapped to one county, multi-county issuers dropped. Bonds 2010–2023; ACS shares 2009–2022; the TRAC window is never stated (the Brookings
deck says 1991–2025). **A "one-unit" change is one quintile step, never converted to people.** One SD of the underlying rate is **0.060 pp of county population**
(bond sample; mean 0.044%, P25 0.009%, P50 0.024%, P75 0.055%) and **0.053 pp** in the employment sample (mean 0.022%). For a 100,000-person county that is ~44
predicted arrivals/yr at the mean, ~60 at +1 SD [INFERENCE on scaling]. **Panel I.C reports no predicted-immigration statistics at all**, so the treatment
distribution in the sample producing every fiscal result is unknown.

**2. Expenditures by function.** See the Table IX block above: county-year, **log outcomes of totals, not per capita** [INFERENCE], Q5 vs Q1, county + year FE, N =
25,090, county-clustered. Welfare and police effects are 1-year and fade by year 2; education effects appear *only* at 2 years; general construction persists (+12.7%
→ +9.0%). **No total-expenditure outcome is estimated.**

**3. Revenues.** See the Table VIII block: total revenue, total taxes and property tax are all flat at both horizons; only selective sales tax moves (−10.1%,
−12.4%). **Intergovernmental transfers received are not an outcome** — the most important omission for the repo, since a local government absorbing newcomers is
substantially funded by state and federal pass-through, and the paper's only transfer variables run *outward* (local→state). **"Not offset by higher tax revenues" is
an imprecise zero**: the 2-year total-revenue 95% CI spans ≈ −1.8% to +2.2% of a $572.7M mean, i.e. −$10.3M to +$12.6M, which brackets every expenditure effect.

**4. Implied spending per additional unauthorized resident.** **The authors never compute it, and the paper does not contain enough to compute it.** Available —
Panel I.C means (county-year, N = 25,090): total revenue 572,656; total taxes 231,406; property tax 166,943; total education expenditure 240,920; general
construction 47,333; public welfare cash assistance 3,237; welfare categorical total 3,599; police capital outlay 1,192. **Units are unstated in the table; the
Government Finance Database reports thousands of dollars, so read these as $572.7M / $240.9M / $47.3M / $3.24M [INFERENCE].** Missing, each piece individually fatal:
(a) the predicted-immigration distribution in the finance sample, so the Q5−Q1 gap in rate terms is unknown (the bond sample's P75−P25 = 0.046 pp is a different,
bond-issue-weighted universe); (b) any population mean for the finance sample — Panel I.C has no population row, and Panel I.A's `Population` mean of 12.679 is
ln(persons) ≈ 321,600 despite the note claiming "millions of people", so the paper's own units statement is wrong there too; (c) confirmation that Table VIII/IX
outcomes are logs of totals; (d) most fundamentally, **the treatment is a push-predicted NTA-derived index never calibrated in levels to actual unauthorized
arrivals** — Table II's 0.9143 slope validates equation (1) against NTA counts, not equation (2), and NTA filings are themselves a selected subset of arrivals. Any
dollars-per-immigrant figure built on this chain is an artifact of the calibration assumption, not a finding. The defensible statement is relative: at the top
immigration quintile welfare cash assistance runs ~10% higher and education ~2% higher than at the bottom, against total revenue statistically flat.

**5. Yields.** Spread = offer yield − duration-matched zero-coupon treasury; mean 16.6 bp, SD 69.2 bp. Bond sample: new issues 2010–2023, **59.2% GO / 40.8%
revenue-and-other**, mean duration 7.888 yrs (P25 4.24, P75 11.23), 48.1% callable, 19.8% insured, 46.2% refunding, 52.8% competitive; N = 1,034,693 (612,428 GO /
422,122 REV; city 560,323, county 250,616). Top vs bottom quintile (Q5 vs Q1), all issuers/all bonds: **+3.94 bp** in non-tight non-sanctuary counties, **−5.67 bp net
in structurally tight counties**, **+8.57 bp net in sanctuary counties** (10%). City issuers carry it: +6.93 bp base (GO +5.75, REV +10.0), −6.05 bp net in tight,
**+17.9 bp net in sanctuary (city/all), +25.3 bp (city/GO)**. County issuers: nothing significant in any cut. "Structurally tight" defined above. **Caveat: the
unconditional Table IV shows essentially no yield effect** (all-issuer Q5 = 0.0137, SE 0.0165) — every headline is interaction-conditional; and the one strong
continuous result, county GO +27.94***, has the *opposite* sign to the county-GO quintile estimates (all insignificant, 0.0225–0.0465) and is never reconciled.

**6. Instrument.** See Identification. Base year of shares: **none — shares are lagged one calendar year and roll forward** with each ACS 5-year release.
**First-stage F: not reported anywhere**; the design is reduced-form, so there is no first stage in the estimating equations, and the nearest diagnostic (Table II)
validates the wrong equation. Shift-share validity diagnostics: **none performed**.

**7. Mexican or Central American origin.** **Nothing.** No origin- or region-specific estimate appears in any table. The only origin-level material is Figure A2
(share maps for Mexico, Haiti, Nicaragua) and a §3.1 passage promising exactly the analysis that never arrives: "This widespread pattern suggests that Mexican
immigration may have diffuse effects on local government finances... We predict variation in effects on local government finances based on the predominant source
countries in each area" (pp. 10–11). Composition cuts against transfer: the 2010–2023 NTA flow is heavily post-2021 and heavily Venezuelan/Haitian/Nicaraguan/West
African (Guinea, Mauritania and Senegal all make the top-20 list), so the identifying variation is largely *not* Mexican.

## Files covered / skipped

Read in full from `_cache/muni_bonds_unauthorized_ssrn5026977.txt` (2,413 lines, 69 PDF pages): title and abstract, Introduction (1–4), Related Literature (4–9),
Data (9–13), Methods and Instrument (13–17), Results (18–26), Conclusion (26–27), all of Tables I–IX (37–62), Internet Appendix (63–66). Re-extracted PDF pages 61–62
with `pdftotext -f N -l N -raw` to confirm the Table IX Panel B header defect. Skipped: the reference list (27–36) beyond spot checks, and Figures 1–5 / A1–A2,
images carrying no numbers the text does not state. SSRN routes tried, both HTTP 403: `papers.cfm?abstract_id=5026977` and `Delivery.cfm/5026977.pdf`; obtained
instead from the corresponding author's page. `_cache/brookings_slides.pdf` (2025-07-22, 21 pp) was used only for the version check.
