**Verdict:** Bigger cities raise other residents' earnings, and the group's low schooling lowers
them. In the one design that measures both on the same data, the two nearly cancel: together they
are worth **+$13.9bn a year** to other US residents (95% interval −$56.6bn to +$84.4bn), which is
**$341 per member** of the 40.9m Mexican-origin union and **$47 per other resident**. Of that,
$6.0bn is induced tax receipts and $8.0bn private income. The sign depends on how large
human-capital spillovers are. The college-share estimates from 1970–2000 data would turn it into a
net cost of $109–677bn.
[CALCULATION: `arms.py` → `derived/summary.csv`, `derived/joint_grid.csv`]

- **Scale (agglomeration): +$38.6bn** (95% interval $32.3–45.0bn; $945 per member, $129 per
  other resident). Card, Rothstein & Yi (2023) measure commuting-zone wage premia with worker
  sorting removed. The premia rise 0.020 (high school or less) and 0.043 (some college or more) per log
  point of CZ employment. Holding the college share fixed, as the composition channel requires,
  they are 0.747 times as large. Applied CZ by CZ to others' earnings, with the group's share of
  workers as the size change, they give $38.6bn. Other sorting-adjusted estimates run $11.5–65.3bn. Estimates
  that keep sorting, or come from 1970–90 instrumented city regressions, run to $98–205bn. The
  gain is twice the congestion lane's $19.2bn cost, its counterpart.
- **Human-capital composition: −$24.9bn** (95% interval −$93.0bn to +$43.1bn; −$610 per member).
  Without the group, the share of workers with some college would be 3.0 points higher. In the
  same regression, premia rise 0.326 per unit of that share. The account's own CES (σ = 2)
  produces 0.253 of that through substitution alone. The remaining externality is 0.073.
  The estimate rests on that netting. With no CES term the cost is −$112.1bn; at σ 1.5–2.5 it is
  +$3.8bn to −$42.2bn. The weight of college workers in CRY's pooled premia (0.609) comes from
  CRY's own tables. Counting its sampling error, as if those tables were independent, widens the
  interval to −$252bn to +$202bn.
- **The literature on composition disagrees.** Average-schooling estimates are near zero: −$47bn
  to +$28bn, with intervals of ±$90–240bn (Ciccone–Peri 2006; Acemoglu–Angrist 2000). The
  instrumented college-share estimates for 1970–2000 are far larger: Moretti (2004) −$148bn to
  −$541bn, and Iranzo–Peri (2009) −$392bn to −$716bn on their own variable definitions.
- **Net across designs.** Other designs that estimate scale and composition in one regression
  give +$11.8bn (Glaeser–Resseger 2010, net of CES), −$21.0bn (Rosenthal–Strange 2008 distance
  rings) and +$116bn to +$169bn (Ciccone–Peri 2006). Within the CRY design the net runs from
  −$72.5bn (no CES term) to +$51.6bn (unconditional size effect, no composition externality).
  Pairing the central scale gain with the college-share instrumented estimates gives −$109bn to
  −$677bn.
- **Innovation is not measurable and is not added.** Burchardi et al. (w27075) find no patent
  response to migrants at the Mexico-born's 9.7 years of schooling: −0.07 of the average migrant's,
  95% −1.42 to +1.29. Scaled through their structural aggregate, that is −$24bn (−$518bn to +$470bn). Their wage
  gradient gives +$50bn (−$139bn to +$240bn), but it is a total local wage effect that overlaps
  scale and P.

**Overlap ruling.** The account's production term P is a one-good CES with constant returns, so
neither the scale gain nor the composition externality is inside P. The substitution part of
composition is inside P and in the wage-split lane's transfers, and every composition estimate
used here removes it. If adopted, the net enters the account the way P and F do. Private income,
+$8.0bn, goes to P and receipts, +$6.0bn, go to F. The main case would fall from $203.2–249.6bn to
$189.3–235.7bn. Innovation is outside P but is not added, as stated above. The overlaps with the
other lanes are set out in section 5.

Date: 2026-09-23. Brief: [`BRIEF.md`](BRIEF.md). 2024 dollars; stationary comparison with and
without the 40,896,574 CPS Mexican-origin residents; effects on the 299.2m other residents.

## 1. Method

**Formula.** For each channel the change in other residents' log earnings, without minus with the
group, is Δψ = Σ elasticity × (change in the regressor). The gain from the group's presence in an
area is E × (1 − exp(Δψ)), with E other residents' 2024 earnings there. E is split by education
wherever the elasticity is. The brief's first-order form, E × elasticity × ln(1/(1 − s)), gives
$38.84bn for the central scale estimate against $38.65bn from the exponential form, a 0.5% gap. A
gate stops the run if the gap exceeds 1%. [CALCULATION: `derived/checks.json`]

**Units matched to each elasticity.**

| Source | Size or schooling regressor | Change applied here |
|---|---|---|
| Card–Rothstein–Yi, Ciccone–Peri scale | log CZ or city employment | ln(1 − group share of workers) |
| Ahlfeldt–Pietrostefani, De la Roca–Puga | log density | ln(1 − group share of persons) at fixed area; ×0.43 if area shrinks with population |
| Glaeser–Resseger | log MSA population; adults' BA share | persons; adults 25+ |
| CRY composition | share of workers with some college or more | 3.0-point rise nationally |
| Moretti | share of workers with a BA or more | 2.8-point rise |
| Ciccone–Peri, Acemoglu–Angrist | workers' mean years of schooling | +0.255 years |
| Iranzo–Peri | years of schooling of workers with (without) any college, per worker | +0.505 (−0.250) |
| Rosenthal–Strange | full-time workers 30–65 within 0–5 and 5–25 miles, by BA | group counts spread evenly over each CBSA's land area |
| Burchardi et al. | adult migrants per county; migrants' years of schooling | ratio to the average migrant, times their structural aggregate |

[DATA: `derived/checks.json` `national`]

**Data.** ACS 2024 one-year PUMS (`tabulate.py`). Group: Hispanic origin Mexican or born in
Mexico. Earnings are PERNP × ADJINC. Five published national totals are reproduced within 0.21%
(`derived/pums_gate.csv`). Group counts are scaled to the CPS union (× 1.0372), and the difference
comes out of other residents. A gate checks that the population is conserved.

**Geography.** The central geography is 1990 commuting zones, CRY's units: 727 areas, with Alaska
pooled and Connecticut's planning regions set to its single CZ. The alternatives are 2023 CBSAs
with state remainders (969 areas) and one national area. Across the three, each result moves by at
most 8%: $2.3bn for the central scale gain and $0.6bn for the central composition cost. The
exception is Glaeser–Resseger's composition term, which varies with local population. The group's metro shares agree with
the congestion lane's urban areas: Los Angeles 0.349 (CBSA) vs 0.365 (UA), Houston 0.270 vs
0.279, Chicago 0.194 vs 0.199. [DATA: `derived/area_measures_*.csv`; congestion
`derived/ua_exposure.csv`]

**The CRY regression.** The public file (`L3_czeffects.dta`, 691 CZs) reproduces CRY Table 3 to
four decimals: 0.0340 on log size and 0.6640 on the college share. That check runs as a positive
control inside the script. With both regressors in one weighted regression, the coefficients are
0.0254 (SE 0.0022) and 0.326 (SE 0.087), with correlation −0.43. The public premia are CRY's best linear predictions from ACS data.
Regression SEs on them are therefore too small, and the college-share SE is inflated by 1.17, the
ratio of the paper's SE to the SE on the public file. The size SE needs no inflation.
[CALCULATION: `derived/cry_gradient.csv`]

**The CES term.** A pooled college-share gradient contains substitution even with no
externality: (θ − m)/(σ s (1 − s)). Here s is the share of workers with some college in CRY's
sample (0.591), θ their earnings share (0.731, from the 2024 earnings-per-worker ratio 1.885) and
m the weight of the more-educated in the pooled premium. m = 0.609 is the value implied by CRY's own
pooled and by-education size estimates, (0.034 − 0.020)/(0.043 − 0.020); its SE is 0.156 if the
three are independent. At σ = 2 the term is 0.253. The Moretti NLSY and Glaeser–Resseger pooled
estimates get the same treatment with bachelor's-degree shares from the 1980, 1990 and 2000
censuses (`sample_weights.py`). [CALCULATION: `derived/checks.json` `ces_shares`]

**Uncertainty.** Delta method, central differences at one SE per parameter, with the regression's
covariance where one regression gives both parameters. Otherwise parameters are treated as
independent. Estimates published without an SE have no interval.

## 2. Results: scale

CZ central; CBSA and national alternatives. Receipts are the account's marginal rates (0.384 on
high-school-or-less earnings, 0.426 above). $bn a year, per member and per other resident in $.

| Specification | Parameter (SE) | CZ $bn | 95% interval | CBSA | National | Receipts | Per member | Per other resident |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **CRY by education, conditional on college share (central)** | 0.0254 (0.0022) × 0.020/0.034, 0.043/0.034 | +38.6 | +32.3 to +45.0 | +38.1 | +40.4 | +16.3 | +945 | +129 |
| CRY pooled, conditional on college share | 0.0254 (0.0022) | +33.3 | +27.8 to +38.8 | +32.9 | +35.3 | +14.0 | +815 | +111 |
| CRY by education, unconditional | 0.020 (0.002); 0.043 (0.003) | +51.6 | +45.1 to +58.1 | +50.9 | +54.0 | +21.8 | +1,262 | +173 |
| CRY pooled, unconditional | 0.034 (0.003) | +44.5 | +36.9 to +52.2 | +44.0 | +47.2 | +18.7 | +1,089 | +149 |
| CRY raw earnings gradient (sorting kept) | 0.075 (0.008) | +97.6 | +77.4 to +117.7 | +96.3 | +104.0 | +40.9 | +2,386 | +326 |
| A&P recommended density elasticity (interval = ±1.96 SD of 47 estimates) | 0.04 (SD 0.04) | +53.4 | −50.6 to +157.3 | +52.6 | +57.2 | +22.4 | +1,305 | +178 |
| A&P net of sorting, fixed area | 0.02 | +26.8 | | +26.4 | +28.6 | +11.2 | +655 | +89 |
| A&P, area shrinking with population | 0.04 × 0.43 | +23.0 | | +22.7 | +24.6 | +9.7 | +563 | +77 |
| A&P net of sorting, area shrinking | 0.02 × 0.43 | +11.5 | | +11.4 | +12.3 | +4.8 | +282 | +39 |
| De la Roca–Puga, static plus seven years' learning | 0.049 | +65.3 | | +64.3 | +70.0 | +27.4 | +1,597 | +218 |
| Ciccone–Peri scale term, Table 4 col 2 | 0.081 (0.027) | +105.3 | +37.4 to +173.2 | +104.0 | +112.2 | +44.2 | +2,574 | +352 |
| Ciccone–Peri scale term, Table 4 col 1 | 0.16 (0.06) | +205.4 | +58.2 to +352.6 | +202.8 | +220.6 | +86.2 | +5,022 | +686 |
| Glaeser–Resseger, size effect rising with BA share | 0.022 (0.012) + 0.196 (0.113) × (BA share − mean) | +32.6 | +1.0 to +64.1 | +29.8 | +31.5 | +13.7 | +796 | +109 |
| CRY pooled, group's share of BA workers only | 0.034 (0.003) | +19.5 | +16.2 to +22.9 | +19.5 | +21.1 | +8.2 | +477 | +65 |

[CALCULATION: `derived/scale_grid.csv`]

The gain is concentrated where the group lives. Ten CBSAs account for half of it, led by Los
Angeles ($5.0bn), Dallas, Chicago, Houston and Riverside. [DATA: `derived/metro_distribution.csv`]

## 3. Results: composition

A negative number is a cost of the group's presence.

| Specification | Parameter (SE) | CZ $bn | 95% interval | CBSA | National | Receipts | Per member | Per other resident |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **CRY college gradient net of CES, σ 2, CRY weights (central)** | 0.326 − 0.253 = 0.073 (0.102) | −24.9 | −93.0 to +43.1 | −24.3 | −24.4 | −10.5 | −610 | −83 |
| same, with the weight m's SE (0.156) | | −24.9 | −251.8 to +201.9 | −24.3 | −24.4 | −10.5 | −610 | −83 |
| CRY net of CES, σ 1.5, CRY weights | −0.011 (0.102) | +3.8 | −63.9 to +71.4 | +3.7 | +3.7 | +1.6 | +92 | +13 |
| CRY net of CES, σ 2.5, CRY weights | 0.124 (0.102) | −42.2 | −110.5 to +26.1 | −41.2 | −41.2 | −17.7 | −1,033 | −141 |
| CRY net of CES, σ 2, employment weights | 0.036 (0.102) | −12.2 | −80.0 to +55.7 | −11.9 | −11.9 | −5.1 | −297 | −41 |
| CRY net of CES, σ 1.5, employment weights | −0.061 (0.102) | +20.7 | −46.7 to +88.1 | +20.2 | +20.3 | +8.7 | +506 | +69 |
| CRY net of CES, σ 2.5, employment weights | 0.094 (0.102) | −32.0 | −100.1 to +36.2 | −31.2 | −31.2 | −13.4 | −782 | −107 |
| CRY gradient with no CES term (includes substitution; bound) | 0.326 (0.102) | −112.1 | −181.4 to −42.8 | −109.5 | −109.0 | −47.1 | −2,741 | −375 |
| Ciccone–Peri average schooling, Table 4 col 2 | −0.004 (0.017) | +11.1 | −81.0 to +103.2 | +10.8 | +11.4 | +4.6 | +271 | +37 |
| Ciccone–Peri, Table 4 col 1 | 0.014 (0.03) | −39.0 | −203.2 to +125.3 | −38.0 | −40.0 | −16.4 | −952 | −130 |
| Ciccone–Peri, Table 4 col 4 (experience control) | −0.01 (0.018) | +27.6 | −69.6 to +124.8 | +27.0 | +28.5 | +11.6 | +676 | +92 |
| Ciccone–Peri, white males, Table 5 col 2 | −0.001 (0.021) | +2.8 | −111.2 to +116.7 | +2.7 | +2.9 | +1.2 | +68 | +9 |
| Acemoglu–Angrist, Table 6 col 3 | 0.004 (0.035) | −11.1 | −201.6 to +179.4 | −10.8 | −11.4 | −4.7 | −271 | −37 |
| Acemoglu–Angrist, Table 6 col 2 | 0.017 (0.043) | −47.3 | −283.2 to +188.6 | −46.2 | −48.6 | −19.9 | −1,158 | −158 |
| Glaeser–Resseger BA share, net of CES σ 2 | 0.411 (0.122) + 0.196 (0.113) × (log pop − mean) | −37.6 | −121.3 to +46.0 | −32.3 | +11.5 | −15.9 | −920 | −126 |
| Glaeser–Resseger BA share, no CES term (bound) | same | −158.1 | −244.6 to −71.7 | −148.9 | −102.6 | −66.5 | −3,866 | −528 |
| Iranzo–Peri, Table 8 col 1 | college 0.06 (0.025); high school −0.01 (0.01) | −392.0 | −705.6 to −78.4 | −382.0 | −373.0 | −164.6 | −9,586 | −1,310 |
| Iranzo–Peri 1980–2000, Table 8 col 5 | 0.12 (0.04); 0.01 (0.03) | −712.8 | −1,275.0 to −150.5 | −694.2 | −669.2 | −299.3 | −17,429 | −2,382 |
| Iranzo–Peri sector-demand control, Table 9 col 4 | 0.11 (0.04); −0.01 (0.02) | −715.5 | −1,257.1 to −174.0 | −696.8 | −668.6 | −300.5 | −17,496 | −2,391 |
| Iranzo–Peri col 1, read as years beyond 12 (not their variable) | 0.06 (0.025); −0.01 (0.01) | −92.1 | −179.6 to −4.5 | −89.4 | −88.2 | −38.7 | −2,251 | −308 |
| Moretti own college coefficient, col 4 (lower bound on spillover) | 0.47 (0.37) | −154.7 | −397.7 to +88.4 | −150.1 | −148.3 | −65.0 | −3,782 | −517 |
| Moretti own, col 3 | 0.86 (0.35) | −287.4 | −524.4 to −50.3 | −278.7 | −272.9 | −120.8 | −7,027 | −960 |
| Moretti own, col 6 (land grant 1990) | 0.55 (0.19) | −181.6 | −307.2 to −56.0 | −176.2 | −173.8 | −76.3 | −4,440 | −607 |
| Moretti own, col 8 (land grant 1980) | 0.45 (0.17) | −148.0 | −259.5 to −36.5 | −143.6 | −142.0 | −62.2 | −3,618 | −495 |
| Moretti earnings-weighted, col 4, 1980–90 weights | 1.181 (0.424) | −399.6 | −694.3 to −104.9 | −387.3 | −376.4 | −167.9 | −9,770 | −1,335 |
| Moretti earnings-weighted, col 4, 2024 weights | 0.862 (0.398) | −287.9 | −557.2 to −18.6 | −279.2 | −273.4 | −121.0 | −7,040 | −962 |
| Moretti earnings-weighted, col 3, 1980–90 weights | 1.573 (0.416) | −540.7 | −838.7 to −242.6 | −523.8 | −504.1 | −227.2 | −13,220 | −1,807 |
| Moretti earnings-weighted, col 3, 2024 weights | 1.258 (0.385) | −427.2 | −696.4 to −158.0 | −414.1 | −401.6 | −179.5 | −10,446 | −1,428 |
| Moretti earnings-weighted, col 6, 1990 weights | 0.747 (0.186) | −248.4 | −373.1 to −123.7 | −241.0 | −236.6 | −104.4 | −6,074 | −830 |
| Moretti earnings-weighted, col 6, 2024 weights | 0.685 (0.187) | −227.3 | −352.0 to −102.6 | −220.5 | −216.8 | −95.5 | −5,557 | −760 |
| Moretti earnings-weighted, col 8, 1980 weights | 0.603 (0.154) | −199.4 | −301.9 to −97.0 | −193.5 | −190.6 | −83.8 | −4,876 | −666 |
| Moretti earnings-weighted, col 8, 2024 weights | 0.536 (0.159) | −176.9 | −281.9 to −71.9 | −171.7 | −169.4 | −74.3 | −4,327 | −591 |
| Moretti NLSY base case, net of CES σ 2 (σ 1.5 / 2.5) | 1.27 − 0.297 = 0.974 (0.33) | −327.1 (−292.8 / −347.7) | −552.6 to −101.6 | −317.1 | −309.7 | −137.4 | −7,997 | −1,093 |
| Moretti NLSY individual × city effects, net of CES σ 2 (σ 1.5 / 2.5) | 1.08 − 0.297 = 0.784 (0.32) | −261.3 (−227.6 / −281.7) | −476.7 to −45.9 | −253.5 | −248.6 | −109.8 | −6,390 | −873 |
| Moretti plant productivity 0.5 / 0.7, as wages at labour share 0.7 | 0.714 / 1.0 | −237.3 / −336.0 | | | | −99.7 / −141.2 | | |

[CALCULATION: `derived/composition_grid.csv`; the σ 1.5 and 2.5 rows and the CBSA and national
columns for the plant rows are there]

Three points about how these estimates were read:

- **Moretti's "own" coefficient** is the effect of the college share on college graduates' wages.
  Moretti presents it as a lower bound on the spillover, because substitution pulls it down. The
  earnings-weighted average of his four group coefficients is Ciccone and Peri's constant-composition
  externality, and his own sample's weights are the right ones for it (1980–90 income shares
  0.133 / 0.283 / 0.233 / 0.351 from the censuses; `derived/sample_weights.csv`). The SE assumes
  the four group estimates are perfectly correlated, which gives the widest interval.
- **Iranzo–Peri's variables** are the total years of schooling of workers with any college, and of
  workers with at most a high-school diploma, each divided by all workers
  ("we compute the years of schooling of workers with at most a high school diploma and divide
  them by the total number of workers"). Their first stage agrees: the instrument moves "years of
  college per worker" 9.23 against 0.55 for the college share (Table 6), about 17 years per
  college worker. On that definition the group's absence raises the college variable by 0.505 and
  the estimate is −$392bn. Their text converts Moretti as if the variable counted only years
  beyond 12. On that reading the estimate is −$92bn; it is reported, but it is not their variable.
- **Constant-composition and CES-netted estimates** exclude the substitution effect that P already
  contains. The two "no CES term" rows keep it and are upper bounds on the cost. Adding them to
  the account would double count P and the wage-split lane.

## 4. Results: scale and composition from one regression, and innovation

| Specification | CZ $bn | 95% interval | CBSA | National | Receipts (CZ) | Per member | Per other resident |
|---|---:|---:|---:|---:|---:|---:|---:|
| **CRY joint, σ 2, CRY weights (central)** | **+13.9** | −56.6 to +84.4 | +14.0 | +16.1 | +6.0 | +341 | +47 |
| same, with the weight m's SE | +13.9 | −211.9 to +239.8 | +14.0 | +16.1 | +6.0 | +341 | +47 |
| CRY joint, σ 1.5 | +42.4 | −27.7 to +112.5 | +41.8 | +44.0 | +17.9 | +1,037 | +142 |
| CRY joint, σ 2.5 | −3.2 | −74.0 to +67.5 | −2.8 | −0.7 | −1.2 | −79 | −11 |
| CRY joint, no CES term | −72.5 | −144.3 to −0.7 | −70.4 | −68.2 | −30.3 | −1,773 | −242 |
| Glaeser–Resseger joint, Table 1 col 3, BA term net of CES σ 2 | +11.8 | −65.1 to +88.7 | +13.5 | +49.2 | +4.9 | +289 | +40 |
| Ciccone–Peri joint, Table 4 col 2 | +116.1 | +3.4 to +228.8 | +114.5 | +123.5 | +48.7 | +2,839 | +388 |
| Ciccone–Peri joint, Table 4 col 1 | +168.2 | −47.9 to +384.2 | +166.4 | +181.4 | +70.5 | +4,112 | +562 |
| Ciccone–Peri joint, Table 4 col 4 | +169.1 | +32.4 to +305.9 | +166.7 | +180.3 | +71.0 | +4,135 | +565 |
| Rosenthal–Strange rings, OLS, by own education (CBSA only) | | | −21.0 (−79.3 to +37.3) | | −8.8 | −513 | −70 |
| Rosenthal–Strange rings, OLS, full sample (CBSA only) | | | −22.8 (−86.9 to +41.2) | | −9.6 | −559 | −76 |

[CALCULATION: `derived/joint_grid.csv`. Every scale × composition pairing on CZs, 560 rows, is in
`derived/net_grid.csv`]

**Rosenthal–Strange.** In their OLS, full-time college-educated workers within five miles raise a
worker's wage by 7.8e−07 log points each (t 2.73). Less-than-college workers lower it by
3.97e−07 each (t −1.12); within 5–25 miles the effects are 2.2e−07 (t 2.52) and −1.04e−07
(t −1.54). Applied to the group's 9.0m less-than-college and 2.3m college-educated full-time workers
aged 30–65, spread evenly over each CBSA's land area, they give −$21bn. The spread is capped at the
ring areas, so Riverside's 27,277 square miles dilute the exposure. The GMM estimates are larger,
but the instruments are weak (Kleibergen–Paap F 0.3–1.1), so they are not used. Areas outside
CBSAs, 3.8% of others' earnings, are left out.

**Innovation (Burchardi, Chaney, Hassan, Tarquinio & Terry, w27075, Table 9 and §6.3).**

| Gradient | Specification | Effect per 1,000 adult migrants (SE) | Ratio to average migrant (95%) | $bn | 95% interval |
|---|---|---:|---:|---:|---:|
| patents | linear in migrants' schooling, at 9.71 years | −0.017 (0.177) | −0.07 (−1.42 to 1.29) | −24.1 | −518.1 to +469.9 |
| patents | bottom tercile of schooling | 2.023 (3.628) | 8.46 (−21.3 to 38.2) | uninformative | |
| wages | linear in migrants' schooling, at 9.71 years | 0.037 (0.071) | 0.14 (−0.38 to 0.66) | +50.3 | −139.0 to +239.5 |
| wages | bottom tercile of schooling | −0.184 (0.242) | −0.77 (−2.74 to 1.21) | −280.0 | −1,001.9 to +441.8 |

Their structural counterfactual removes post-1965 immigration equal to 16% of population growth,
18.4m people by 2010, and wages fall 5%. Scaled linearly to the 12.0m Mexico-born, that is 3.27% of
others' earnings for average migrants. The table multiplies it by the ratio at the Mexico-born's
mean schooling, 9.71 years at age 25 and over against their 10.88. Only the Mexico-born enter:
BCHTT estimate the effects of migrants, and US-born members are covered by the scale and
composition channels. The authors' own reading is that "low education migrants ... have no
detectable impact on local innovation." [SOURCE: w27075 p. 2, Table 9; CALCULATION:
`derived/innovation_bchtt.csv`]

## 5. Overlap ruling, channel by channel

| Channel | Inside P? | Where it goes | Overlaps and how they are handled |
|---|---|---|---|
| Scale | No. P has constant returns | Adds to the account: private (1 − τ) to P, receipts τ to F | Congestion ($19.2bn) is its cost counterpart and sits beside the account; scale net of congestion is +$19.4bn. Agglomeration raises land rents too, but that is a transfer among other residents, and the housing lanes estimate rents from population shocks that include it, so it is not priced here |
| Composition externality | No. P has no productivity externality | Adds like scale, with a negative sign | Its substitution part is inside P and in the wage-split lane's $66–166bn transfers. It is removed by the CES netting (CRY, Moretti NLSY, Glaeser–Resseger) or by construction (Ciccone–Peri, Iranzo–Peri, Moretti earnings-weighted). The "no CES term" rows double count it |
| Net of the two (central) | No | +$13.9bn to the account ($8.0bn P, $6.0bn F) | The joint rows are alternatives to one another; add at most one |
| Innovation | No. P has no endogenous technology | Not added | The wage transport is a total local wage effect, which contains substitution (P) and scale. The patent transport is zero with a ±$500bn interval |

**Other lanes.** The ancestry-IV lane (`ancestry_iv_congestion_wages_2026_09_23`) estimates total
native wage effects, which net substitution, scale, composition and innovation together, so it is
not added to this lane. Its instrument turned out weak (first-stage F 1.4–1.9). Its interval for
less-educated natives, −10.1% to +5.5%, contains both this lane's central net (+0.12% of others'
earnings) and the college-share scenario (about −3.5%), so it bounds neither. The care and
household-services lane prices induced native hours and their taxes, a labour-supply response that
shares no term with this lane. The construction lane prices cheaper building (a supply response)
and the mobility lane insurance across local shocks; neither contains an agglomeration or
human-capital term. On the cost side, justice, victims, uncompensated care, housing and congestion
price other items. Crime-induced loss of density (`agglom_crime_2026_09_17`) stays unestimated and
out of the sum, as the 2026-09-17 audit §5 set it.

## 6. How the studies were graded (evidence-symmetry rules 1–5)

- **Same design on both sides for the central.** The scale and composition centrals come from one
  regression on one file: sorting-adjusted CZ premia, US, 2010–2018. Both inherit the same flaw.
  Places with natural advantages or amenities could be both bigger and more educated, and both
  gradients are cross-sectional. Neither is discounted for it, so the flaw is treated alike.
- **The instrumented 1970–2000 literature on both sides.** Ciccone–Peri's instrumented scale
  term, 0.081–0.16 or $105–205bn, is reported beside Moretti's and Iranzo–Peri's instrumented
  college-share terms. Adopting the large composition estimates while keeping the smaller modern
  scale estimate would grade the two sides differently. The pairing that keeps one family together
  is Ciccone–Peri's joint estimate, at +$116–169bn.
- **Nothing is dismissed.** Moretti's NLSY estimates with individual × city effects (1.08–1.27)
  are a sorting-adjusted counterweight to CRY. CRY find that 58% of the raw college-share gradient
  is sorting (0.982 of 1.683), so the two sorting-adjusted sources disagree, and both are in the
  table. Rosenthal–Strange's OLS, which finds low-skill neighbours lower wages, is priced even
  though its low-skill coefficients are not significant. The same would apply to an insignificant
  positive.
- **Affiliation:** none weighed.

## 7. Sources, with intervals and populations

| Source | Estimates used | Population |
|---|---|---|
| Card, Rothstein & Yi 2023, NBER w31587, and public file `L3_czeffects.dta` | log size 0.034 (0.003); by education 0.020 (0.002) / 0.043 (0.003); college share 0.664 (0.099); raw 0.075 (0.008); joint (this lane) 0.0254 (0.0022), 0.326 (0.102) | 691 US CZs, LEHD 2010Q1–2018Q2, workers 22–62 |
| Ahlfeldt & Pietrostefani 2019, JUE 111 (LSE eprint 100482) | density elasticity of wages 0.04, SD 0.04 across 47; "net of selection effects ... about halve"; density-to-size 0.43 | 347 estimates, mostly high-income countries |
| Combes & Gobillon 2015, Handbook ch. 5 (IZA DP 8508) | 0.04–0.07 without controls; worker fixed effects "typically around 0.02"; De la Roca–Puga 0.025 static, 0.049 with learning | France, Spain, Italy, UK, Netherlands |
| Ciccone & Peri 2006, REStud 73 | Table 4: scale 0.081 (0.027), 0.16 (0.06), 0.11 (0.04); schooling −0.004 (0.017), 0.014 (0.03), −0.01 (0.018); Table 5 −0.001 (0.021) | 163 US cities, 1970–1990 |
| Acemoglu & Angrist 2000, NBER w7444 | Table 6: 0.004 (0.035), 0.017 (0.043) | US states, white men 40–49, 1960–1980 |
| Iranzo & Peri 2009, NBER w12440 | Table 8: 0.06 (0.025) / −0.01 (0.01); 0.12 (0.04) / 0.01 (0.03); Table 9: 0.11 (0.04) / −0.01 (0.02) | US states, 1970–2000 |
| Moretti 2004, J. Econometrics (w9108) | Table 5 cols 3, 4, 6, 8 by education; Table 2 NLSY 1.27 (0.33), 1.08 (0.32) | 282 US MSAs 1980–1990; NLSY79 in 201 MSAs 1979–1994 |
| Moretti 2004, AER (w9316) | plant productivity 0.5–0.7% per point of college share | US manufacturing plants, 1982–1992 |
| Glaeser & Resseger 2010, NBER w15103 | Table 1 col 3: 0.022 (0.012), 0.411 (0.122), 0.196 (0.113) | 2.1m workers in US MSAs, 2000 |
| Rosenthal & Strange 2008, JUE 64 | Table 4 OLS ring coefficients (t-ratios above) | 730,281 workers, 297 MSAs, 2000 Census |
| Burchardi et al., NBER w27075 (Nov 2021) | Table 9 panels A–B; §6.3 structural 5% | US counties, 1975–2010 |
| Account parameters | τ 0.384 / 0.426; between-skill σ 1.5–2.5, 2 central | `matched_benefits_2026_09_19`, `wage_distribution_2026_09_23` |

The PDFs are in `_cache/`, which is ignored. Moretti's NBER PDFs have no text layer and were read
by OCR (`_cache/ocr_w9108/`, including rotated table pages). Hashes are in `_cache/manifest.json`.

## 8. Limits

- **Cross-sectional identification on both sides.** With instruments, density elasticities fall
  10–20% (Combes–Gobillon). The composition gradient may also reflect demand for skills rather
  than spillovers.
- **The composition central depends on a model step.** The CES netting uses the account's σ and
  shares from other years (CRY's sample share; θ from the 2024 earnings ratio). If local labour
  markets absorb skill mixes with less relative-wage change than the national CES implies, the
  netting is too large and the cost is understated. The σ = 2.5 and no-CES rows show that direction.
- **Transport in time and place.** CRY is 2010–2018, the literature 1960–2000, Rosenthal–Strange
  2000 and BCHTT 1975–2010. Moretti's and Iranzo–Peri's estimates are applied at the 2024 margin
  (2.8–3.0 points of college share). That margin is inside their data's range of decade changes,
  but the returns may have changed since.
- **Conditional by-education elasticities** scale both of CRY's Table 10 terms by the pooled
  conditional/unconditional ratio, 0.747 [INFERENCE].
- **The public CRY premia are predictions,** so the lane's joint regression is a projection of
  CRY's premia on two of the predictors, and its SEs are inflated by hand.
- **Rosenthal–Strange geography is crude:** residence instead of workplace, and uniform density
  within a CBSA. Uniform spreading understates exposure where jobs cluster downtown and overstates
  it on metro fringes.
- **Glaeser–Resseger** is demeaned at 2024 population-weighted means because the 2000 sample means
  are not published.
- **Moretti's sample weights** use total personal income from the IPUMS 1980/1990 extract; the
  extract has no earnings variable.
- **BCHTT** is a linear scaling of a nonlinear structural aggregate, and the bottom-tercile patent
  estimate is uninformative.
- **Native labour supply is fixed,** as in the account's central. The group's workers, and only
  they, change area size.
- **Land-rent capitalization** of the productivity gain is not priced (a transfer, see §5).

## 9. What the parent must check

1. **The composition netting.** It carries the central: without it the net is −$72.5bn. The weight
   m = 0.609 comes from CRY's point estimates, and its sampling error, if independent, widens the
   net's interval to −$212bn to +$240bn.
2. **Whether to carry the college-share instrumented estimates as a scenario.** Moretti 2004 and
   Iranzo–Peri 2009 put the net at −$109bn to −$677bn. Adopting them alone, without Ciccone–Peri's
   larger scale term from the same kind of evidence, would break symmetry rule 2.
3. **Iranzo–Peri's variable definition.** The literal definition, supported by their Table 6,
   gives −$392bn; the years-beyond-12 reading gives −$92bn.
4. **Adjacent defect in two other lanes, not fixed here.** `congestion_2026_09_23/derived/cbsa_commute.csv`
   and `housing_transfer_2026_09_23/derived/cbsa_exposure.csv` map PUMAs to 2020 counties and then
   through a 2013 county→CBSA file. Connecticut's 2022 planning regions (09110–09190) are not in
   that file, so the whole state (3.68m persons, group share 1.8%) lands in `nonmetro_09`. Hartford,
   Bridgeport–Stamford and New Haven then take nonmetro parameters. The congestion headline uses
   urban areas and is unaffected. For the housing lane the effect is probably under $0.1bn, but
   that has not been checked. This lane avoids the problem with Geocorr's 2023 CBSA layer and sets
   Connecticut to its 1990 CZ by rule.
5. **Rerun and compare**, from the repository root (all outputs reproduced byte for byte on a second
   run):

```sh
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a   # PUMS gate needs the key
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/scale_spillovers_2026_09_23/fetch.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/scale_spillovers_2026_09_23/tabulate.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 infra/immigration-fiscal/scale_spillovers_2026_09_23/sample_weights.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with statsmodels python3 infra/immigration-fiscal/scale_spillovers_2026_09_23/arms.py
```

`sample_weights.py` reads the local IPUMS extract outside the repository
(`~/research-data/immigration-fiscal/derived/immigration_microdata.duckdb`). `arms.py` also reads
the employment-entry lane's PUMA→county crosswalk (sha256 prefix in `derived/checks.json`).

## Files

- `fetch.py`: crosswalks, the CRY file, the gazetteer and the papers into `_cache/`, with sha256
  manifest.
- `tabulate.py`: ACS PUMS cells by PUMA, plus the published-table gate.
- `sample_weights.py`: census education shares for 1980, 1990 and 2000.
- `arms.py`: every specification, the gates and the outputs.
- `derived/`: `summary.csv` (the numbers in the verdict), `scale_grid.csv`,
  `composition_grid.csv`, `joint_grid.csv`, `net_grid.csv`, `innovation_bchtt.csv`,
  `metro_distribution.csv`, `area_measures_cz.csv`, `area_measures_cbsa.csv`, `cry_gradient.csv`,
  `parameters.csv`, `checks.json`, `sample_weights.csv`, `pums_*`.

Model self-report: `claude-opus-5-5[1m]`. Nothing was committed.
