<!-- reader extraction, opus-low agent, 2026-09-22; every numeric row carries a verbatim quote re-found in the parsed corpus text with rg -F; parent spot-checked the rows cited in the memo -->
# Wilson & Zhou (2026) — The Impacts of Unauthorized Immigration on U.S. Labor and Housing Markets: New Evidence from Administrative Microdata. Federal Reserve Bank of Dallas Working Paper 2607, March 6 2026

[SOURCE: /Users/alien/Projects/corpus/doi_10_24149_wp2607/parsed.pymupdf4llm@0.3.4+cfg-99914b93/page.md — all numbers below are quoted from that parsed text]

**Verdict:** A cross-sectional shift-share IV over US commuting zones/MSAs identifies the local effect of the 2021–2024 unauthorized-immigrant worker inflow on employment (≈1-for-1), wages (negative, imprecise), house prices and rents (strongly positive), housing permits (null) and BEA government transfers (strongly negative); the design is credible for a *local relative* effect with a first stage F near 30 and passing Rotemberg/over-ID/placebo checks, but it is a single 3-year cross-section with a new, partly imputed inflow measure and cannot deliver national general-equilibrium or fiscal-account magnitudes.

## Population, period, unit

- Population: **unauthorized immigrants**, defined as "individuals who enter the U.S. without formal admission under immigration law". Main regressor is **UIWF = unauthorized immigrant worker flows** = net entries × working-age share × employment rate of recent same-origin arrivals. Working age = 16–65.
- Origin composition is dominated by 11 "high-encounter" countries: "High-Encounter countries include Mexico, Guatemala, Honduras, El Salvador, Venezuela, Colombia," "Cuba, Ecuador, Nicaragua, Haiti, and Peru." (~80% of net entries 2021–2024). **No US-born second/third generation is observed at all** — this is a flow paper, not a lineage paper.
- Periods: **boom = 2021m3–2024m3** (main); **slowdown = 2024m6–2025m6** (extension, cautioned); income outcomes 2021–2023 (and 2021–2024 in appendix).
- Unit: **commuting zone (CZ)** for QCEW employment/wages, ACS outcomes and BEA income (n = 721 CZs; 712 with BEA/ACS). **MSA** for Zillow house prices, rents and permits (n = 348 / 280 / 343). Weighted by beginning-of-period employment; SEs heteroskedasticity-robust, **clustered on state**.

## Design and identification

**(1) How the unauthorized inflow measure is built, and from what data.**

Two restricted-use individual-level administrative files obtained via TRAC (Syracuse) FOIA:
- **EOIR immigration-court records (DOJ)**: nationality, age, reported US residence ZIP, reported entry date, NTA issuance date, court decisions, custody status. This is the only source with geography.
- **CBP parole records (DHS)**: nationality, age, entry date, parole program — **no US residence location**.
Plus **DHS "got-aways"** (national only; press releases + FOIA for 2023 onward), and DHS encounters/deportations for external validation.

Entries = NTA inflows + parole entries + got-aways. Exits = court-ordered removals/voluntary departures + newly detained + (for 2025) imputed voluntary exits of parolees/got-aways using parole duration and the NTA exit rate. Net entry = entries − exits.

Imputations worth flagging:
- Entry date missing for ~30% of NTA records → NTA issuance date used as proxy.
- Got-aways have no geography and no age → apportioned to counties by origin-specific NTA shares; working-age share assumed equal to NTA+parole.
- Worker conversion: "approximately 70% are employed", estimated from ACS 2021–2024 one-year microdata on working-age immigrants arriving within the prior three years from high-encounter countries.
- Local totals are rescaled so that county sums match national and origin-specific totals.
- **Excluded by construction**: visa overstays (entries) and adjustments to LPR status (exits), on the argument that CBO projections show them roughly offsetting.

**(2) The instrument.** The parent's prior is only half right. The **preferred** instrument is NOT the public ancestry shift-share; it is a **two-way leave-out shift-share** (Card 2001 + Burchardi et al. 2019 / Terry et al. 2026):
- **Shift**: current national UIWF from origin o over the period, **excluding flows into destination d**.
- **Share**: the pre-boom distribution across destinations of immigrants **from all origins other than o**, computed from the **2015–2019 ACS five-year file**. Scaled by pre-boom (2021 ACS) employment.
- **First-stage F ≈ 28.5 (CZ employment/wages), 14.0 (MSA housing), 32.2 (ACS outcomes), 43.3 (BEA income)** — Kleibergen-Paap.
- Controls: 2015–2019 QCEW NAICS 2-digit industry employment shares; 2015–2019 ACS 5-year age shares (16–24, 25–54), education shares (≤HS, ≥BA), non-white population share.

The **public ancestry instrument is the alternative/robustness arm**: predicted 2010 ancestry A-hat(o,d) from Burchardi et al. (2019) / Terry et al. (2026), built from **decennial census pull-push interactions 1880–2000**, downloaded at county×origin level from `https://www.immigrationshock.com/ancestry-instruments` and aggregated to CZ with the 1990 county-to-CZ crosswalk. **Base year of the ancestry stock is 2010.** It is rejected as the preferred design: first-stage F = 6.80, and Mexico alone carries a Rotemberg weight of 0.674.

**Validation run**: placebo regressions on 2015m3–2018m3, 2016m3–2019m3, 2017m3–2020m3, 2018m3–2021m3 (no notable pre-trends); Rotemberg weights (no country above 0.16 in the preferred design; "Other" 0.27, and dropping it moves the estimate 0.961 → 1.042); over-ID p = 0.67.

## Headline estimates

All coefficients are the effect of **UIWF equal to 1% of initial local employment** on the percent growth of the outcome over the period. SEs in parentheses.

| Outcome | Estimate | SE (95% CI) | Table / page | Verbatim quote (≤40 words) |
|---|---|---|---|---|
| Employment, QCEW CZ, boom, IV | **0.961*** | 0.274 (0.42 to 1.50) | Table 1, p.26 | "The IV estimate is 0.96 (column 2), implying" |
| Employment, QCEW CZ, boom, OLS | 0.840*** | 0.143 | Table 1, p.26 | "UIWF 0.840 _[∗∗∗]_ 0.961 _[∗∗∗]_ -0.140 -0.933" |
| First-stage F, main employment/wage spec | 28.50 | — | Table 1, p.26 | "F Statistic 28.50 28.50" |
| Avg weekly wages, QCEW CZ, boom, IV | −0.933 (n.s.) | 0.608 (−2.12 to 0.26) | Table 1, p.26 | "(0.143) (0.274) (0.197) (0.608)" |
| Avg weekly wages, QCEW CZ, boom, OLS | −0.140 (n.s.) | 0.197 | Table 1, p.26 | "UIWF 0.840 _[∗∗∗]_ 0.961 _[∗∗∗]_ -0.140 -0.933" |
| Employment, QCEW **MSA**, boom, IV | 0.954*** | 0.252; first-stage F 14.02 | Table B1, appx p.5 | "0.784 [∗∗∗] 0.954 [∗∗∗] 0.154 -0.169" |
| Employment, **all working-age** unauthorized flows, IV | 0.650*** | 0.191 | Table B2, appx p.6 | "d ~~i~~ mm wa 0.588 _[∗∗∗]_ 0.650 _[∗∗∗]_ -0.0982 -0.625" |
| Employment, **all** unauthorized flows (all ages), IV | 0.507*** | 0.149 | Table B2, appx p.6 | "d ~~i~~ mm 0.470 _[∗∗∗]_ 0.507 _[∗∗∗]_ -0.0660 -0.501" |
| Employment, slowdown 2024m6–2025m6, IV | 1.588 (n.s.) | 1.258 | Table 3, p.34 | "UIWF 0.650 1.588 0.195 0.720" |
| Wages, slowdown, IV | 0.720 (n.s.) | 2.150; F 13.45 | Table 3, p.34 | "(0.417) (1.258) (0.531) (2.150)" |
| **House prices** (Zillow ZHVI), MSA, boom, IV | **2.189*** | 0.741 (0.74 to 3.64) | Table 6b, p.43 | "UIWF 2.189 _[∗∗∗]_ 1.438 _[∗∗∗]_ 1.229 _[∗∗]_ 1.470 _[∗∗∗]_" |
| **Rents** (Zillow ZORI, all homes), IV | **1.438*** | 0.344 | Table 6b, p.43 | "(0.741) (0.344) (0.529) (0.287)" |
| Rents, single-family, IV | 1.229** | 0.529 | Table 6b, p.43 | "F Statistic 14.02 13.64 13.25 13.92" |
| Rents, multi-family, IV | 1.470*** | 0.287 | Table 6b, p.43 | "UIWF 2.189 _[∗∗∗]_ 1.438 _[∗∗∗]_ 1.229 _[∗∗]_ 1.470 _[∗∗∗]_" |
| House prices, CoreLogic / Freddie Mac, IV | 0.632 / 1.182 (both n.s.) | 1.094 / 0.817 | Table B4, appx p.10 | "UIWF 0.632 1.182" |
| House price & rent, **self-reported ACS**, CZ, IV | −2.227 / 0.734 (n.s.) | 1.827 / 1.567 | Table B5, appx p.11 | "UIWF -2.227 -1.068 0.734 0.674" |
| New permits / initial units, total, IV | −0.208 (n.s.) | 0.213 | Table 6d, p.43 | "UIWF -0.208 -0.227 0.00998" |
| New permits, single-family / multi-family, IV | −0.227 / 0.00998 (n.s.) | 0.170 / 0.0650 | Table 6d, p.43 | "(0.213) (0.170) (0.0650)" |
| Personal income (BEA), 2021–23, IV | 0.341 (n.s.) | 0.992 | Table 7b, p.46 | "UIWF 0.341 -0.141 -0.670 -1.151 _[∗∗]_ -4.495 _[∗∗∗]_ -4.977 _[∗∗∗]_" |
| Personal income **per capita**, IV | −0.141 (n.s.) | 0.737 | Table 7b, p.46 | "(0.992) (0.737) (0.711) (0.503) (1.388) (1.324)" |
| Labor income, IV | −0.670 (n.s.) | 0.711 | Table 7b, p.46 | "UIWF 0.341 -0.141 -0.670 -1.151 _[∗∗]_ -4.495 _[∗∗∗]_ -4.977 _[∗∗∗]_" |
| **Labor income per capita**, IV | **−1.151**** | 0.503 | Table 7b, p.46 | "(0.992) (0.737) (0.711) (0.503) (1.388) (1.324)" |
| **Government transfers, total**, IV | **−4.495*** | 1.388 (−7.22 to −1.77) | Table 7b, p.46 | "UIWF 0.341 -0.141 -0.670 -1.151 _[∗∗]_ -4.495 _[∗∗∗]_ -4.977 _[∗∗∗]_" |
| **Government transfers per capita**, IV | **−4.977*** | 1.324; F 43.30 | Table 7b, p.46 | "F Statistic 43.30 43.30 43.30 43.30 43.30 43.30" |
| Government transfers, total / p.c., OLS | −1.018** / −1.509*** | 0.484 / 0.391 | Table 7a, p.46 | "UIWF 0.595 _[∗]_ 0.104 0.448 _[∗]_ -0.0431 -1.018 _[∗∗]_ -1.509 _[∗∗∗]_" |
| **Government transfers, total / p.c., 2021–2024 window, IV** | **−1.423** / −1.963**** | 0.677 / 0.803 | Table B6, appx p.12 | "UIWF 0.413 -0.127 -0.563 -1.103 _[∗∗∗]_ -1.423 _[∗∗]_ -1.963 _[∗∗]_" |
| Labor income p.c., 2021–2024 window, IV | −1.103*** | 0.330 | Table B6, appx p.12 | "(0.575) (0.398) (0.548) (0.330) (0.677) (0.803)" |
| ACS employment, CZ total, 2021–23, IV | 0.924 (n.s.) | 0.800 | Table 4a, p.38 | "UIWF 0.924 0.749 _[∗∗]_ 0.698 _[∗∗∗]_ 0.175 0.168 0.00770" |
| ACS employment, **foreign-born**, IV | 0.749** | 0.355 | Table 4a, p.38 | "(0.800) (0.355) (0.247) (0.854) (0.388) (0.533)" |
| ACS employment, **high-encounter immigrants**, IV | 0.698*** | 0.247 | Table 4a, p.38 | "UIWF 0.924 0.749 _[∗∗]_ 0.698 _[∗∗∗]_ 0.175 0.168 0.00770" |
| ACS employment, **native-born**, IV | 0.175 (n.s.) | 0.854 | Table 4a, p.38 | "(0.800) (0.355) (0.247) (0.854) (0.388) (0.533)" |
| ACS employment, low-ed / high-ed native, IV | 0.168 / 0.0077 (n.s.) | 0.388 / 0.533; F 32.18 | Table 4a, p.38 | "F Statistic 32.18 32.18" |
| ACS hourly earnings, CZ total, IV | **−0.873**** | 0.344 | Table 4b, p.38 | "UIWF -0.873 _[∗∗]_ 1.894 0.398 -0.691 _[∗]_ -0.928 -0.757 _[∗]_" |
| ACS hourly earnings, foreign-born / HE immigrants, IV | 1.894 / 0.398 (n.s.) | 1.530 / 2.465 | Table 4b, p.38 | "(0.344) (1.530) (2.465) (0.378) (0.677) (0.443)" |
| ACS hourly earnings, **native-born**, IV | −0.691* | 0.378 | Table 4b, p.38 | "UIWF -0.873 _[∗∗]_ 1.894 0.398 -0.691 _[∗]_ -0.928 -0.757 _[∗]_" |
| ACS hourly earnings, **low-ed native** | −0.928 (n.s.) | 0.677 | Table 4b, p.38 | "(0.344) (1.530) (2.465) (0.378) (0.677) (0.443)" |
| ACS hourly earnings, **high-ed native** | −0.757* | 0.443 | Table 4b, p.38 | "UIWF -0.873 _[∗∗]_ 1.894 0.398 -0.691 _[∗]_ -0.928 -0.757 _[∗]_" |
| Ancestry-IV employment (alternative design) | 2.499*** | 0.822; **first-stage F 6.80** | Table B3, appx p.7 | "Full IV estimate ( _β_ [ˆ] ) 2.499*** 0.651**" |
| Conventional (no leave-out) shift-share employment | 0.651** | 0.260; F 14.09 | Table B3, appx p.7 | "First-Stage F 6.80 14.09" |
| Rotemberg weight on Mexico, ancestry IV | 0.674 | just-identified β = 2.553 | Table B3, appx p.7 | "Mexico 0.674 2.553 0.011 1.135" |
| Baseline IV excluding "Other" origins | 1.042 | over-ID p = 0.61 | Table 2, p.30 | "Baseline IV estimate ( _β_ [ˆ] ) 0.961 1.042" |
| Over-ID test p-values (preferred design) | 0.67 / 0.61 | — | Table 2, p.30 | "Over-identifcation test p-value 0.67 0.61" |
| Boom-period contribution, employment (median / average area) | 14.6% / 30.1% of growth | implied effect 0.8% / 2.6% | Table 5, p.39 | "Employment 0.8 5.6 14.6 2.6 8.7 30.1" |
| Boom-period contribution, house prices | 13.1% / 29.6% | implied 2.9% / 6.6% of 22.3 / 22.4 | Table 5, p.39 | "House Prices 2.9 22.3 13.1 6.6 22.4 29.6" |
| Boom-period contribution, rents | 8.6% / 20.1% | implied 1.9% / 4.3% | Table 5, p.39 | "Market Rents 1.9 22.3 8.6 4.3 21.6 20.1" |
| Working-age share of post-2021 unauthorized arrivals | 75–80% | vs 62% for US-born | Fig. 3b, p.17 | "75%-80% of unauthorized immigrants arriving after 2021 are of working age (orange line)." |
| Employment rate of working-age unauthorized | ~70% | ACS 2021–24, 3-yr arrivals, HE countries | Fig. 3b / text p.17 | "estimate that approximately 70% are employed (blue line)." |
| Implied worker share of all unauthorized entrants | 50–60% | — | text p.17 | "between 50 and 60% of unauthorized immigrants entering" |
| National scale of the episode | ~7 million over 2021–2024 (1.75M/yr) | CBO 2026 | intro p.1 | "this category of immigrants added roughly 7 million people to the U.S. population over" |

Stars: * p<0.1, ** p<0.05, *** p<0.01. CIs shown are my ±1.96·SE arithmetic on the reported SEs, not printed in the paper. [CALCULATION]

**Verification:** all 48 numeric rows above, and every prose quote in this file, were re-found in the parsed source with `rg -F` (64 distinct verbatim fragments, 0 failures). No row was dropped.

## What it says about

- **Native wages by skill/education.** Only in the ACS arm (Table 4b, 2021–2023, CZ). Native-born hourly earnings −0.691 (SE 0.378, p<0.1); low-education native −0.928 (SE 0.677, insignificant); high-education native −0.757 (SE 0.443, p<0.1). The paper notes "estimated effects on low-education and high-education native-born wages are of a similar" magnitude — i.e. **no skill gradient is detected**, which is itself awkward for a canonical low-skill labor-supply story. The QCEW arm finds no significant industry-specific wage effect at all: "are negative for all but one industry, but the effects are statistically insignificant in all cases."
- **Native employment / crowd-out.** Effectively **no measurable crowd-out**: native-born employment coefficient 0.175 (SE 0.854), low-ed native 0.168, high-ed native 0.0077, all insignificant. The foreign-born effect (0.749) is "driven almost entirely by individuals from high-encounter countries". The authors concede the identification is weak in this arm: "_A_ _priori_, we would have expected the impact on foreign-born employment to be closer to" one, "and that on native-born employment to be closer to zero; one cannot statistically reject" either hypothesis **Treat the native-employment null as uninformative, not as evidence of zero.**
- **Housing prices, rents.** House prices +2.2% and rents +1.4% per 1%-of-employment UIWF, with permits null and construction employment muted → interpreted as a pure demand shock against inelastic short-run supply. Robustness is mixed: CoreLogic and Freddie Mac price effects are ~1% and insignificant; self-reported ACS values show **no significant effect** (median house price point estimate is negative, −2.227). Comparison anchors given: Saiz (2007) legal immigration IV house-price elasticity "a little over 3", rent elasticity ~1; Cabral & Steingress (2026) rents ~2, prices 2–3.
- **Fiscal: taxes, transfers, public services, schooling.** **Taxes: not studied.** **Public services and schooling: not studied** — there is no spending-side, per-pupil, enrollment or service-cost analysis anywhere in the paper. The only fiscal object is **government transfers measured as the transfer-receipts component of personal income in BEA Regional Economic Accounts** (county-level annual, aggregated to CZ): "we obtain county-level annual personal income and its components from the" Bureau of Economic Analysis' Regional Economic Accounts. It is **income received by local residents, in dollars, total and per capita** — not program enrollment, not government outlay per immigrant, not a budget line. Effects: −4.495 (total) and −4.977 (per capita) for 2021–2023; **−1.423 and −1.963 for the 2021–2024 window**, a factor of ~2.5 smaller, which the authors attribute to rising utilization with tenure. Programs named as the *mechanism* (UI, TANF, SNAP, Medicaid) are illustrative; the paper never decomposes the BEA transfer series by program. The authors explicitly contrast this with Camarota & Zeigler (2026), who report 59% of non-citizen-headed households receiving at least one major welfare benefit in 2024 vs 37% of US-born households, and rebut on three grounds: extensive margin only, no legal/unauthorized split, and no treatment of US-citizen children in mixed households.
- **Firms, production, investment, profits.** Not studied, except housing investment via permits (null) and the industry composition of employment growth. No output, productivity, capital or profit outcome.
- **Mechanism the authors claim.** Labor market: a **labor supply shock absorbed roughly one-for-one into employment** without measurable wage decline, concentrated in Leisure & Hospitality ("timated effect is statistically significantly positive for three industries (Leisure & Hospitality," ... "share for Leisure & Hospitality."), with a negative and significant effect on Manufacturing employment during the boom. Housing: a **demand shock with fixed short-run supply**. Reconciling flat total income with rising house prices: **non-homothetic preferences with housing as a necessity** — a composition shift toward low-income households with higher housing expenditure shares. Transfers: higher employment plus lower program take-up among recent unauthorized arrivals.

## Elasticities or parameters a model could transport

Each object below is a **semi-elasticity with respect to UIWF measured as a percent of initial local employment**, estimated on US commuting zones (or MSAs), boom period 2021m3–2024m3, employment-weighted, IV.

1. **Employment response to unauthorized worker inflow, CZ level: 0.961** (SE 0.274). Equivalently 0.650 per 1% of employment in *all working-age* unauthorized flow and 0.507 per 1% in *all* unauthorized flow — the ratio 0.507/0.961 ≈ 0.53 is the paper's own implicit worker share.
2. **House price semi-elasticity, MSA level: 2.189** (SE 0.741); **market rent semi-elasticity: 1.438** (SE 0.344), SF 1.229, MF 1.470. Denominator is *employment*, not population — rescaling to a population-based elasticity (as in Saiz 2007) requires the local employment/population ratio.
3. **Per-capita labor income semi-elasticity: −1.151** (SE 0.503) — a pure composition object, not a wage effect.
4. **Per-capita government transfer-receipt semi-elasticity: −4.977** over 2021–2023, **−1.963** over 2021–2024 (SE 1.324 and 0.803). **The two windows disagree by 2.5×; any transport should use the 2021–2024 figure or the range, and should not be read as a lifetime or steady-state fiscal parameter.**
5. **Housing supply response: −0.208 permits per initial housing unit** per 1% UIWF (SE 0.213) — a usable short-run no-supply-response prior over a 3-year horizon.
6. **Worker conversion factors** for translating headcounts to workers: working-age share **75–80%** (vs 62% US-born), employment rate among working-age **~70%**, implied worker share **50–60%**.

**Transport warning for the parent's fiscal account.** [INFERENCE] These are *local relative* coefficients from a 3-year cross-section of net flows of recent unauthorized arrivals. They are not a stationary fiscal account, they exclude taxes and all public services, and the transfer coefficient is a BEA *receipts* series for all local residents, not an outlay attributable to immigrants. The authors themselves warn that "the employment (and other) effects of" / "UIWF for the weighted-mean CZ do not necessarily equal the national effects. National effects of UIWF will" / "additionally reflect cross-CZ spillovers and general equilibrium effects beyond local markets." Nothing here identifies a native surplus, a CES substitution elasticity, or any production-function parameter — **the paper estimates no elasticity of substitution between natives and immigrants.**

## Authors' stated limitations and external-validity notes

- **Geography imputed for parolees and got-aways**: "The scaling procedure we use to construct local UIWF assumes that, conditional on the country of origin," parolees and got-aways settle like NTA entrants, and "little is known about how the settlement patterns may" differ. They argue IV remains unbiased under classical measurement error in the endogenous variable while OLS attenuates.
- **Slowdown period treated as an extension**, with three cautions: only Feb–Jul 2025 has net aggregate outflows, exit measurement is weakest from 2025 on, and lagged boom effects may contaminate but cannot be estimated without severe multicollinearity.
- **QCEW is not seasonally adjusted**; heterogeneous seasonality across CZs could correlate with UIWF, so expanding-window estimates ending far from March/Q1 are flagged as less reliable. Over those windows employment ranges "from about 0.5 to nearly 1" and wages "from roughly -1 to -2".
- **Average weekly wages conflate hours and hourly wages** — a rising-hours / falling-hourly-wage combination could cancel: "hourly wages, as one might expect from a labor supply shock, these countervailing effects" could offset each other
- **ACS concerns**: unauthorized respondents may under-participate and be under-covered; foreign-born vs native-born sample weights since 2021 are "likely to be inaccurate" (Coglianese et al. 2025); annual frequency cannot be aligned with the monthly boom/slowdown windows.
- **Self-reported ACS home values** carry "substantial, and possibly non-classical, measurement error" from uncontrolled quality/composition and owners' ignorance of current market value.
- **Rotemberg sensitivity**: the "Other" origin category carries weight 0.27 with a just-identified estimate of 0.803; excluding it moves the headline from 0.961 to 1.042.
- QCEW covers **private nonfarm** employment on UI-covered payrolls — off-books and agricultural employment of unauthorized workers is outside the measure. [INFERENCE: the paper describes the coverage but does not draw this caveat itself.]

## Data availability

**No replication package is mentioned anywhere in the paper.** The two core inputs are explicitly **restricted-use** individual-level administrative files (EOIR immigration-court records; CBP parole records), accessed through TRAC at Syracuse under FOIA. Got-away figures for 2023+ come from DHS press releases and FOIA requests. The ancestry-instrument inputs are the one public component: county×origin predicted ancestry and the historical pull-push interaction terms downloaded from `https://www.immigrationshock.com/ancestry-instruments`. Remaining inputs are licensed or public series: QCEW, Zillow ZHVI/ZORI, CoreLogic, Freddie Mac HPI, Census building permits, BEA Regional Economic Accounts, ACS. One wage result is reported as "upon request) is significantly negative under the ancestry IV, with an estimated magnitude" (ancestry-IV wage effect, −1.3).
