**Verdict:** Small. The group's mobility across local labour markets is worth about **$0.65bn a
year** to other residents today (range $0.18–2.5bn), or **$16 per group member** ($4–60) and
**$2.2 per other resident** ($0.6–8.3). Two pieces make it up. Local-shock insurance, the
Cadena–Kovak smoothing of natives' employment, is worth **$0.13bn** at present-day mobility (range
0–1.0). Borjas's efficiency gain at the group's observed 2024 location is **$0.52bn**
($0.18–1.4bn). At 2006–10 mobility the insurance was worth $0.80bn ($0.04–3.0bn). Borjas's gain as
he defines it is $5.6bn ($3.4–16.6bn), but that case puts every Mexican-born worker in the
high-wage region, and in 2024 only 60% of them live there. Present-day Mexico-born mobility no
longer exceeds natives' inside the US. Men with high school or less moved between states or arrived
from abroad at 1.92% a year in 2019–24, against 2.13% for other natives (−0.21pp, SE 0.06); in
2006–10 they were +1.23pp above. Only return migration to Mexico, 0.8% a year and a third of its
2005–10 rate, keeps their total movement slightly above natives'. Our replication finds
Cadena–Kovak's pattern in the Great Recession but no smoothing in the COVID shock or the 2012–16
boom. Overlap ruling: nothing here is inside the production term P, which has no places or shocks.
Both channels sit beside the account as social benefits. The fiscal slice is the tax on the net
earnings change: $0.03bn today, and about $0.2bn more if Borjas's gain is taxed at the account's
marginal rate. It does not move the $203–250bn main case.

claude-opus-5-5[1m], lane agent, 2026-09-23. Frame: the complete annual account (2024, United
States with and without the 40,896,574 CPS Mexican-origin residents), effects on the 295.83m other
residents, 2024 dollars. Brief: [BRIEF.md](BRIEF.md).

## 1. The answer by channel

| Channel | $bn a year, central (range) | Per group member | Per other resident | Inside P? | Ruling |
|---|---|---|---|---|---|
| Local-shock insurance, present-day mobility | 0.13 (0–1.03) | $3.2 (0–25) | $0.44 (0–3.5) | no | beside the account, social benefit; tax slice $0.03bn |
| Same channel at 2006–10 mobility (reference) | 0.80 (0.04–3.03) | $19.6 (0.9–74) | $2.7 (0.1–10.2) | no | reference only; not the 2024 group |
| Borjas efficiency gain, observed 2024 location | 0.52 (0.18–1.43) | $12.8 (4.4–35) | $1.77 (0.61–4.85) | no | beside the account; needs fixed regional factors that the account's capital adjustment removes |
| Borjas efficiency gain as defined (all in the high-wage region) | 5.6 (3.4–16.6) | $136 (83–406) | $18.9 (11.5–56) | no | hypothetical; the group does not sort that way |
| National buffer: emigration and fewer arrivals in national recessions | unpriced | | | no | flagged, §8 |
| **Lane total, present day** | **0.65 (0.18–2.46)** | **$16 (4–60)** | **$2.2 (0.6–8.3)** | | |

[CALCULATION: `price_insurance.py` → `derived/insurance_summary.json`; `borjas_model.py` →
`derived/borjas_2024.csv`] The lane total adds the present-day insurance and Borjas's gain at the
observed location. The two are distinct mechanisms: responsiveness to shocks, and where the stock
sits. The low end of the total takes the insurance at zero.

## 2. The two anchor papers, read at the source

**Cadena & Kovak (2016), "Immigrants Equilibrate Local Labor Markets", AEJ: Applied 8(1):257–290**
[SOURCE: PMC4991313, cached `_cache/papers/ck2016_pmc.txt`]. The sample covers 95 metros (94 in the
IV), 2006–2010, ages 18–64, not in school or group quarters. For men with high school or less, the
population response to the group-specific payroll shock is 0.569 (SE 0.202) OLS and 0.992 (0.468)
Bartik IV for the Mexican-born (first-stage F 11.9). For natives it is 0.041 (0.072) and 0.007
(0.090) (Tables 2, 4). Smoothing (Table 5, IV) is the slope of native less-skilled men's log
employment rate on the shock:

- 0.731 (0.138) in metros with a below-median Mexican-born share of the less-skilled population;
- 0.283 (0.072) above the median;
- difference −0.448 (0.155), or −0.431 (0.152) with natives' own industry weights;
- placebo on high-skilled natives: −0.079 (0.151).

In the 2000–06 boom the smoothing difference is −0.111 (0.150) and −0.099 (0.162), not significant
(Table 7). Their structural check (eq. 7, footnote 52: Mexican-born elasticity 1.206, SE 0.300)
predicts a slope gap of −0.29. Our 2006 sample reproduces −0.294 from its own gap in Mexican-born
employment share between the halves (0.245). The authors state the reallocation plainly: "Mexican
mobility therefore provides an implicit form of insurance to native workers by transferring native
employment probability from cities with relatively strong demand to cities experiencing the largest
negative shocks", and "the same smoothing results imply opposite effects for cities experiencing
relatively positive shocks". Table 1 gives annual long-distance mobility of men with high school or
less, 2005–10: Mexican-born 7.0% (arrivals 1.8, internal 3.0, emigration to Mexico 2.3); natives
4.0% (0.2 and 3.8).

**Borjas (2001), "Does Immigration Grease the Wheels of the Labor Market?", BPEA 2001(1):69–133**
[SOURCE: cached `_cache/papers/borjas2001_bpea.txt`, SHA-256 ef893e65…]. The data are the
censuses of 1950–90, by state and five education groups.

- New immigrants' relative supply rises with the relative wage index: 1.150 (0.355); 1.754 (0.373)
  with fixed effects; single decades 0.258 (0.936) and 0.507 (0.556); IV 2.254 (7.936) (Table 3).
- Convergence rises with immigrant penetration: −0.013 (0.006); −0.021 (0.008) with education
  effects; −0.001 (0.005) once period effects are added. There are 20 observations (Table 7).
- The efficiency gain to natives comes from a simulated two-region model ($10tn economy, m = 0.1):
  $2.7–22.0bn a year; central $4.7–7.9bn; $13.2bn if natives never move (Table 8). His summary:
  "the efficiency gain is probably below $10 billion a year" (p. 118).

The discussants in the same issue disagree. Shimer: "The finding goes away in an unweighted
ordinary least-squares regression. It also goes away when a time trend or year fixed effects are
added". Topel: the only gain beyond the conventional surplus is natives' saved migration cost, and
"the forces studied here are, empirically, fairly small".

## 3. Later tests, graded alike

Rubric, applied to every row: A means credible identification of the quoted parameter, a large
sample and robustness shown. B means a reasonable design with one contestable assumption or a narrow
sample. C means the quoted parameter is descriptive, calibrated, or tangential to this channel.
Direction is whether the study supports a sizable insurance or sorting value for natives.

| Study | Population, period | Estimate (SE or t) | Finding for this channel | Grade | Direction |
|---|---|---|---|---|---|
| Cadena & Kovak 2016 (above) | 95 US metros, men HS or less, 2006–10 | smoothing gap −0.448 (0.155) | natives' employment insulated where Mexican share is high | B (pre-trend critique below; boom null) | supports |
| Borjas 2001 (above) | states × education, 1960–90 | convergence −0.013 (0.006); −0.001 (0.005) with period effects | efficiency gain < $10bn/yr, calibrated | C (calibration; convergence fragile) | supports, small |
| Cadena 2013, JHR 48(4) | MSAs ≥150k adults, women 18–54 HS or less, 1990–2000 | IV −0.169 (0.043) to −0.104 (0.024), Table 5 | "for each native woman working due to reform, 0.5 fewer female immigrants enter the local labor force" | B (welfare-participation instrument) | supports responsiveness |
| Cadena 2014, JUE 80 | states, recent low-skilled immigrants, CPS 1994–2007 | −0.815 (0.277) with state trends; −1.407 (0.292) without | "A ten percent increase in a state's minimum wage leads to a roughly eight percent decrease in the number of recently arrived immigrants" | B | supports responsiveness |
| Basso & Peri 2020, JEP 34(3) | states and CZs, 25–64, 1980–2017 | foreign-born 27% of state population adjustment with 11% of population (1980–2000); 36% with 17% (2000–17); no SEs in text | ~2.5× more responsive in 1980–2000; in 2000–17 "the own-population elasticity of the foreign-born to employment became similar to that of natives and rather small" | C (correlations) | supports early, weak late |
| Basso, D'Amuri & Peri 2019, IMF Econ Rev (w25091) | euro area regions 2007–16; US ACS 2007–16 | Europe: 6–7% smaller employment-rate response; US CZs: native slope 0.086 (0.043) high- vs 0.104 (0.029) low-migration | Europe yes; US gap 17% and insignificant | B | mixed |
| Amior 2024, JOLE (CEP DP 1678) | 722 CZs, decades 1960–2010 | population response 0.748 (0.043) → 0.720 (0.040) holding foreign inflows fixed; smoothing interaction +1.159 (0.773); on CK's data with a dynamics control, natives 0.871 (0.441), Mexican-born 0.380 (0.413), weak IV (F 5.5, 1.05) | immigrants 40% of adjustment but "immigration does not significantly accelerate local population adjustment overall, as it crowds out the contribution from internal mobility" | A/B | weak or none |
| Monras 2015, IZA DP 8840 | US MSAs, Great Recession | IV on construction share and household debt | after pre-2006 trends, "natives and immigrants responded similarly to local economic shocks"; adjustment through lower in-migration | B (working paper) | weak or none (for the differential) |
| Autor, Dorn & Hanson 2024, ILR Review (IZA DP 17213) | 722 CZs, China shock, 2000–18 | foreign-born population −4.16 (t −2.01) vs natives −0.88 (t −0.80) per unit exposure | foreign-born 17.5% of the needed adjustment; "the contribution of immigration to labor market adjustment in this episode was small" | A/B (shift-share IV) | responsive, small value |
| Jauer, Liebig, Martin & Puhani 2014, IZA DP 7921 | US states and 532 SuperPUMAs, 2006–11 (all residents) | FE: states −0.021 (0.009); SuperPUMAs −0.006 (0.004) | "the crisis and subsequent sluggish recovery were not accompanied by greater interregional labour mobility" in the US | B/C (not by nativity for the US) | weak |
| Şahin, Song, Topa & Violante 2014, AER (w18265) | 280 local labour markets, 2006–10 | mismatch accounting | "geographical mismatch plays no apparent role" in the unemployment rise | B | weak (bounds the value of relocation) |
| Peri & Zaiour 2023, J Pop Econ | states, CPS 2010–22 | no native mobility response to the post-2019 immigration drop | documents a fall in the Mexican-born working-age population after 2019; not a smoothing test | C for this channel | context |
| Faber, Sarto & Tabellini 2022 (w30048) | CZs, robots and China shock | immigrants' employment effect of robots near zero | "we cannot conclude" on immigrants' mobility | C | none |
| This lane, QCEW replication (§4) | 91–93 metros, 2006–10, 2019–21/22/23, 2012–16 | GR smoothing −0.204 (0.209) OLS; COVID +0.065 (0.239), +0.195 (0.319), +0.267 (0.176); boom −0.025 (0.234) | GR direction replicates, at a quarter of CK's size; none since | B (OLS; IVs weak) | weak today |

Pricing inputs, graded the same way:
- **Davis & von Wachter 2011** (BPEA, w17638) [A]: men ≤50 with ≥3 years' tenure displaced in mass
  layoffs 1980–2005, SSA records. They "lose an average of 1.4 years of pre-displacement earnings" if
  national unemployment is below 6% and "2.8 years" above 8%.
- **Schmieder, von Wachter & Heining 2023** (AER, w30162) [A]: German administrative data. Losses
  are "nearly doubling in size during downturns" of the national cycle.
- **Yagan 2019** (JPE, w23844) [A]: 722 CZs, full-population tax data. A 1pp larger 2007–09 local
  unemployment shock cut 2015 employment by 0.393pp (SE 0.097), "approximately linear in shock
  intensity". There was no significant out-migration response.
- **Ganong & Noel 2019** (AER, w25417) [A]: bank-account data. "Monthly spending drops by 6 percent"
  at job loss and "by 12 percent at UI benefit exhaustion".

**Lean.** Of the 13 external tests:

- 5 support greater immigrant responsiveness or a sizable value: Cadena–Kovak, Borjas, the two
  Cadena papers, and Basso–Peri for 1980–2000;
- 2 are mixed: Basso–D'Amuri–Peri (Europe yes, US no) and Autor–Dorn–Hanson (responsive, small
  contribution);
- 4 find weak or no effect: Amior, Monras, Jauer et al. for the US, and Şahin et al. Basso–Peri's
  own 2000–17 result points the same way;
- 2 are tangential.

The set is balanced. This lane's reading leans to the weak side
for 2024 for three reasons:

- the supportive studies measure responsiveness in 1980–2010;
- the smoothing estimate itself rests on one episode (2006–10), with a pre-trend critique that
  Amior's re-analysis supports;
- our own tests find nothing since.

Same-flaw check (rule 2): weak first stages count against Amior's re-analysis of CK's data (F 5.5 and
1.05), our COVID IVs (F ≤ 3) and our GR above-median IV (F 1.4) alike, and none of the three is used
as evidence. The pre-trend concern is applied to CK (Monras) and to our own COVID estimates (the
2016–19 placebo loads on the COVID shock) alike.

## 4. Our replication: the Great Recession pattern holds, later shocks show none

Data: ACS 1-year persons 2005–2024 on 2013 metros (Geocorr PUMA → county → CBSA). Shocks are the
change in log BLS QCEW payroll employment (place of work, the analogue of the paper's County Business
Patterns). The instruments are Bartik predictions from base-year sector shares and QCEW national
sector changes. Sample rules follow the paper: ≥100,000 adults, ≥60 sampled Mexican-born, no empty
cells. That gives 91–93 metros. [CALCULATION: `ck_tests.py`; full grid in §9]

- **2006–10.** Population response of men with high school or less to the payroll shock (OLS,
  Mexican-share control):
  - Mexico-born 1.193 (0.413);
  - natives −0.125 (0.165);
  - US-born Mexican-origin −0.014 (0.322).

  Reduced form on the Bartik instrument: 7.892 (1.822) against −1.010 (0.565). The differential
  population response replicates. Smoothing of native men's employment rate (OLS) is 0.975 (0.175)
  below the median share against 0.771 (0.114) above, a difference of −0.204 (0.209). The continuous
  gradient is −0.471 (0.825) per unit of Mexican share, a quarter of the paper's −2.0. The
  high-skilled placebo is −0.061 (0.088). Our IV version, −0.997 (0.852), has a first-stage F of 1.4
  in the above-median half and is not used.
- **COVID, 2019–21.** The OLS population response is 0.860 (0.380) for the Mexico-born against 0.413
  (0.187) for natives. But the placebo fails: 2016–19 population change loads on the COVID shock
  (natives 0.681 (0.184), other foreign-born 2.435 (0.380)). The Bartik IVs are weak (F ≤ 3). With
  later end years the Mexico-born response falls below natives' at 2022, 0.301 (0.427) against 0.611
  (0.162), and matches it at 2023, 0.562 (0.432) against 0.513 (0.177). Smoothing differences are
  +0.065 (0.239), +0.195 (0.319) and +0.267 (0.176) for 2021, 2022 and 2023: the wrong sign, and
  none significant.
- **Boom, 2012–16.** The Mexico-born OLS response is 0.320 (0.378) against 0.619 (0.186) for
  natives. The IV is −0.824 (0.772) against 0.473 (0.362), F 16.4. Smoothing difference −0.025
  (0.234).

## 5. Present-day mobility (task 3)

ACS migration in the past year, Cadena–Kovak sample (18–64, not in school or group quarters), SDR
replicate SEs; period means assume independent years. [DATA: `derived/mobility_summary.csv`, from
`acs_extract.py` and `mobility_summary.py`]

| Men with high school or less, % a year (SE) | 2006–10 | 2019–24 | 2024 |
|---|---:|---:|---:|
| Mexico-born: from abroad | 2.11 (0.06) | 1.16 (0.05) | 1.56 (0.11) |
| Mexico-born: between states | 1.62 (0.04) | 0.76 (0.03) | 0.93 (0.09) |
| Mexico-born: either | 3.73 (0.07) | 1.92 (0.06) | 2.49 (0.15) |
| US-born Mexican-origin: either | 2.29 (0.07) | 1.70 (0.05) | 1.47 (0.10) |
| Other natives: either | 2.50 (0.02) | 2.13 (0.02) | 2.01 (0.04) |
| Other foreign-born: either | 4.23 (0.07) | 4.52 (0.07) | 5.70 (0.15) |
| Mexico-born minus other natives, either | +1.23 (0.07) | −0.21 (0.06) | +0.48 (0.16) |
| US-born Mexican-origin minus other natives, either | −0.21 (0.07) | −0.43 (0.05) | −0.54 (0.11) |
| Mexico-born minus other natives, between states | −0.64 (0.05) | −1.15 (0.04) | −0.84 (0.10) |

- **Within the US**, the Mexico-born now move between states at 40% of other natives' rate (0.76%
  against 1.91%). Their long-distance total was below natives' in 2019–24. In 2024 alone it was
  above, +0.48pp, because arrivals from Mexico rose.
- **Across all education levels and both sexes**, long-distance moves in 2019–24 were 2.10% for the
  Mexico-born against 2.79% for other natives. In 2006–10 they were 3.29% against 2.82%.
- **US-born Mexican-origin** members move less than other natives in every period.
- **Return migration to Mexico** is not in the ACS. We measure it as ENADID five-year counts of
  returned men over ACS Mexico-born men with high school or less, aged 18–59, five years earlier:
  0.95% a year for 2013–18 and 0.78% for 2018–23. Cadena–Kovak's Table 1 has 2.3% for 2005–10.
  Adding it leaves the Mexico-born about 0.58pp a year above other natives today (−0.21 + 0.78),
  against about 3.5pp in 2005–10 (+1.23 + 2.3). This is approximate: the two surveys differ, and
  the ages are mismatched by three years.
  [CALCULATION: `price_insurance.py` `return_rates()`, from
  `enadid_return_selectivity_2026_09_22/derived/return_migrants_by_schooling.csv`]
- **The highly mobile group today** is other recent immigrants (other foreign-born 5.70% in 2024),
  who are outside this account's group.
- **Employment of those who stay.** Mexico-born men with high school or less kept their employment
  rate better than other natives in the Great Recession: 86.5% to 83.3% (−3.2pp), against 69.6% to
  64.8% (−4.8pp) for other natives. They adjusted by leaving. In 2019–21 the two fell alike (−3.1
  and −2.5pp). [DATA: `derived/employment_cyclicality.csv`; SEs 0.1–0.3pp]

**Answer to task 3.** No. In 2019–24 the Mexico-born moved within the US less than other natives,
and US-born members of the group moved less still. Their total, counting arrivals and returns to
Mexico, exceeds natives' by about a sixth of the 2006–10 margin.

## 6. Pricing the insurance (task 2)

**Method.** The script works metro by metro and compares the 2006–10 shock with and without the
group. The change in other-native employment rates attributable to the group is g · x · s. Here s is
the metro's QCEW shock less its employment-weighted mean: moving between metros cannot smooth the
common national shock. x is the Mexican-born share, and g is the change in natives' slope per unit
share. Cadena–Kovak's −0.448 over our halves' share gap (0.224) gives g = −2.0 (SE 0.69). The paper
does not print its halves' means. [CALCULATION: `price_insurance.py`]

- Jobs are g · x · s times base-year employed other-native men with high school or less. These are
  the account's other residents (15.7m in all metros).
- Each job is valued at the metro's 2006 annual wage for those men, in 2024 dollars (CPI-U; $56.5k
  on average).
- "Kept" sums the metros whose shock was worse than average. "Forgone" sums the milder ones, where
  natives gain fewer jobs because the Mexican-born move in or stay. The net is their difference.

**Episode values, central (CK Table 5b, all 355 metros).** 61,000 jobs are kept where the shock was
worst and 50,000 forgone where it was mild. That is $3.68bn and $2.77bn of earnings per year of the
gap, net $0.91bn (SE 0.31, from g alone). The net is positive only because, weighted by employment,
the metros with more Mexican-born workers were hit harder than average in 2006–10: Los Angeles,
Riverside, Phoenix and Las Vegas outweigh the growing Texas border metros. (Unweighted, share and
shock correlate at +0.20 in the 91-metro sample.) It depends on which metros count: in the paper's 91-metro sample the net is $0.36bn, and with the paper's structural
slope it is −158 jobs. Read the first-order effect as a reallocation of about 50–60 thousand jobs
with a small, fragile net.

**Annualising over a cycle.** Each endpoint job is counted as D job-years: 2.5 during the 2007–10
build-up, plus 0, 2.5 or 5 years after 2010. The high case follows Yagan's finding that 2007–09
local gaps persisted to 2015. D is therefore 2.5, 5 or 7.5, spread over a cycle of L = 12, 10 or 8
years; NBER peaks fall in 1990, 2001, 2007 and 2020. [ASSUMPTION] Central D/L = 0.5.

| CK Table 5b, all metros, other-native men, D 5, L 10 | $bn a year |
|---|---:|
| Earnings kept in the hardest-hit metros (gross protection) | 1.84 |
| Earnings forgone in milder metros | 1.38 |
| Net, first order (ρ = 1) | 0.45 (SE 0.16) |
| Welfare with a forgone job worth ρ = 0.75 of a kept one (central) | 0.80 |
| Welfare at ρ = 0.5, Davis–von Wachter's national recession/expansion ratio used across metros | 1.15 |
| Upper bound, forgone jobs costless (ρ = 0) | 1.84 |
| Risk-premium alternative, 0.5 γ ΔVar × earnings, γ = 1, 2, 3 | 0.13, 0.27, 0.40 |
| Taxes on the net earnings change at the account's low-skill marginal rate 0.384 | 0.17 |
| Taxes on gross protection (offset by the forgone side) | 0.71 |

**Why ρ, and why 0.75.** Under expected utility a job is worth the same wherever it is kept or lost.
Any value beyond the net therefore needs a lost job to cost more where the shock is severe. Two
sources pull in opposite directions:

- Davis–von Wachter and Schmieder et al. find displacement losses double between national
  expansions and recessions (ρ = 0.5).
- Yagan finds the persistence of local employment gaps "approximately linear in shock intensity"
  across areas within one recession (ρ = 1).

The central 0.75 is the midpoint. [ASSUMPTION]

The risk-premium line treats each metro's employment change as everyone's consumption change. Actual
spending falls 6% at job loss (Ganong–Noel), so it is an upper bound on a different concept and is
not added.

**Range at 2006–10 mobility: $0.04–3.03bn.** The low end takes ρ = 1, the short gap and the long
cycle, over the paper's three men's specifications and both metro sets. The high end takes ρ = 0.5,
the long gap and the short cycle, and adds other foreign-born men and native women (eq. 7 with the
paper's Table 3 elasticities for women, g = −0.58). Our own Great Recession OLS gradient (−0.47)
gives about a quarter of the central. The central uses the paper's estimate and so leans generous.

**Present day.** The 2006–10 values are scaled by how much of the group's excess mobility remains.
Long-distance excess plus return migration now stands at 0.58pp against 3.53pp, a factor of 0.16
(central). The low end is 0: our COVID and boom tests find no smoothing. The high end is 0.34, the
COVID OLS population-elasticity gap relative to 2006–10, which fails its placebo. Present-day
insurance is **$0.13bn (0–1.03)**. [INFERENCE: the scaling assumes smoothing is proportional to excess
mobility]

## 7. Borjas's efficiency gain, restated for 2024

The model is reproduced before use. [CALCULATION: `borjas_model.py`] It has two regions with
Q = A L^0.7 and natives adjusting with a lag at quadratic moving cost. The gain is
r × [PV(θ = 1) − PV(θ = λ)] (eq. 34). Three choices were fixed by matching the printed Table 8:

- a 100-period horizon;
- exact mover counts;
- a 0.1 grid for σ.

With these, 11 of the 12 printed cells come within 0.1bn. The twelfth, printed 12.4, lies between
the 0.1-grid (13.45) and 0.01-grid (11.42) optima (§9).

**2024 inputs.** GDP is $29.30tn (BEA NIPA T1.1.5, vintage published 26 August 2026). There are
6,857,152 employed Mexico-born and 146,437,472 other workers (ACS 2024), so m = 0.0468 (Borjas used
0.1).

**Sorting.** States are ranked by the mean log full-time wage of US-born workers with high school or
less. The high-wage states holding λ = 41% of those workers include CA, AZ, NV, IL, CO, WA and NJ;
TX is not among them. They hold 60.2% of Mexico-born workers with high school or less (θ). At λ = 30%
θ is 0.470; at 45% it is 0.612. The observed log wage gap is 0.147, against the model's 0.122.
[DATA: `derived/borjas_2024_inputs.json`, `derived/borjas_state_sorting.csv`]

| 2024, Mexico-born, $bn a year (0.01 grid) | Low cost | Medium | High | Prohibitive |
|---|---:|---:|---:|---:|
| As defined, θ = 1: λ 0.45 / 0.40 / 0.30 | 3.41 / 4.45 / 6.50 | 4.34 / 5.58 / 8.18 | 5.34 / 6.79 / 10.03 | 7.54 / 9.72 / 16.61 |
| Observed 2024 θ: λ 0.45 / 0.40 / 0.30 | 0.30 / 0.41 / 0.18 | 0.38 / 0.52 / 0.30 | 0.46 / 0.71 / 0.44 | 0.74 / 1.32 / 1.43 |

- **Central.** At λ 0.40 and medium cost the gain is $5.58bn as defined and $0.52bn at the observed
  location. The account compares the US with and without the group, so the observed-location number
  is the relevant one.
- **Recent arrivals** (2019–24, m = 0.0047): at most $0.2bn as defined and about zero as observed.
- **The union scenario** is reported in §9 but not used. It treats US-born members as sorting like
  new immigrants (m = 0.131, $23–102bn as defined), and their location was never measured that way.
- **Caveats.** Wages are nominal, so part of the high-wage states' premium is housing cost. The model
  needs regional diminishing returns with fixed regional factors.

## 8. Overlap ruling (task 4)

The account's production term P, with induced receipts F ($8.8–13.3bn), is one national CES
economy. It has constant returns, capital that adjusts, native labour supply fixed in the central
case, and no regions or shocks. It cannot contain either channel.

- **Local-shock insurance.** Not in P, since P has no local shocks. At first order it moves native
  jobs from milder metros to the hardest-hit ones. Only the convexity or risk value and a small,
  fragile net remain. **Ruling: beside the account as a social benefit.** The fiscal part is the tax
  on the net earnings change ($0.17bn at 2006–10 mobility, $0.03bn today). Unemployment insurance
  and other transfers move with the jobs, so they net to about zero across metros too. A stationary
  2024 account has no recession year for anyone. If a cycle-averaged account were built, this slice
  would add to it.
- **The group's own cyclical transfers**, the mirror item under rule 5, give no sign to add. Those
  who stayed in 2006–10 kept their employment rate better than other natives (−3.2 against −4.8pp)
  because others left, and many are ineligible for unemployment insurance. [DATA; INFERENCE]
- **Borjas's gain.** Not in P, since P has no regions. It needs regional diminishing returns with
  fixed regional capital or land. The account instead lets capital adjust, which by itself would
  close regional gaps, so the gain is at most the observed-location $0.52bn. **Ruling: beside the
  account as a social benefit.** Taxing it at the account's 0.384 rate would give about $0.2bn of
  receipts. The rate is the account's labour rate applied to all of the gain, which is approximate.
- **National buffer.** Busts bring more emigration and fewer arrivals, which lowers national
  low-skill labour supply. Cross-metro designs cannot identify this: it sits in the regression
  constant. Whether it raises natives' employment depends on whether departing workers take their
  jobs and spending with them. **Unpriced and flagged.**
- **Other benefit lanes.** Nothing here double counts with scale spillovers, care and household
  services, or construction and housing supply:
  - scale spillovers price density externalities, a level effect, while Borjas's gain rests on
    diminishing regional returns. If both are used, reconcile the city wage premium, which feeds
    each.
  - care and household services price induced native hours;
  - construction and housing supply price building capacity. The 2006–10 smoothing was largely a
    construction bust, but it is a cyclical reallocation of employment, not capacity.
- **Cost lanes.** No overlap with congestion, crime, housing or the distribution lane's wage
  transfer, which is a level effect inside the account's CES. The jobs forgone in milder metros are
  already netted here.

## 9. Every specification computed

Full grids: `derived/ck_population.csv` (all groups, both sexes and education levels, OLS, reduced
form and IV, with and without the Mexican-share control); `derived/ck_smoothing.csv`;
`derived/insurance_episode.csv` and `derived/insurance_annual.csv` (every D, L, ρ and γ, both metro
sets, with and without other foreign-born beneficiaries); `derived/borjas_2024.csv`. The tables below
are printed by `result_tables.py` from those files.

### 1 Population responses

| Period | Spec | Natives | Mexico-born | US-born Mexican-origin | Other natives | First-stage F (Mexico-born) |
|---|---|---:|---:|---:|---:|---:|
| GR_2006_2010 | OLS_qcew | -0.125 (0.165) | 1.193 (0.413) | -0.014 (0.322) | -0.247 (0.183) |  |
| GR_2006_2010 | OLS_acs | 0.058 (0.141) | 1.410 (0.383) | 0.197 (0.280) | -0.106 (0.176) |  |
| GR_2006_2010 | RF_bartik_qcew | -1.010 (0.565) | 7.892 (1.822) | 4.684 (2.060) | -2.035 (0.538) |  |
| GR_2006_2010 | IV_qcew_by_bartik_qcew | -0.565 (0.350) | 3.853 (1.900) | 1.559 (0.906) | -1.210 (0.479) | 5.2 |
| GR_2006_2010 | RF_bartik_acs | -0.652 (0.660) | 7.045 (1.687) | 4.783 (1.894) | -1.928 (0.684) |  |
| GR_2006_2010 | IV_qcew_by_bartik_acs | -0.421 (0.433) | 4.146 (2.527) | 1.878 (1.088) | -1.378 (0.671) | 2.7 |
| COVID_2019_2021 | OLS_qcew | 0.413 (0.187) | 0.860 (0.380) | 0.606 (0.500) | 0.366 (0.217) |  |
| COVID_2019_2021 | OLS_acs | 0.403 (0.173) | 0.362 (0.322) | 0.547 (0.364) | 0.374 (0.231) |  |
| COVID_2019_2021 | RF_bartik_qcew | 1.255 (0.731) | 0.472 (1.468) | 3.098 (2.128) | 0.911 (0.699) |  |
| COVID_2019_2021 | IV_qcew_by_bartik_qcew | 5.084 (15.641) | 0.495 (1.447) | 2.820 (2.810) | 10.475 (102.318) | 2.6 |
| COVID_2019_2021 | RF_bartik_acs | 0.830 (0.501) | 0.034 (1.022) | 3.222 (1.450) | 0.361 (0.490) |  |
| COVID_2019_2021 | IV_qcew_by_bartik_acs | -3.548 (9.676) | 0.163 (4.686) | 7.974 (10.657) | -1.067 (2.818) | 0.2 |
| COVID_2019_2022 | OLS_qcew | 0.611 (0.162) | 0.301 (0.427) | 0.286 (0.467) | 0.654 (0.181) |  |
| COVID_2019_2022 | OLS_acs | 0.720 (0.142) | 0.178 (0.328) | 0.763 (0.314) | 0.727 (0.162) |  |
| COVID_2019_2022 | RF_bartik_qcew | -1.127 (1.061) | -0.137 (2.875) | -1.466 (3.465) | -1.154 (1.005) |  |
| COVID_2019_2022 | IV_qcew_by_bartik_qcew | 1.897 (2.762) | 0.137 (2.820) | 2.372 (6.373) | 1.885 (2.554) | 0.8 |
| COVID_2019_2022 | RF_bartik_acs | -1.073 (0.730) | 1.603 (1.462) | -0.629 (2.303) | -1.174 (0.721) |  |
| COVID_2019_2022 | IV_qcew_by_bartik_acs | 1.175 (0.825) | -2.024 (2.353) | 1.794 (6.946) | 1.174 (0.744) | 2.6 |
| COVID_2019_2023 | OLS_qcew | 0.513 (0.177) | 0.562 (0.432) | 0.120 (0.619) | 0.606 (0.179) |  |
| COVID_2019_2023 | OLS_acs | 0.605 (0.136) | 0.770 (0.308) | 0.453 (0.411) | 0.682 (0.146) |  |
| COVID_2019_2023 | RF_bartik_qcew | -3.109 (1.682) | -4.431 (4.199) | -1.539 (5.510) | -3.784 (1.784) |  |
| COVID_2019_2023 | IV_qcew_by_bartik_qcew | 1.945 (1.586) | 1.691 (1.493) | 0.733 (2.474) | 2.489 (2.017) | 1.9 |
| COVID_2019_2023 | RF_bartik_acs | -1.139 (1.126) | -0.265 (2.043) | 1.443 (3.080) | -2.009 (1.318) |  |
| COVID_2019_2023 | IV_qcew_by_bartik_acs | 0.648 (0.606) | 0.135 (1.027) | -0.916 (2.095) | 1.126 (0.704) | 8.1 |
| BOOM_2012_2016 | OLS_qcew | 0.619 (0.186) | 0.320 (0.378) | 1.183 (0.589) | 0.518 (0.195) |  |
| BOOM_2012_2016 | OLS_acs | 0.401 (0.157) | 0.857 (0.318) | -0.090 (0.564) | 0.460 (0.169) |  |
| BOOM_2012_2016 | RF_bartik_qcew | 1.934 (1.446) | -2.638 (2.393) | 4.698 (5.245) | 1.572 (1.421) |  |
| BOOM_2012_2016 | IV_qcew_by_bartik_qcew | 0.473 (0.362) | -0.824 (0.772) | 1.312 (1.342) | 0.378 (0.349) | 16.4 |
| BOOM_2012_2016 | RF_bartik_acs | 1.172 (1.414) | -2.259 (2.131) | -0.457 (3.645) | 1.581 (1.437) |  |
| BOOM_2012_2016 | IV_qcew_by_bartik_acs | 0.423 (0.508) | -1.196 (1.348) | -0.214 (1.733) | 0.550 (0.501) | 4.9 |

Placebo, 2016-2019 population change on the COVID shocks:

| Period | Spec | Natives | Mexico-born | US-born Mexican-origin | Other foreign-born |
|---|---|---:|---:|---:|---:|
| COVID_2019_2021 | PLACEBO_prechange_on_qcew | 0.681 (0.184) | 0.253 (0.349) | 0.202 (0.501) | 2.435 (0.380) |
| COVID_2019_2021 | PLACEBO_prechange_on_bartik_qcew | -2.267 (1.144) | -2.239 (1.917) | -1.788 (3.224) | -4.285 (3.287) |
| COVID_2019_2022 | PLACEBO_prechange_on_qcew | 0.631 (0.160) | 0.315 (0.329) | 0.304 (0.458) | 2.455 (0.371) |
| COVID_2019_2022 | PLACEBO_prechange_on_bartik_qcew | -2.178 (1.310) | -3.750 (2.199) | 0.318 (4.406) | -9.734 (3.308) |

### 2 Smoothing

| Period | Panel | Spec | Below median | Above median | Difference | Gradient per unit eta | F (below, above) |
|---|---|---|---:|---:|---:|---:|---|
| GR_2006_2010 | a_all_lowed_men | bartik_qcew_lowmen | 1.624 (0.268) | -6.870 (47.650) | -8.494 (47.651) | 1.417 (5.111) | 25.3, 0.0 |
| GR_2006_2010 | a_all_lowed_men | bartik_qcew | 1.479 (0.280) | 0.954 (0.439) | -0.525 (0.520) | -1.861 (1.338) | 21.7, 1.7 |
| GR_2006_2010 | a_all_lowed_men | ols | 0.984 (0.150) | 0.652 (0.109) | -0.332 (0.185) | -1.047 (0.699) |  |
| GR_2006_2010 | b_native_lowed_men | bartik_qcew_lowmen | 1.673 (0.328) | -2.198 (17.909) | -3.870 (17.912) | 0.827 (5.399) | 19.2, 0.0 |
| GR_2006_2010 | b_native_lowed_men | bartik_qcew | 1.413 (0.331) | 0.416 (0.785) | -0.997 (0.852) | -2.002 (1.708) | 19.2, 1.4 |
| GR_2006_2010 | b_native_lowed_men | ols | 0.975 (0.175) | 0.771 (0.114) | -0.204 (0.209) | -0.471 (0.825) |  |
| GR_2006_2010 | b1_oth_nb_lowed_men | bartik_qcew_lowmen | 1.805 (0.345) | -0.184 (2.320) | -1.989 (2.345) | 10.899 (48.508) | 18.4, 0.4 |
| GR_2006_2010 | b1_oth_nb_lowed_men | bartik_qcew | 1.483 (0.355) | 0.513 (1.486) | -0.971 (1.527) | -0.959 (3.339) | 18.7, 0.4 |
| GR_2006_2010 | b1_oth_nb_lowed_men | ols | 0.962 (0.182) | 0.724 (0.129) | -0.238 (0.223) | -0.256 (1.025) |  |
| GR_2006_2010 | b2_mex_nb_lowed_men | bartik_qcew_lowmen | -0.827 (1.558) | 2.346 (2.861) | 3.173 (3.258) | 4.384 (8.547) | 18.2, 0.5 |
| GR_2006_2010 | b2_mex_nb_lowed_men | bartik_qcew | -0.341 (1.155) | 0.595 (0.598) | 0.936 (1.301) | 1.969 (3.868) | 23.3, 7.5 |
| GR_2006_2010 | b2_mex_nb_lowed_men | ols | 1.545 (0.440) | 0.932 (0.216) | -0.613 (0.490) | -2.713 (1.306) |  |
| GR_2006_2010 | b3_native_lowed_women | bartik_qcew_lowmen | 1.333 (0.334) | 0.892 (3.565) | -0.441 (3.581) | -2.036 (2.957) | 21.1, 0.1 |
| GR_2006_2010 | b3_native_lowed_women | bartik_qcew | 1.002 (0.222) | -0.467 (1.235) | -1.469 (1.255) | -2.653 (1.611) | 19.5, 1.3 |
| GR_2006_2010 | b3_native_lowed_women | ols | 0.668 (0.148) | 0.618 (0.204) | -0.050 (0.252) | -0.677 (1.212) |  |
| GR_2006_2010 | d_native_highed_men | bartik_qcew_lowmen | 0.394 (0.202) | 0.598 (0.625) | 0.204 (0.657) | -0.996 (4.038) | 23.7, 0.6 |
| GR_2006_2010 | d_native_highed_men | bartik_qcew | 0.447 (0.132) | -0.282 (1.069) | -0.729 (1.077) | -1.106 (0.907) | 22.6, 0.5 |
| GR_2006_2010 | d_native_highed_men | ols | 0.359 (0.071) | 0.299 (0.053) | -0.061 (0.088) | -0.345 (0.351) |  |
| COVID_2019_2021 | a_all_lowed_men | bartik_qcew_lowmen | -0.538 (4.380) | 1.321 (0.489) | 1.859 (4.407) | 5.406 (10.415) | 0.2, 4.8 |
| COVID_2019_2021 | a_all_lowed_men | bartik_qcew | 0.518 (0.676) | 1.176 (0.668) | 0.658 (0.950) | 1.962 (4.369) | 1.6, 1.5 |
| COVID_2019_2021 | a_all_lowed_men | ols | 0.811 (0.190) | 0.717 (0.148) | -0.094 (0.241) | -0.578 (1.021) |  |
| COVID_2019_2021 | b_native_lowed_men | bartik_qcew_lowmen | -12.824 (88.812) | 1.309 (0.607) | 14.132 (88.814) | 30.616 (99.158) | 0.0, 3.8 |
| COVID_2019_2021 | b_native_lowed_men | bartik_qcew | -0.718 (1.672) | 0.993 (0.665) | 1.711 (1.800) | 6.693 (6.525) | 1.2, 1.7 |
| COVID_2019_2021 | b_native_lowed_men | ols | 0.664 (0.182) | 0.729 (0.154) | 0.065 (0.239) | 0.263 (1.053) |  |
| COVID_2019_2021 | b1_oth_nb_lowed_men | bartik_qcew_lowmen | -15.954 (121.246) | 1.121 (0.740) | 17.075 (121.248) | 113.745 (1393.026) | 0.0, 3.2 |
| COVID_2019_2021 | b1_oth_nb_lowed_men | bartik_qcew | -0.774 (1.731) | 0.515 (0.913) | 1.289 (1.957) | 5.135 (8.275) | 1.2, 1.7 |
| COVID_2019_2021 | b1_oth_nb_lowed_men | ols | 0.669 (0.170) | 0.917 (0.233) | 0.248 (0.288) | 1.979 (1.508) |  |
| COVID_2019_2021 | b2_mex_nb_lowed_men | bartik_qcew_lowmen | 4.858 (21.316) | 1.471 (1.035) | -3.387 (21.341) | -2.981 (14.166) | 0.0, 4.3 |
| COVID_2019_2021 | b2_mex_nb_lowed_men | bartik_qcew | -1.379 (10.411) | 1.680 (1.358) | 3.059 (10.500) | -0.006 (9.261) | 0.1, 1.7 |
| COVID_2019_2021 | b2_mex_nb_lowed_men | ols | 0.342 (0.486) | 0.449 (0.204) | 0.106 (0.528) | -1.084 (2.058) |  |
| COVID_2019_2021 | b3_native_lowed_women | bartik_qcew_lowmen | 3.991 (12.681) | 1.138 (1.172) | -2.854 (12.735) | -10.713 (36.899) | 0.1, 4.2 |
| COVID_2019_2021 | b3_native_lowed_women | bartik_qcew | 1.089 (1.041) | 0.017 (0.881) | -1.071 (1.364) | -7.447 (7.068) | 1.4, 2.0 |
| COVID_2019_2021 | b3_native_lowed_women | ols | 0.641 (0.211) | 0.775 (0.172) | 0.134 (0.272) | 0.299 (1.239) |  |
| COVID_2019_2021 | d_native_highed_men | bartik_qcew_lowmen | 0.328 (1.583) | 0.434 (0.533) | 0.105 (1.671) | 0.302 (7.292) | 0.1, 1.6 |
| COVID_2019_2021 | d_native_highed_men | bartik_qcew | 0.368 (0.468) | 1.156 (2.038) | 0.788 (2.091) | 1.666 (6.108) | 1.4, 0.3 |
| COVID_2019_2021 | d_native_highed_men | ols | 0.410 (0.144) | 0.251 (0.125) | -0.159 (0.191) | -0.866 (0.905) |  |
| COVID_2019_2022 | a_all_lowed_men | bartik_qcew_lowmen | 0.085 (1.423) | -192.547 (31323.496) | -192.632 (31323.496) | 59.181 (968.292) | 0.5, 0.0 |
| COVID_2019_2022 | a_all_lowed_men | bartik_qcew | 0.257 (0.840) | -0.232 (0.861) | -0.488 (1.203) | -0.204 (2.946) | 1.0, 1.1 |
| COVID_2019_2022 | a_all_lowed_men | ols | 0.253 (0.163) | 0.384 (0.234) | 0.131 (0.286) | 0.439 (1.191) |  |
| COVID_2019_2022 | b_native_lowed_men | bartik_qcew_lowmen | -2.224 (6.632) | -19.390 (512.477) | -17.166 (512.520) | 27.271 (110.241) | 0.2, 0.0 |
| COVID_2019_2022 | b_native_lowed_men | bartik_qcew | -0.855 (2.451) | 0.398 (1.593) | 1.253 (2.923) | 1.824 (5.384) | 0.6, 0.5 |
| COVID_2019_2022 | b_native_lowed_men | ols | 0.234 (0.178) | 0.430 (0.265) | 0.195 (0.319) | 0.571 (1.446) |  |
| COVID_2019_2022 | b1_oth_nb_lowed_men | bartik_qcew_lowmen | -1.836 (5.820) | -3.768 (16.082) | -1.932 (17.103) | 24.030 (38.977) | 0.2, 0.1 |
| COVID_2019_2022 | b1_oth_nb_lowed_men | bartik_qcew | -0.609 (2.031) | 0.518 (2.077) | 1.127 (2.905) | 6.228 (14.535) | 0.6, 0.3 |
| COVID_2019_2022 | b1_oth_nb_lowed_men | ols | 0.222 (0.175) | 0.414 (0.307) | 0.192 (0.353) | 1.213 (2.071) |  |
| COVID_2019_2022 | b2_mex_nb_lowed_men | bartik_qcew_lowmen | -9.123 (53.696) | 0.196 (2.951) | 9.318 (53.778) | 5.629 (7.983) | 0.0, 0.2 |
| COVID_2019_2022 | b2_mex_nb_lowed_men | bartik_qcew | 7.131 (27.872) | 0.928 (1.891) | -6.202 (27.936) | -7.667 (27.564) | 0.0, 0.9 |
| COVID_2019_2022 | b2_mex_nb_lowed_men | ols | 0.197 (0.567) | 0.543 (0.320) | 0.346 (0.651) | -1.077 (2.251) |  |
| COVID_2019_2022 | b3_native_lowed_women | bartik_qcew_lowmen | 2.037 (2.649) | -19.625 (469.802) | -21.662 (469.809) | 4.132 (38.629) | 0.3, 0.0 |
| COVID_2019_2022 | b3_native_lowed_women | bartik_qcew | 0.914 (1.202) | -0.284 (1.976) | -1.199 (2.313) | -0.248 (3.701) | 0.7, 0.4 |
| COVID_2019_2022 | b3_native_lowed_women | ols | 0.320 (0.204) | 0.409 (0.172) | 0.090 (0.267) | 1.003 (1.159) |  |
| COVID_2019_2022 | d_native_highed_men | bartik_qcew_lowmen | 0.301 (0.517) | -0.090 (0.815) | -0.391 (0.965) | -2.149 (12.662) | 0.7, 0.3 |
| COVID_2019_2022 | d_native_highed_men | bartik_qcew | 0.707 (0.684) | 0.408 (0.445) | -0.299 (0.816) | 0.466 (2.915) | 0.8, 1.6 |
| COVID_2019_2022 | d_native_highed_men | ols | 0.142 (0.083) | 0.140 (0.081) | -0.002 (0.116) | 0.011 (0.610) |  |
| COVID_2019_2023 | a_all_lowed_men | bartik_qcew_lowmen | 1.827 (4.506) | 2.535 (12.224) | 0.708 (13.028) | -12.471 (74.239) | 0.2, 0.0 |
| COVID_2019_2023 | a_all_lowed_men | bartik_qcew | 0.761 (0.671) | 0.478 (0.450) | -0.283 (0.808) | 1.014 (3.035) | 1.8, 2.1 |
| COVID_2019_2023 | a_all_lowed_men | ols | 0.113 (0.115) | 0.248 (0.094) | 0.135 (0.149) | 0.694 (0.659) |  |
| COVID_2019_2023 | b_native_lowed_men | bartik_qcew_lowmen | -1.634 (8.848) | 0.357 (5.490) | 1.991 (10.413) | 4.499 (24.813) | 0.0, 0.0 |
| COVID_2019_2023 | b_native_lowed_men | bartik_qcew | -0.138 (0.882) | 1.544 (1.454) | 1.683 (1.701) | 7.045 (7.731) | 1.3, 1.2 |
| COVID_2019_2023 | b_native_lowed_men | ols | 0.032 (0.115) | 0.299 (0.133) | 0.267 (0.176) | 1.456 (0.879) |  |
| COVID_2019_2023 | b1_oth_nb_lowed_men | bartik_qcew_lowmen | -0.585 (4.521) | -35.559 (3566.101) | -34.974 (3566.104) | 5.902 (26.190) | 0.0, 0.0 |
| COVID_2019_2023 | b1_oth_nb_lowed_men | bartik_qcew | 0.092 (0.896) | 2.186 (2.114) | 2.093 (2.296) | 18.945 (33.964) | 1.3, 1.1 |
| COVID_2019_2023 | b1_oth_nb_lowed_men | ols | 0.035 (0.117) | 0.360 (0.197) | 0.325 (0.229) | 1.954 (1.462) |  |
| COVID_2019_2023 | b2_mex_nb_lowed_men | bartik_qcew_lowmen | 16.748 (96.804) | -0.483 (2.594) | -17.232 (96.839) | 13.208 (31.441) | 0.0, 0.2 |
| COVID_2019_2023 | b2_mex_nb_lowed_men | bartik_qcew | -13.862 (61.481) | 0.830 (0.944) | 14.691 (61.488) | 7.137 (7.325) | 0.1, 1.3 |
| COVID_2019_2023 | b2_mex_nb_lowed_men | ols | -0.023 (0.460) | 0.308 (0.159) | 0.331 (0.487) | 1.006 (1.568) |  |
| COVID_2019_2023 | b3_native_lowed_women | bartik_qcew_lowmen | 5.612 (18.408) | 13.175 (72.477) | 7.563 (74.778) | -3.483 (74.745) | 0.1, 0.0 |
| COVID_2019_2023 | b3_native_lowed_women | bartik_qcew | 1.358 (1.288) | -1.382 (1.630) | -2.740 (2.077) | -9.129 (7.708) | 1.5, 1.0 |
| COVID_2019_2023 | b3_native_lowed_women | ols | 0.201 (0.190) | 0.109 (0.176) | -0.092 (0.259) | 0.297 (1.154) |  |
| COVID_2019_2023 | d_native_highed_men | bartik_qcew_lowmen | 0.385 (0.645) | -62.621 (8496.182) | -63.007 (8496.182) | -17.628 (90.959) | 0.3, 0.0 |
| COVID_2019_2023 | d_native_highed_men | bartik_qcew | 0.469 (0.351) | 0.538 (0.391) | 0.069 (0.526) | 2.298 (3.546) | 1.7, 3.0 |
| COVID_2019_2023 | d_native_highed_men | ols | 0.111 (0.055) | 0.082 (0.092) | -0.029 (0.108) | 0.073 (0.496) |  |
| BOOM_2012_2016 | a_all_lowed_men | bartik_qcew_lowmen | -0.839 (1.153) | 0.611 (0.246) | 1.450 (1.179) | 11.612 (12.859) | 1.3, 18.9 |
| BOOM_2012_2016 | a_all_lowed_men | bartik_qcew | -0.001 (0.280) | 0.862 (0.283) | 0.863 (0.398) | 4.208 (2.496) | 13.1, 16.5 |
| BOOM_2012_2016 | a_all_lowed_men | ols | 0.232 (0.119) | 0.157 (0.142) | -0.074 (0.185) | -0.414 (0.739) |  |
| BOOM_2012_2016 | b_native_lowed_men | bartik_qcew_lowmen | -0.603 (0.811) | 0.676 (0.344) | 1.279 (0.881) | 10.348 (9.326) | 1.5, 20.0 |
| BOOM_2012_2016 | b_native_lowed_men | bartik_qcew | -0.016 (0.267) | 1.047 (0.469) | 1.063 (0.540) | 5.992 (3.106) | 13.7, 14.5 |
| BOOM_2012_2016 | b_native_lowed_men | ols | 0.200 (0.120) | 0.175 (0.201) | -0.025 (0.234) | 0.222 (1.067) |  |
| BOOM_2012_2016 | b1_oth_nb_lowed_men | bartik_qcew_lowmen | -0.686 (0.933) | 0.594 (0.384) | 1.280 (1.009) | 10.217 (12.155) | 1.3, 20.4 |
| BOOM_2012_2016 | b1_oth_nb_lowed_men | bartik_qcew | 0.001 (0.279) | 0.788 (0.422) | 0.787 (0.506) | 4.512 (3.540) | 12.5, 13.5 |
| BOOM_2012_2016 | b1_oth_nb_lowed_men | ols | 0.206 (0.120) | 0.118 (0.212) | -0.087 (0.243) | -0.697 (1.049) |  |
| BOOM_2012_2016 | b2_mex_nb_lowed_men | bartik_qcew_lowmen | 0.291 (0.684) | 1.162 (0.577) | 0.871 (0.895) | 11.672 (9.917) | 24.5, 15.5 |
| BOOM_2012_2016 | b2_mex_nb_lowed_men | bartik_qcew | 0.220 (0.647) | 1.924 (0.870) | 1.704 (1.084) | 9.968 (8.579) | 66.5, 11.1 |
| BOOM_2012_2016 | b2_mex_nb_lowed_men | ols | 0.352 (0.500) | 0.357 (0.343) | 0.005 (0.607) | 3.331 (3.072) |  |
| BOOM_2012_2016 | b3_native_lowed_women | bartik_qcew_lowmen | -1.034 (1.405) | 0.253 (0.497) | 1.288 (1.490) | 9.711 (12.922) | 1.6, 20.3 |
| BOOM_2012_2016 | b3_native_lowed_women | bartik_qcew | -0.243 (0.470) | 0.296 (0.837) | 0.539 (0.960) | 3.125 (4.347) | 13.3, 14.9 |
| BOOM_2012_2016 | b3_native_lowed_women | ols | 0.218 (0.243) | 0.040 (0.256) | -0.178 (0.353) | -0.802 (1.497) |  |
| BOOM_2012_2016 | d_native_highed_men | bartik_qcew_lowmen | -0.357 (1.621) | -0.044 (0.122) | 0.313 (1.626) | 6.881 (35.379) | 0.2, 24.8 |
| BOOM_2012_2016 | d_native_highed_men | bartik_qcew | 0.280 (0.199) | 0.356 (0.207) | 0.076 (0.287) | 0.801 (1.402) | 8.1, 17.1 |
| BOOM_2012_2016 | d_native_highed_men | ols | 0.139 (0.065) | 0.113 (0.089) | -0.026 (0.110) | 0.306 (0.480) |  |

### 3 Pricing per episode

| Spec | Shock period | Metros | g per unit share (SE) | Jobs kept (bust) | Jobs forgone (mild) | Net jobs | Kept $bn | Forgone $bn | Net $bn (SE) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| CK_T5b_IV | GR_2006_2010 | all_metros (355) | -2.000 (0.692) | 61,032 | 50,161 | 10,870 | 3.68 | 2.77 | 0.91 (0.31) |
| CK_T5b_IV | GR_2006_2010 | ck_sample (91) | -2.000 (0.692) | 48,456 | 46,946 | 1,510 | 2.98 | 2.62 | 0.36 (0.12) |
| CK_T5c_IV_native_shock | GR_2006_2010 | all_metros (355) | -1.924 (0.679) | 58,716 | 48,258 | 10,458 | 3.54 | 2.66 | 0.87 (0.31) |
| CK_T5c_IV_native_shock | GR_2006_2010 | ck_sample (91) | -1.924 (0.679) | 46,617 | 45,164 | 1,453 | 2.87 | 2.52 | 0.35 (0.12) |
| CK_eq7_structural | GR_2006_2010 | all_metros (348) | -1.199 (0.313) | 45,768 | 39,463 | 6,305 | 2.75 | 2.19 | 0.57 (0.15) |
| CK_eq7_structural | GR_2006_2010 | ck_sample (91) | -1.199 (0.313) | 36,357 | 36,515 | -158 | 2.23 | 2.05 | 0.18 (0.05) |
| CK_T3_structural_women | GR_2006_2010 | all_metros (331) | -0.577 (0.256) | 9,539 | 7,715 | 1,823 | 0.41 | 0.30 | 0.11 (0.05) |
| CK_T3_structural_women | GR_2006_2010 | ck_sample (91) | -0.577 (0.256) | 7,668 | 7,294 | 374 | 0.34 | 0.29 | 0.05 (0.02) |
| own_GR_OLS_natives | GR_2006_2010 | all_metros (355) | -0.471 (0.825) | 14,376 | 11,815 | 2,560 | 0.87 | 0.65 | 0.21 (0.37) |
| own_GR_OLS_natives | GR_2006_2010 | ck_sample (91) | -0.471 (0.825) | 11,414 | 11,058 | 356 | 0.70 | 0.62 | 0.08 (0.15) |
| own_GR_OLS_other_natives | GR_2006_2010 | all_metros (355) | -0.256 (1.025) | 7,819 | 6,427 | 1,393 | 0.47 | 0.35 | 0.12 (0.46) |
| own_GR_OLS_other_natives | GR_2006_2010 | ck_sample (91) | -0.256 (1.025) | 6,208 | 6,015 | 193 | 0.38 | 0.34 | 0.05 (0.18) |
| own_GR_IV_natives | GR_2006_2010 | all_metros (355) | -2.002 (1.708) | 61,089 | 50,208 | 10,880 | 3.68 | 2.77 | 0.91 (0.78) |
| own_GR_IV_natives | GR_2006_2010 | ck_sample (91) | -2.002 (1.708) | 48,501 | 46,990 | 1,512 | 2.98 | 2.62 | 0.36 (0.31) |
| own_GR_OLS_native_women | GR_2006_2010 | all_metros (355) | -0.677 (1.212) | 15,357 | 13,230 | 2,127 | 0.66 | 0.52 | 0.14 (0.25) |
| own_GR_OLS_native_women | GR_2006_2010 | ck_sample (91) | -0.677 (1.212) | 12,433 | 12,395 | 38 | 0.55 | 0.49 | 0.05 (0.10) |
| own_COVID21_OLS_natives | COVID_2019_2021 | all_metros (351) | 0.263 (1.053) | -3,182 | -5,104 | 1,922 | -0.19 | -0.27 | 0.08 (0.33) |
| own_COVID21_OLS_natives | COVID_2019_2021 | ck_sample (92) | 0.263 (1.053) | -3,001 | -4,113 | 1,112 | -0.18 | -0.22 | 0.04 (0.17) |
| own_COVID22_OLS_natives | COVID_2019_2022 | all_metros (351) | 0.571 (1.446) | -5,691 | -14,758 | 9,066 | -0.34 | -0.80 | 0.46 (1.18) |
| own_COVID22_OLS_natives | COVID_2019_2022 | ck_sample (93) | 0.571 (1.446) | -6,263 | -10,844 | 4,580 | -0.38 | -0.59 | 0.22 (0.55) |
| own_COVID23_OLS_natives | COVID_2019_2023 | all_metros (351) | 1.456 (0.879) | -19,398 | -43,155 | 23,757 | -1.14 | -2.33 | 1.18 (0.71) |
| own_COVID23_OLS_natives | COVID_2019_2023 | ck_sample (93) | 1.456 (0.879) | -21,747 | -31,513 | 9,765 | -1.31 | -1.71 | 0.40 (0.24) |
| own_BOOM_OLS_natives | BOOM_2012_2016 | all_metros (359) | 0.222 (1.067) | -1,940 | -7,734 | 5,794 | -0.10 | -0.40 | 0.30 (1.44) |
| own_BOOM_OLS_natives | BOOM_2012_2016 | ck_sample (91) | 0.222 (1.067) | -2,291 | -4,320 | 2,030 | -0.12 | -0.22 | 0.10 (0.48) |
| own_GR_OLS_natives_split | GR_2006_2010 | all_metros (355) | -0.912 (0.932) | 27,825 | 22,869 | 4,956 | 1.68 | 1.26 | 0.41 (0.42) |
| own_GR_OLS_natives_split | GR_2006_2010 | ck_sample (91) | -0.912 (0.932) | 22,091 | 21,403 | 688 | 1.36 | 1.19 | 0.16 (0.17) |

### 4 Mobility

| Rate, % a year (SE) | Group | 2006-2010 | 2019-2024 | 2024 |
|---|---|---:|---:|---:|
| From abroad | mex_fb | 2.11 (0.06) | 1.16 (0.05) | 1.56 (0.11) |
| From abroad | mex_nb | 0.40 (0.03) | 0.35 (0.02) | 0.29 (0.03) |
| From abroad | oth_nb | 0.24 (0.01) | 0.22 (0.01) | 0.24 (0.01) |
| From abroad | oth_fb | 2.38 (0.06) | 3.01 (0.06) | 4.08 (0.14) |
| From abroad | mex_fb_minus_oth_nb | 1.87 (0.06) | 0.94 (0.05) | 1.32 (0.11) |
| From abroad | mex_nb_minus_oth_nb | 0.16 (0.03) | 0.13 (0.02) | 0.05 (0.03) |
| Between states | mex_fb | 1.62 (0.04) | 0.76 (0.03) | 0.93 (0.09) |
| Between states | mex_nb | 1.89 (0.06) | 1.35 (0.04) | 1.18 (0.09) |
| Between states | oth_nb | 2.26 (0.02) | 1.91 (0.02) | 1.77 (0.04) |
| Between states | oth_fb | 1.85 (0.05) | 1.52 (0.04) | 1.63 (0.09) |
| Between states | mex_fb_minus_oth_nb | -0.64 (0.05) | -1.15 (0.04) | -0.84 (0.10) |
| Between states | mex_nb_minus_oth_nb | -0.37 (0.07) | -0.56 (0.05) | -0.58 (0.10) |
| Either | mex_fb | 3.73 (0.07) | 1.92 (0.06) | 2.49 (0.15) |
| Either | mex_nb | 2.29 (0.07) | 1.70 (0.05) | 1.47 (0.10) |
| Either | oth_nb | 2.50 (0.02) | 2.13 (0.02) | 2.01 (0.04) |
| Either | oth_fb | 4.23 (0.07) | 4.52 (0.07) | 5.70 (0.15) |
| Either | mex_fb_minus_oth_nb | 1.23 (0.07) | -0.21 (0.06) | 0.48 (0.16) |
| Either | mex_nb_minus_oth_nb | -0.21 (0.07) | -0.43 (0.05) | -0.54 (0.11) |

### 5 Borjas

| lambda | k | Cost | Printed $bn | Reproduced, 0.1 grid | 0.01 grid |
|---:|---:|---|---:|---:|---:|
| 0.45 | 1.0 | low | 2.7 | 2.67 | 2.65 |
| 0.45 | 1.0 | medium | 3.5 | 3.51 | 3.50 |
| 0.45 | 1.0 | high | 4.6 | 4.60 | 4.54 |
| 0.45 | 1.0 | prohibitive | 10.3 | 10.30 | 10.30 |
| 0.4 | 0.5 | low | 4.7 | 4.70 | 4.64 |
| 0.4 | 0.5 | medium | 6.1 | 6.05 | 6.03 |
| 0.4 | 0.5 | high | 7.9 | 7.92 | 7.65 |
| 0.4 | 0.5 | prohibitive | 13.2 | 13.18 | 13.18 |
| 0.3 | 0.25 | low | 6.9 | 6.91 | 6.99 |
| 0.3 | 0.25 | medium | 9.0 | 9.03 | 9.06 |
| 0.3 | 0.25 | high | 12.4 | 13.45 | 11.42 |
| 0.3 | 0.25 | prohibitive | 22.0 | 22.00 | 22.00 |

| Scenario | Sorting | lambda | theta | Low | Medium | High | Prohibitive |
|---|---|---:|---:|---:|---:|---:|---:|
| mexico_born_all | full_sorting_theta_1 | 0.45 | 1.000 | 3.41 | 4.34 | 5.34 | 7.54 |
| mexico_born_all | observed_sorting_2024 | 0.45 | 0.612 | 0.30 | 0.38 | 0.46 | 0.74 |
| mexico_born_all | full_sorting_theta_1 | 0.4 | 1.000 | 4.45 | 5.58 | 6.79 | 9.72 |
| mexico_born_all | observed_sorting_2024 | 0.4 | 0.602 | 0.41 | 0.52 | 0.71 | 1.32 |
| mexico_born_all | full_sorting_theta_1 | 0.3 | 1.000 | 6.50 | 8.18 | 10.03 | 16.61 |
| mexico_born_all | observed_sorting_2024 | 0.3 | 0.470 | 0.18 | 0.30 | 0.44 | 1.43 |
| mexico_born_arrived_2019_2024 | full_sorting_theta_1 | 0.45 | 1.000 | 0.05 | 0.06 | 0.07 | 0.09 |
| mexico_born_arrived_2019_2024 | observed_sorting_2024 | 0.45 | 0.523 | 0.00 | 0.00 | 0.00 | 0.00 |
| mexico_born_arrived_2019_2024 | full_sorting_theta_1 | 0.4 | 1.000 | 0.06 | 0.07 | 0.05 | 0.11 |
| mexico_born_arrived_2019_2024 | observed_sorting_2024 | 0.4 | 0.513 | -0.00 | 0.00 | 0.00 | 0.01 |
| mexico_born_arrived_2019_2024 | full_sorting_theta_1 | 0.3 | 1.000 | 0.12 | 0.12 | 0.19 | 0.20 |
| mexico_born_arrived_2019_2024 | observed_sorting_2024 | 0.3 | 0.392 | 0.01 | 0.01 | 0.02 | 0.01 |
| mexican_origin_union_upper | full_sorting_theta_1 | 0.45 | 1.000 | 27.22 | 30.02 | 33.37 | 48.38 |
| mexican_origin_union_upper | observed_sorting_2024 | 0.45 | 0.612 | 1.81 | 2.33 | 2.92 | 4.81 |
| mexican_origin_union_upper | full_sorting_theta_1 | 0.4 | 1.000 | 23.36 | 30.28 | 38.18 | 61.68 |
| mexican_origin_union_upper | observed_sorting_2024 | 0.4 | 0.602 | 2.48 | 3.30 | 4.33 | 8.59 |
| mexican_origin_union_upper | full_sorting_theta_1 | 0.3 | 1.000 | 36.60 | 47.04 | 58.80 | 101.84 |
| mexican_origin_union_upper | observed_sorting_2024 | 0.3 | 0.470 | 0.56 | 1.20 | 2.20 | 9.47 |

## 10. Limits

- The insurance channel rests on one episode, the Great Recession. The smoothing gradient's pre-trend
  critique (Monras; Amior's dynamics control) is not resolved. Our replication gives a quarter of
  the paper's gradient with a standard error larger than the estimate.
- The paper does not print its halves' mean Mexican shares. Converting its slope gap into a
  gradient uses our 2006 sample's gap (0.224). The structural check (−0.294 against the paper's
  −0.29) suggests the samples align.
- D, L and ρ are assumptions, bounded by Yagan (persistence, linearity) and Davis–von Wachter
  (national convexity). No study measures how displacement losses vary across metros within one
  recession.
- Wages are 2006 wage and salary income per employed man, which includes the non-employed who
  earned wages earlier in the year. The marginal worker probably earns less than the average, so
  the dollar values lean high.
- The present-day factor assumes smoothing scales with excess mobility. Return migration comes from
  ENADID over ACS denominators, with a three-year age mismatch.
- Rural areas are outside the metro sets. Their Mexican-born shares are lower, so the national total
  would change little.
- Connecticut: 2020 PUMAs (ACS 2022–2024) join through the 2022 planning regions (09110–09190).
  The shared county→CBSA file (`hedonic_composition_2026_09_19/derived/geo_county_cbsa_2013.csv`)
  lacks those regions, so `metro_panel.county_cbsa()` maps them with the lane's `CT_REGIONS` and
  prints `[DEGRADED]`. `CT_REGIONS` assigns each region to the 2013 metro holding most of its
  people. Once the file carries the regions, its rows win and no county can appear twice. QCEW
  2006–2023 uses the old counties (09001–09015) and is unaffected.
  - Only the 2022 and 2023 metro cells depend on this, so only the COVID 2019–22 and 2019–23 rows
    of §9 can move.
  - The headline uses the 2006–10 episode, national mobility and the 2019–21 elasticity gap, so it
    cannot move.
  - Status and rerun result after the shared fix: pending, see the note appended below.
- Borjas's model uses nominal state wages and his calibrated moving costs (0.5×, 1× and 2× annual
  income per worker at one million movers).
- The research was done through an LLM (`notes/llm-bias-caveat.md`). Every number above comes from a
  cached primary text or a script in this lane.

## 11. Reproduce

From the repository root, in order (raw pulls land in the ignored `_cache/`; the 2023 ACS zip was
fetched into `_cache/acs_raw/`, SHA-256 98b6ecb1…):

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/labor_mobility_insurance_2026_09_23/acs_extract.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/labor_mobility_insurance_2026_09_23/metro_panel.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/labor_mobility_insurance_2026_09_23/fetch_qcew.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/labor_mobility_insurance_2026_09_23/ck_tests.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/labor_mobility_insurance_2026_09_23/borjas_inputs.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/labor_mobility_insurance_2026_09_23/borjas_model.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/labor_mobility_insurance_2026_09_23/mobility_summary.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/labor_mobility_insurance_2026_09_23/price_insurance.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/labor_mobility_insurance_2026_09_23/result_tables.py
```

The following steps stop on failure, not silently:

- `borjas_model.py` exits before writing 2024 rows if Table 8 is not reproduced.
- `price_insurance.py` checks its CPI-U values against the BLS pull cached by the NCVS lane.
- `fetch_qcew.py` checks county counts and national totals.

## Sources

All texts were read in `_cache/papers/` or `_cache/lit/` (ignored); page, table or quoted phrase is
given in §2–§3.

- Cadena, B. C. & Kovak, B. K. (2016). AEJ: Applied 8(1):257–290. PMC4991313.
- Borjas, G. J. (2001). BPEA 2001(1):69–133, with comments by R. Topel and R. Shimer.
- Cadena, B. C. (2013). JHR 48(4):910–944. PMC4190078.
- Cadena, B. C. (2014). JUE 80:1–12. PMC4079004.
- Basso, G. & Peri, G. (2020). JEP 34(3):77–98. doi:10.1257/jep.34.3.77.
- Basso, G., D'Amuri, F. & Peri, G. (2019). IMF Economic Review; NBER w25091.
- Amior, M. (2024). JOLE, doi:10.1086/730163; CEP DP 1678 (rev. Sept 2021).
- Monras, J. (2015). IZA DP 8840.
- Autor, D., Dorn, D. & Hanson, G. (2024). ILR Review, doi:10.1177/00197939241293404; IZA DP 17213.
- Jauer, J., Liebig, T., Martin, J. P. & Puhani, P. (2014). IZA DP 7921 (J Pop Econ 2019).
- Şahin, A., Song, J., Topa, G. & Violante, G. (2014). AER; NBER w18265.
- Peri, G. & Zaiour, R. (2023). J Pop Econ, doi:10.1007/s00148-023-00972-y.
- Faber, M., Sarto, A. & Tabellini, M. (2022). NBER w30048; IZA DP 14623.
- Davis, S. J. & von Wachter, T. (2011). BPEA; NBER w17638.
- Schmieder, J. F., von Wachter, T. & Heining, J. (2023). AER; NBER w30162.
- Yagan, D. (2019). JPE; NBER w23844.
- Ganong, P. & Noel, P. (2019). AER; NBER w25417.
- Data:
  - ACS 1-year PUMS 2005–2024 (Census);
  - BLS QCEW annual single files 2006–2023 (`derived/qcew_manifest.json` has URLs and SHA-256);
  - BLS CPI-U CUUR0000SA0;
  - BEA NIPA T1.1.5;
  - ENADID 2018 and 2023, via `enadid_return_selectivity_2026_09_22`;
  - Geocorr PUMA–county crosswalks (`derived/xwalk_manifest.json`).
