<!-- reader extraction, opus-low agent, 2026-09-22; every numeric row carries a verbatim quote re-found in the parsed corpus text with rg -F; parent spot-checked the rows cited in the memo -->
[UNVERIFIED]

Provenance note: every number below is transcribed from the parsed text of
`/Users/alien/Projects/corpus/doi_10_1086_707764/parsed.pymupdf4llm@0.3.4+cfg-99914b93/page.md`
(JPE-accepted preprint, "not copyedited or formatted", dated October 21, 2019). Page numbers are
the preprint's own printed page markers; `L####` are line anchors in that parsed file. Tag for the
parent's ladder: [SOURCE: doi:10.1086/707764] for each row, since each carries a verbatim quote.

# Monras (2020), "Immigration and Wage Dynamics: Evidence from the Mexican Peso Crisis", JPE

**Verdict:** A push-factor natural experiment (the 1995 Mexican Peso Crisis) crossed with the
Card networks instrument identifies a large *short-run* inverse local labour demand elasticity for
low-skilled natives (about −0.7 state-level, −1.4 metro-level), shows it dissipating within ~2–3
years through internal migration, and finds the only lasting effects are on the *cohorts* that
entered the low-skilled labour market in high-immigration years and on *house prices* (Mexicans
enter construction and cut construction costs); the design is strong on the short run (first-stage
F 19–27, clean placebos) and much weaker on the long run, where the cross-age IV is a new,
untested instrument and the housing result rests on a back-of-envelope cost-share argument.

## Population, period, unit

- **Shock:** Mexican net inflows to the US, 1995 (and 1996), triggered by the December 1994 peso
  devaluation. "migration flows to the US were at least 40 percent higher, with 200,000 to 300,000
  more Mexicans immigrating in 1995 than in a typical year of the 1990s" (p.3, L206). CPS-based
  magnitude: "around 500,000 low-skilled Mexicans entered the US in 1995 and in 1996, up from
  around 200,000 or 300,000 a year before 1995" (p.7, L625).
- **Units:** 51 states (50 + DC) and 163 CPS-identifiable metropolitan areas; 141/135 metros for
  housing (FHFA coverage), 157/147 metros for 1990-Census-based long-run regressions.
- **Periods:** short run = 1994 (or 1992–94 pooled) vs 1995, annual March CPS 1990s; long run =
  1990 vs 2000 decennial Census; cross-age long-run cells = 46 ages (20–65) low-skilled, 41 ages
  (25–65) high-skilled.
- **Skill definition:** "I define high-skilled workers as workers having more than a high school
  diploma, while I define low-skilled workers as having a high school diploma or less" (p.9, L739).
- **"Native" definition:** non-Mexican / non-Hispanic (US-born-only variant in Appendix A.5).
  Wages are weekly wages of full-time workers, individual-adjusted via Mincer regressions in the
  preferred column.

## Design and identification

- **Short run:** first-difference 1994→1995 of local outcomes on the change in the Mexican share of
  the low-skilled labour force, instrumented with the **1980 Mexican share** (networks instrument);
  the exogenous *timing* comes from the peso crisis, the exogenous *place* from 1980 settlement.
  Controls: Δlog state GDP, Δlog exports to Mexico, Δlog low- and high-skilled labour;
  location-specific linear wage trends; preferred column uses 1992–94 as the pre-period.
- **First stage:** state-level F = 26.73, metro-level F = 19.14 for the differenced wage
  specifications (Table 3); cross-sectional F = 511.5 (state) / 68.33 (metro). Table 2 reports the
  1980→1995 share regressions: state coefficient 6.116 (0.270), R² 0.967; metro 4.232 (0.512),
  R² 0.813. Placebo: 1980 high-skilled Mexican share does **not** predict the differenced
  high-skilled share (−0.197, s.e. 0.399).
- **Long run, cross-space:** 1990→2000 changes on the relative inflow of Mexicans, networks IV
  (state F = 42.73; metro F = 24.18 / 15.89 for housing).
- **Long run, cross-age (new IV):** interacts the (stable) age distribution of Mexican arrivals with
  aggregate yearly inflows in the 1990s, giving exogenous variation in immigration across
  experience cells for a Borjas (2003)-style regression (F = 53.59 low-skilled, 33.59 high-skilled).
- **Placebos** run by relabelling a pre-shock year as the post-shock year (Table 7).

## Headline estimates

All wage/employment coefficients are **inverse elasticities**: the effect of a 1 percent
immigration-induced increase in the local (or cell) low-skilled labour supply.

| Outcome | Estimate | SE or CI | Table / page | Verbatim quote (≤40 words) |
|---|---|---|---|---|
| SHORT RUN: native low-skilled wage, state, IV, preferred (col 7) | **−0.708** | s.e. 0.307 | Table 3 Panel A col 7, p.45 (L3997) | "∆Share of Mexicans, LS -0.602 -0.733 -0.832 -0.721 -0.708" |
| SHORT RUN: native low-skilled wage, metro, IV, preferred (col 7) | **−1.418** | s.e. 0.331 | Table 3 Panel B col 7, p.45 (L4015) | "∆Share of Mexicans, LS -1.397 -1.518 -2.295 -2.218 -1.418" |
| SHORT RUN: stated range for the inverse demand elasticity | **−0.7 to −1.4** | — | §3.2, p.14 (L1148) | "of the inverse demand elasticity that goes from -.7 to -1.4." |
| SHORT RUN: headline summary of the same | −0.7 to −1.4 per 1% | — | §1, p.3 (L211) | "reduces low-skilled wages at the state or metropolitan area levels by around .7 to 1.4 percent" |
| SHORT RUN: native **high-skilled** wage, state, IV (col 7) | +0.170 (null) | s.e. 0.229 | Table 3 Panel C col 7, p.45 (L4033) | "∆Share of Mexicans, LS -0.246 -0.301 0.114 0.119 0.170" |
| SHORT RUN: native **high-skilled** wage, metro, IV (col 7) | −0.0111 (null) | s.e. 0.417 | Table 3 Panel D col 7, p.45 (L4051) | "∆Share of Mexicans, LS -0.661 -0.426 -0.744 -0.719 -0.0111" |
| Inverse elasticity of substitution high-vs-low skilled (wage-gap regression), state IV | 0.883 | s.e. 0.408 | Table 4 Panel A col 8, p.46 (L4111) | "∆Share of Mexicans, LS 0.381 0.434 0.485 0.776 0.795 0.883" |
| Same, metro IV | 1.395 | s.e. 0.387 | Table 4 Panel B col 8, p.46 (L4131) | "∆Share of Mexicans, LS 0.822 0.838 1.008 1.181 1.262 1.395" |
| Implied σ used in the model | **σ ≈ 1** | — | §3.2, p.14 (L1246) | "Estimates of the inverse of the elasticity of substitution between high- and low-skilled workers" [next line: "cluster around 1."] |
| SHORT RUN: low-skilled native **employment rate**, state, IV | +0.131 (null) | s.e. 0.323 | Table 5 Panel A col 5, p.47 (L4188) | "∆Share of Mexicans, LS -0.0840 -0.0276 0.131" |
| SHORT RUN: low-skilled native employment rate, metro, IV | +0.0308 (null) | s.e. 0.554 | Table 5 Panel B col 5, p.47 (L4206) | "∆Share of Mexicans, LS -0.402 -0.379 0.0308" |
| Author's reading of employment | no differential response | — | §3.3, p.14 (L1336) | "employment rates did not differentially change in high- relative to low-immigrant locations" |
| SHORT RUN: **rental gap** (rents relative to house prices), state, IV | **+0.676** | s.e. 0.346 | Table 6 Panel A col 7, p.48 (L4276) | "∆Share of Mexicans, LS 0.279 0.223 0.0449 0.676" |
| SHORT RUN: rental gap, metro, IV | **+0.555** | s.e. 0.165 | Table 6 Panel B col 7, p.48 (L4298) | "∆Share of Mexicans, LS 0.205 0.130 0.0304 0.555" |
| Author's rescaling of the rental effect | ~1% rents per 1% population | — | §3.4, p.16 (L1397) | "in a city leads to around 1 percent increase in rental prices" |
| Cross-sectional level: rents vs Mexican share, state IV | +0.382 | s.e. 0.186 | Table 6 Panel A col 2, p.48 (L4279) | "Share of Mexicans, LS 0.402 0.382 0.422" |
| DYNAMICS: wage, state, 1992-94 → 1995 | −0.708 | 95% CI −0.401 to −1.015 | Table 7 Panel A, p.49 (L4335) | "from 1992-94 to 1995 (main estimate) -0.708 -0.401 -1.015" |
| DYNAMICS: wage, state, 1992-94 → 1995-98 | −0.413 | 95% CI −0.0239 to −0.803 | Table 7 Panel A, p.49 (L4338) | "from 1992-94 to 1995-98 -0.413 -0.0239 -0.803" |
| DYNAMICS: wage, state, 1990 → 1999 | −0.255 (n.s.) | 95% CI +0.0586 to −0.569 | Table 7 Panel A, p.49 (L4339) | "from 1990 to 1999 -0.255 0.0586 -0.569" |
| DYNAMICS: wage, state, placebo 1992-94 → 1991 | −0.0779 (n.s.) | 95% CI +0.163 to −0.318 | Table 7 Panel A, p.49 (L4334) | "from 1992-94 to 1991 (placebo) -0.0779 0.163 -0.318" |
| DYNAMICS: wage, metro, 1992-94 → 1995 | −1.418 | 95% CI −0.769 to −2.066 | Table 7 Panel B, p.49 (L4347) | "from 1992-94 to 1995 (main estimate) -1.418 -0.769 -2.066" |
| DYNAMICS: wage, metro, 1990 → 1999 | −0.384 | 95% CI +0.007 to −0.839 | Table 7 Panel B, p.49 (L4351) | "from 1990 to 1999 -0.384 0.007 -0.839" |
| DYNAMICS: rental gap, state, 1994 → 1995 | +0.584 | 95% CI +1.235 to −0.0663 | Table 7 Panel C, p.49 (L4360) | "from 1994 to 1995 (main estimate) 0.584 1.235 -0.0663" |
| DYNAMICS: rental gap, metro, 1994 → 1995 | +0.555 | 95% CI +0.878 to +0.232 | Table 7 Panel D, p.49 (L4372) | "from 1994 to 1995 (main estimate) 0.555 0.878 0.232" |
| DYNAMICS: rental gap, metro, 1994 → 1995-99 | −0.469 | 95% CI −0.0358 to −0.902 | Table 7 Panel D, p.49 (L4376) | "from 1994 to 1995-99 -0.469 -0.0358 -0.902" |
| RELOCATION: Δ low-skilled pop. share per Δ Mexican share, 1994→95, state IV + native-trend control (col 6) | **+1.077** | s.e. 0.293 | Table 8 Panel A, p.50 (L4387) | "1.253<br>1.077" [row: "1.230<br>1.244<br>1.253<br>1.077<br>(0.233)<br>(0.254)<br>(0.217)<br>(0.293)"] |
| RELOCATION: same, 1995→96, state IV (col 10) | **−0.741** | s.e. 0.412 | Table 8 Panel A, p.50 (L4387) | "-0.791<br>-0.741" [row: "-0.153<br>-0.111<br>-0.791<br>-0.741<br>(0.383)<br>(0.397)<br>(0.373)<br>(0.412)"] |
| RELOCATION: metro, 1994→95, IV (cols 5/6) | +2.102 / +1.112 | s.e. 0.484 / 0.571 | Table 8 Panel B, p.50 (L4394) | "2.102<br>1.112" |
| RELOCATION: metro, 1995→96, IV | −0.642 / −0.522 | s.e. 0.874 / 0.911 | Table 8 Panel B, p.50 (L4394) | "-0.642<br>-0.522" |
| Author's summary of the impact year | ≈ one-for-one | — | §3.6, p.19 (L1694) | "estimate very close to 1, both using cross-state and cross-metropolitan area variation" |
| Author's summary of year 2 | reverts | — | §3.6, p.19 (L1713) | "the share of low-skilled workers almost reverts back to where it was before" |
| LONG RUN: native low-skilled wage, cross-state IV, 1990–2000 | −0.255 (n.s.) | s.e. 0.160 | Table 9 Panel A, p.51 (L4425) | "-0.00831<br>-0.255" [with "(0.168)<br>(0.160)"] |
| LONG RUN: native low-skilled wage, cross-metro IV | −0.384 (n.s.) | s.e. 0.232 | Table 9 Panel A, p.51 (L4427) | "0.0312<br>-0.384" [with "(0.103)<br>(0.232)"] |
| LONG RUN: native low-skilled wage, **cross-age IV** | **−0.533** | s.e. 0.130 | Table 9 Panel A, p.51 (L4425) | "-0.235<br>-0.533" [with "(0.0939)<br>(0.130)"] |
| Author's statement of the cross-age estimate | ≈ −0.53 | — | §4.2, p.21 (L1899) | "I obtain an estimate of around -.53." |
| LONG RUN: native high-skilled wage, cross-age IV | +0.241 (n.s.) | s.e. 0.177 | Table 9 Panel B, p.51 (L4470) | "0.297<br>0.241" |
| LONG RUN: low-skilled native employment rate, cross-age IV | **−0.572** | s.e. 0.142 | Table 9 Panel C, p.51 (L4456) | "-0.714<br>-0.572" [with "(0.135)<br>(0.142)"] |
| LONG RUN: high-skilled native employment rate, cross-age IV | +0.124 (n.s.) | s.e. 0.126 | Table 9 Panel D, p.51 (L4447) | "-0.457<br>0.124" |
| Author's reading of the employment-rate result | 10% shock → 6–7% lower employment rate | — | §4.3, p.21 (L1920) | "a 10 percent immigration induced labor supply shock decreases employment rates by around" [next line: "6 or 7 percent"] |
| LONG RUN HOUSING: Δln rent, state IV | **−0.548** | s.e. 0.366 | Table 10 Panel A col 2, p.52 (L4505) | "-0.244<br>-0.548" [with "(0.336)<br>(0.366)"] |
| LONG RUN HOUSING: Δln house price index, state IV | **−0.780** | s.e. 0.424 | Table 10 Panel A col 4, p.52 (L4505) | "-0.0866<br>-0.780" |
| LONG RUN HOUSING: Δln rent gap, state IV | +0.231 (n.s.) | s.e. 0.284 | Table 10 Panel A col 6, p.52 (L4505) | "-0.157<br>0.231" |
| LONG RUN HOUSING: Δln rent, metro IV | **−1.171** | s.e. 0.518 | Table 10 Panel B col 2, p.52 (L4515) | "-0.284<br>-1.171" |
| LONG RUN HOUSING: Δln house price index, metro IV | **−1.430** | s.e. 0.704 | Table 10 Panel B col 4, p.52 (L4515) | "-0.202<br>-1.430" |
| Author's summary of long-run housing | elasticity ≈ −1, rent gap zero | — | §4.4, p.22 (L2056) | "lower housing prices and lower rental prices, with and elasticity of around -1" |
| LONG RUN RELOCATION: Δ low-skilled share per Mexican inflow, state IV | 0.794 (no control) / 0.613 (with 1980 share) | s.e. 0.0513 / 0.0988 | Table 11 Panel A cols 6, 8, p.53 (L4541) | "0.782<br>0.794<br>0.632<br>0.613" |
| Author's summary of that | 0.8 per arrival, 0.6 with controls | — | §4.5, p.23 (L2110) | "for every low-skilled Mexican entering a high-immigration state, the state gains" [next line: "0.8 low-skilled workers"] |
| CONSTRUCTION: Δ Mexican share of low-skilled construction per Mexican inflow, state IV | 0.495 | s.e. 0.0980 | Table D10 Panel A col 2 (L8146) | "0.652 0.495 0.118 0.00268 -0.144 -0.454" |
| CONSTRUCTION: Δ share of all workers in construction, state IV (i.e. full native displacement) | 0.00268 (zero) | s.e. 0.0694 | Table D10 Panel A col 4 (L8146) | "0.652 0.495 0.118 0.00268 -0.144 -0.454" |
| CONSTRUCTION: Δln native low-skilled wage **within construction**, state IV | **−0.454** | s.e. 0.213 | Table D10 Panel A col 6 (L8146) | "0.652 0.495 0.118 0.00268 -0.144 -0.454" |
| CONSTRUCTION: same, metro IV | **−0.765** | s.e. 0.330 | Table D10 Panel B col 6 (L8156) | "0.598 0.373 0.103 -0.0197 -0.0539 -0.765" |
| Author's summary of construction wages | −0.7 to −0.8 | — | Appendix A.9, p.9 (L5892) | "by around .7 to .8 percent for a 1 percent immigration-induced supply shock" |
| Implied house-price elasticity from construction-cost channel (labour share 0.6, composition adj. ~40%) | **−0.84** | back-of-envelope, no SE | §4.4, p.23 (L2067); derivation Appendix A.10 | "an elasticity of around -0.84" |
| Price elasticity of local housing demand implied by new construction | −0.3 to −0.4 | no SE | §4.4, p.23 (L2073) | "-0.3 and -0.4, in line with Hanushek" |
| New single-family construction 1994–2000 per Mexican inflow, state IV | +2.159 | s.e. 0.329 | Table D11 Panel A (L8181) | "1.873 2.159" |
| Mexicans' renter share on arrival (1987–90 arrivals, 1990 Census) | 0.82 US / 0.84 CA | descriptive | Table 1 Panel C, p.43 (L3922) | "Mexicans in rented units / Total Mexicans (Census 1990, 1987-1990 arrivals)) 0.82 0.84" |
| Net change in construction workers 1990–2000, CA | Mexicans +110,028 / natives −76,962 | descriptive | Table 1 Panel B, p.43 (L3899, L3900) | "∆Mexicans in Construction (1990-2000) 592,868 110,028" and "∆Natives in Construction (1990-2000) 1,138,228 -76,962" |
| MODEL: implied internal-migration cost parameter λ̂ | **≈ 1.47** (given β = 0.95, η = 0.05) | calibrated | §6.2, p.33 (L3295) | "0 _._ 05) _[∗]_ [0] _[.]_ [05] _[∗]_ 0 _._ 135 _[≈]_ [1] _[.]_ [47]" (mangled math in the parse; λ̂ ≈ 1.47) |
| MODEL: estimated housing supply elasticity (rentals vs owned) | 0.5–0.6 | — | §6.2, p.33 (L3298) | "between .5 and .6. This is the average housing supply elasticity across locations" |
| COUNTERFACTUAL: Arizona sealing its border, low-skilled wage gain | ~2% (1–3% in the intro) | model, no SE | §6.4, p.34 (L3459); §1, p.5 (L367) | "was maybe 2 percent lower than what it would have been with a more restrictive immigration law"; "on the order of 1 to 3 percent higher wages" |
| SHOCK SIZE | ≥ +40%, 200–300k extra arrivals in 1995 | — | §1, p.3 (L206) | "at least 40 percent higher, with 200,000 to 300,000 more Mexicans immigrating in 1995" |

## What it says about

- **Native wages by skill/education.** The core result. Low-skilled natives (high-school diploma or
  less) lose 0.7% (state) to 1.4% (metro) per 1% immigration-induced supply increase **on impact**;
  high-skilled natives are unaffected at every horizon (short-run point estimates +0.17 / −0.01,
  long-run cross-age +0.24, all insignificant). Effects fade over 3–5 years and are statistically
  zero over 1990–1999 across space. The lasting damage is **cohort-specific**: workers entering the
  low-skilled labour market in high-immigration years show −0.53 wage growth per unit shock over
  1990–2000. Unlike Borjas (2017) on Mariel, the effect is **not** confined to high-school dropouts:
  "I obtain similar results if I consider the high school dropouts or the high school graduates
  exclusively as the group of workers competing with the Mexicans" (§3.2, p.14).
- **Native employment / crowd-out.** No short-run local employment-rate response (state +0.13,
  metro +0.03, both insignificant); the author drops employment from the structural model for this
  reason. But over the decade, across age cells, low-skilled native employment rates fall −0.572
  per unit shock (high-skilled +0.12, null). Within construction, crowd-out is essentially complete:
  the sector's share of all workers does not grow (IV 0.003, s.e. 0.069) while Mexicans take ~0.5 of
  each arrival's slot; in California natives *left* construction (−76,962) as Mexicans entered
  (+110,028). Spatial crowd-out (internal migration) is the paper's main adjustment channel, not
  employment exit: the low-skilled population share rises ~1-for-1 in the shock year and reverts
  the next year (−0.74).
- **Housing prices, rents.** Two opposite-signed channels. Short run: >80% of new Mexican arrivals
  rent, so the **rental gap** (rents relative to house prices) rises ~0.55–0.68 per unit shock on
  impact, stays elevated ~3 years, then closes. Long run (1990–2000): **both** rents and house
  prices fall in high-Mexican-inflow locations, elasticity ≈ −1 (state −0.55 rents / −0.78 HPI;
  metro −1.17 / −1.43), leaving the rent gap at zero. The author attributes the long-run decline to
  cheaper construction labour, not to native flight, and corroborates with a +2.16 elasticity of new
  single-family construction.
- **Fiscal: taxes, transfers, public services, schooling.** **Not studied.** The parsed text contains
  no occurrence of "fiscal", "tax", "welfare benefit", "public service" or school spending. The one
  adjacent remark is that immigrants "may affect the quality of local public goods, thus reducing
  the amenity value of living in certain locations" (§4.4, p.22) — cited as a *possible* mechanism
  from Saiz and Wachter (2011) / Sa (2015) and not measured.
- **Firms, production, investment, profits.** Not directly measured. Production enters only through
  the structural model: a location-level CES over high- and low-skilled labour with σ ≈ 1 and
  elastically supplied capital; construction is modelled as perfectly competitive with a labour cost
  share of at least 0.6 (from Gyourko and Saiz 2006). Counterfactual 1 finds that a model where
  **local technology adapts to expected inflows** fits the data better than a fixed-technology
  model, so expected immigration is absorbed by technology and unexpected immigration by internal
  migration. No profit, investment or firm-entry outcomes are estimated.
- **Mechanism the authors claim.** (1) An unexpected low-skilled inflow depresses local low-skilled
  wages and raises the rental gap on impact; (2) internal relocation of low-skilled workers
  (≈ 0.5 workers leave per Mexican arrival within a year) spreads the shock nationally and restores
  local relative wages within ~2–3 years; (3) what survives nationally is a cohort effect on those
  entering the labour market in high-immigration years; (4) in housing, the durable effect is a
  *fall* in prices and rents caused by Mexicans entering construction, displacing natives, and
  lowering construction labour costs — an explanation distinct from the native-avoidance story in
  Saiz and Wachter (2011) and Sa (2015).

## Elasticities or parameters a model could transport

1. **Inverse local labour demand elasticity for low-skilled natives, short run, state level:
   −0.708 (s.e. 0.307)**; metro level −1.418 (s.e. 0.331). Estimated on non-Mexican full-time
   workers with ≤ high-school education, US states / 163 metros, 1992-94 vs 1995. This is a
   *local, on-impact* object and is explicitly not the national long-run elasticity.
2. **Elasticity of substitution between high- and low-skilled workers, σ ≈ 1** (Cobb-Douglas),
   identified from the wage-gap regression; inverse-σ point estimates 0.883 (state) and 1.395
   (metro). Population: US state/metro labour markets, 1994–95. Note this is the **skill-cell**
   elasticity, NOT a native-vs-foreign-born within-cell elasticity — the paper never estimates the
   latter, so it does not pin down the parent's ε.
3. **Internal-migration response: ∂L_s/∂Mex_s ≈ 0.5 within one year** ("how many low-skilled workers
   relocate per Mexican arrival", §6.2, p.33), which combined with the −0.7 wage estimate gives the
   model's migration-elasticity parameter **λ̂ ≈ 1.47** under β = 0.95 (Kennan-Walker) and η = 0.05.
4. **Long-run national (cross-experience-cell) inverse elasticity for low-skilled natives: −0.533
   (s.e. 0.130)** on wages and **−0.572 (s.e. 0.142)** on employment rates, 1990–2000, 46 age cells.
   This is the cohort-entry effect, not a steady-state wage elasticity.
5. **Long-run cross-location inverse elasticity: −0.255 (state) / −0.384 (metro), both insignificant**
   — the number that mechanically results when internal migration has already dissipated the shock.
   Useful as the "spatial approach attenuation" benchmark.
6. **Housing: long-run elasticity of rents and of house prices to Mexican inflow ≈ −1**; short-run
   rental-gap elasticity ≈ +0.55 to +0.68 per unit low-skilled shock, or ≈ 1% rents per 1%
   population. **Housing supply elasticity 0.5–0.6** (the paper substitutes Saiz 2010's
   heterogeneous elasticities in the model). **Price elasticity of local housing demand −0.3 to
   −0.4.** **Construction labour cost share ≥ 0.6**; wage-composition adjustment ≈ 40%.
7. **Renter share of recent Mexican arrivals: 0.82** (1987–90 arrivals, 1990 Census) versus ~0.30–0.32
   for low-skilled natives — directly usable as a housing-tenure split for a Mexican-origin G1
   population.
8. **Construction-sector absorption: ~0.5 of each Mexican low-skilled arrival enters construction,
   with zero net growth in the sector's employment share** (state IV 0.003, s.e. 0.069), i.e. full
   native displacement within the sector, and native construction wages −0.45 (state) to −0.77
   (metro) over the decade.

## Authors' stated limitations and external-validity notes

- **Estimates are deliberately conservative.** "I consider all Mexican as potential workers, and
  measure the shock relative to the full-time non-Mexican labor force... Second, among the many
  estimates of the size of the shock I discussed earlier, I use the largest one" (fn.19, p.13) —
  both choices bias the inverse elasticity toward zero.
- **Short run only, by construction.** "It is important to keep in mind that these are short-run
  effects" (Conclusion, p.36). The long-run cross-space design is contaminated by spillovers:
  "internal migration generates spillovers between treatment and control units that tends to
  attenuate the estimated effect" (§4, p.19).
- **Metro estimates exceed state estimates** because immigration is urban; the author attributes the
  gap to an urban-rural trend rather than to a truer local market, and shows in Table D4 that
  controlling for baseline wage levels brings metro and state estimates together.
- **Net flow measurement is uncertain.** "Precise estimates on net Mexican immigration are hard to
  obtain... Many Mexicans enter the US illegally, potentially escaping the count of US statistical
  agencies" (§2, p.7). A documented CPS weighting change between 1995 and 1996 forces the author to
  avoid supplement weights in cross-1995 comparisons (fn.8, p.8).
- **Low R²** in the wage regressions "due to the large variance in small low-immigration states"
  (fn.20, p.13).
- **The construction-cost mechanism is a back-of-envelope**, not an estimated structural object; the
  −0.84 figure rests on Gyourko-Saiz's labour share and an assumed perfectly competitive,
  elastically-capital-supplied construction sector.
- **Model calibration borrows β = 0.95 from Kennan and Walker (2011)** and sets η = 0.05 to match
  the average internal migration rate; λ̂ is not independently estimated.
- **Generalisability**: the experiment is a low-skilled, largely undocumented, Mexican inflow into
  historically Mexican locations in the mid-1990s. The author argues it improves on Mariel because
  it hits many markets rather than five cities, and shows robustness to dropping California or
  Texas (Table D5) and to defining natives as US-born only (Table D7).

## Data availability

No replication-package, data-availability, archive or "available on request" statement appears
anywhere in this parsed preprint (searched for "replication", "data availability", "dataverse",
"openicpsr", "zenodo", "available upon request" — zero hits). All inputs are public or licensed
secondary sources: March CPS and decennial Censuses via IPUMS (Ruggles et al. 2016), the Mexican
Census 2000, FHFA house price indexes, INS apprehensions data from Gordon Hanson's website, state
GDP and exports to Mexico, and Saiz (2010) housing supply elasticities. Nothing in the paper is
restricted-access microdata. [INFERENCE] the JPE-era replication archive presumably exists at the
journal, but this parsed file does not evidence it.

---

**Verification:** 78 distinct `rg -F` checks run against the paper path. Every numeric row in the
headline table carries a fragment that returned ≥1 hit, and **no row was dropped** — nothing failed
to re-find. Five fragments failed on the first attempt only because the pymupdf4llm parse inserts
hard line breaks mid-sentence and `<br>` separators inside table cells; each was re-anchored to a
single physical line of the parse and then hit. The longer prose quotes in the limitations section
run across those same parse line breaks, so they are verbatim from the paper but must be searched
half-line by half-line (each half was confirmed). Rows verified: 48 of 48.
