**Verdict:** The group's labour makes construction cheaper. That trims the housing lane's
demand-only transfers by about a tenth, and it adds nothing to the fiscal account. The union
(Mexico-born plus US-born Mexican-origin) holds **24.4% of construction-trades jobs**: 15.4%
Mexico-born and 8.6% US-born Mexican-origin. It holds 20.0% of construction-industry jobs, and
50–66% of trades jobs in the large Sun Belt and western metros.

In the account's own factor prices (σ = 2, capital adjusting), construction costs are **0.75%
lower** with the group present (range 0.53–1.17%). The long-run housing stock is then 10.2%
larger rather than the demand-only 9.75%, and long-run rents are 4.57% higher rather than 5.14%.
That is an **offset of $3.6bn a year to other renters' $33.5bn of extra rent** (range $2.2–5.8bn).
Per head it is $91 per other renter household, $11.9 per other resident and $87 per group
member. It is also an **offset of $0.20tn to other owners' $1.91tn home-value gain** (range
$0.12–0.33tn).

Two larger variants add a construction-specific wage premium, from Monras (2020) or Bratsberg
and Raaum (2012). They raise the offset to $6.8–15.5bn a year (owners $0.38–0.88tn). Most of that
extra is a transfer out of other residents' construction wages ($12.6–24.1bn a year). Only a
triangle of $2.0–3.8bn is a net gain.

**Overlap ruling:** 77–100% of the offset (89.5% in the central case) is cheaper structures. That
is the buyers' side of the same low-skill wage changes the account's production term already
counts. It is therefore **inside P**, reported as a side view and not added. It only
reapportions the housing lane's gross renter-to-owner flows, which cancel at fiscal weight 1.
The remainder, lower land rent, corrects the housing lane's demand-only arm. It moves the lane's
welfare-net Z item by −$0.01bn (−$0.10bn to +$0.01bn across the account-consistent cases).

A construction-specific premium would sit **beside P** in the nest class (the
production-nativity nest lane's ε variants) and is not added. The main case stays at
$203.2–249.6bn.

The causal evidence, graded alike on both sides, supports two things: a short-run supply
bottleneck on new homes, and long-run local price declines. No study measures a national,
long-run cost effect. The enforcement studies with construction wages do not show costs rising
when immigrant workers are removed. Howard, Wang and Zhang's wage-cost measures stay flat, and
287(g) *lowered* construction weekly wages by 2.3% (SE 0.9). The 2025–26 surge studies measure
construction jobs only. 2026-09-23.

Model self-report: `claude-opus-5-5[1m]`. Lane brief: [`BRIEF.md`](BRIEF.md). Nothing was
committed and nothing outside this directory was edited. The housing lane's `arms.py` is imported
read-only.

## 1. Frame

This lane keeps the brief's frame: the complete annual account's stationary 2024 comparison of
the United States with and without the 40,896,574 CPS Mexican-origin residents. Effects are
measured on the other 299.2m residents, in 2024 dollars
[SOURCE: [main case](../main_case_2026_09_23/RESULT.md)]. The supply offset is priced in the
housing lane's **long-run arm**, its primary case and the one that matches the account: land is
fixed and structures are rebuilt at unit cost c. The arm uses functional form A and the lane's
primary household rule, and it calls the lane's own `load_areas()` and `evaluate()`
[SOURCE: [housing lane](../housing_transfer_2026_09_23/RESULT.md) §1–4]. The short-run arm holds
the stock fixed, so it has no supply offset by construction.

The ACS group person follows the housing lane: `HISP=02` or `POBP=303`. That gives 39.43m people,
3.7% below the CPS union. Construction shares below are not rescaled; the cost change uses shares
of earnings, which the rescaling would barely move.

## 2. The group's share of construction work (task 1) [DATA: `derived/construction_national.csv`, `derived/construction_metro.csv`]

ACS 2024 one-year PUMS, person weights, 80 replicate weights (SE in parentheses). Employed means
ESR 1–2 and earnings means PERNP × ADJINC. Trades are OCCP 6200–6765 in any industry; the
construction industry is INDP 0770 in all occupations.

| Scope | Employed | Union share of employed | Mexico-born | US-born Mexican-origin | Union share of earnings |
|---|---:|---:|---:|---:|---:|
| All workers | 167.4m | 11.3% (0.03) | 4.3% | 6.8% | 8.0% |
| Construction trades, any industry | 7.79m | 24.4% (0.25) | 15.4% | 8.6% | 21.4% |
| Construction industry, all occupations | 11.58m | 20.0% (0.17) | 11.8% (0.15) | 7.9% (0.12) | 15.8% (0.17) |
| Trades inside the construction industry | 6.70m | 25.8% (0.26) | 16.8% | 8.6% | 22.8% |
| Construction industry, high school or less | 6.55m | 27.2% (0.25) | 17.9% | 8.8% | 23.8% (0.28) |
| Construction industry, below BA | 9.73m | 22.4% (0.19) | 13.5% | 8.5% | 18.9% (0.21) |

- Workers with high school or less earn 47.2% of the construction industry's $810bn; workers
  below BA earn 76.1%. Across all industries the union holds 17.9% (0.09) of low-skill earnings
  in the ACS. That matches the account's CPS efficiency share of 17.8%.
- The Mexico-born share of construction-industry employment (11.8%) reproduces the 2026-09-18
  consumer-price lane's `t3_construction` figure
  [DATA: `../consumer_price_benefit_2026_09_18/derived/industry_shares.csv`].
- **By trade:** drywall 48.7%, plasterers 46.7%, cement masons 41.3%, roofers 40.7%, insulation
  33.3%, floor and tile 33.2%, masons 32.6%, painters 31.1%, construction laborers 30.7% (2.0m
  workers), carpenters 25.3%. The licensed and equipment trades are lowest: plumbers 15.8%,
  electricians 14.8%, equipment operators 14.6% and inspectors 10.4%.
- **By metro** (the housing lane's 2013 CBSA geography, via the Geocorr PUMA→county→CBSA
  allocation; national totals are preserved), the union's share of construction-trades jobs is:
  - 50–66% in the large Sun Belt and western markets: Riverside 65.8%, San Antonio 62.0%,
    Phoenix 61.4%, San Diego 60.1%, Dallas 60.0%, Los Angeles 56.6%, Houston 54.5%, Austin
    54.1%, Denver 50.9%, Las Vegas 50.3%;
  - 36.2% in Chicago and 28.6% in Atlanta;
  - under 10% in New York, Miami, Washington, Philadelphia and Boston.

## 3. How much cheaper is construction with the group present?

**Cost shares** [DATA: `derived/inputs_bea.csv`, BEA industry accounts]:

- **Construction (NAICS 23), 2024.** Gross output was $2,511.5bn, value added $1,305.4bn and
  compensation $799.3bn; TVA113 and NIPA 6.2D agree on compensation within $0.5bn. Proprietors'
  income was $246.1bn (NIPA 6.12D).
- **Labour's share of gross output**, counting 0.5, 0.67 or 1.0 of proprietors' income as labour:
  0.367, 0.384 or 0.416 in 2024, and 0.389, 0.408 or 0.448 in 2017.
- **New single-family structures, 2017 benchmark detail Use table** (before redefinitions):
  intermediate inputs 46.6%, compensation 37.2%, gross operating surplus 15.7%. The labour share
  including proprietors' income is 0.430, 0.450 or 0.489.

The lane uses three values of θ. The low is construction in 2024 at 0.5 of proprietors' income
(0.367). The central is the mean of construction 2024 and single-family 2017 at 0.67 (0.417). The
high is single-family 2017 counting all proprietors' income as labour (0.489).

**The account's wage changes.** These are with minus without, in logs, from the production term's
CES (capital fully adjusting, native labour supply elasticity 0, PEARNVAL, GDP normalisation)
[DATA: `../matched_benefits_2026_09_19/derived/scenarios.csv`]:

| Split | σ | Lower skill group | Upper skill group | Group's share of the lower group's efficiency units |
|---|---:|---:|---:|---:|
| high school or less | 1.5 | −7.21% | +1.93% | 0.178 |
| high school or less | 2.0 | −5.42% | +1.44% | 0.178 |
| high school or less | 2.5 | −4.34% | +1.14% | 0.178 |
| below BA | 2.0 | −3.21% | +2.20% | 0.141 |

**Cost change.** d ln c = θ·[ℓ·d ln w_L + (1 − ℓ)·d ln w_H] + premium. Here ℓ is the lower group's
share of construction earnings (0.472 for high school or less, 0.761 below BA). Capital's rental
rate is unchanged in the account's long-run case. Intermediate inputs are priced at the numeraire.
The cases [CALCULATION: `supply.py` → `derived/supply_checks.json`]:

| Case | What it adds | d ln c |
|---|---|---:|
| A_low | σ 2.5, θ low | −0.53% |
| **A_central** | σ 2.0, θ central: the account's own factor prices | **−0.75%** |
| A_high | σ 1.5, θ high | −1.17% |
| A_central_below_ba | the account's below-BA split | −0.80% |
| B_state | Monras state premium: native low-skill wage in construction minus in all sectors, −0.454 − (−0.255), × dose m/(1 − m) = 0.217, on θ·ℓ | −1.60% |
| B_metro | the same at the metro level, −0.765 − (−0.384) | −2.38% |
| B_high | B_metro at σ 1.5 and θ high | −3.08% |
| C_wage | Bratsberg–Raaum native-wage coefficient −0.724 × construction's excess ln(1 + M/N) within below-BA earnings (0.0646), on θ·ℓ_belowBA | −2.23% |
| C_price_excl_licensed | Bratsberg–Raaum price coefficient without plumbing and electrical, −0.387 × 0.0646 | −3.25% |
| C_price_all | Bratsberg–Raaum price coefficient on all activities, −1.155 × 0.0646 | −8.22% |

The premium in B and C is construction-specific: the group's concentration in construction moves
construction wages more than low-skill wages in general. The C dose is conditioned on skill,
comparing construction with all sectors inside the below-BA cell, so it does not count A's
skill-level wage change twice. An all-education dose (0.0883) would scale the C premiums by 1.37,
and an employment-based dose (0.0885 within below-BA) by 1.37 too.

Case A is the account's own general-equilibrium relative price. With the aggregate's zero-profit
condition, ℓ̄·d ln w_L + (1 − ℓ̄)·d ln w_H = 0 at the economy's ℓ̄ ≈ 0.21. So construction's cost
falls only because its low-skill share, 0.47, exceeds the economy's, and skill-intensive goods
become dearer by the mirror amount. Cravino, Levchenko, Ortega and Pandalai-Nayar (2026)
calibrate a multi-sector model with this structure. In their data, unauthorized workers are 3.2%
of US workers and 11% of construction and extraction employment. Removing half of them (about
3.7 million) changes construction's long-run relative producer price by an amount that is "small
on average" and reaches "0.8-0.9% in some regions". The union's share of construction-occupation
jobs (24.4%) is about 4.4 times that removal (5.5%). Scaled linearly, the regional maximum would
be about 3.5–4%, and the national average is smaller but not printed. Case A (0.75%) and the
premium cases (1.6–3.1%) lie below that regional maximum [INFERENCE: linear scaling of a
calibrated model's output].

## 4. The supply offset in the housing lane's model (task 3) [CALCULATION: `supply.py`; 6 tests in `test_supply.py` pass]

**Model.** Housing services are Cobb–Douglas in fixed land and structures built at cost c. The
parameters are the land share a and the per-capita demand elasticity e_D, set at the housing
lane's levels: low (0.25, 1.0), central (0.35, 0.7) and high (0.46, 0.5). Log changes with minus
without the group:

- d ln P = e_d·d ln N + π·d ln c, where e_d = a / (1 − a(1 − e_D)) and π = (1 − a) / (1 − a(1 − e_D)) = e_S / (e_D + e_S), with e_S = (1 − a)/a.
- The land-rent part of the price change is e_d·d ln N + a(1 − e_D)·π·d ln c.
- The housing stock is d ln H = d ln N − e_D·d ln P.

The housing lane's long-run arm is the special case d ln c = 0. Along the arrival path, ln c moves
in proportion to ln(1 + λg). The combined path therefore keeps the lane's form A, with
e_total = e_d + π·d ln c / ln(1 + g) and e_land = e_d + a(1 − e_D)·π·d ln c / ln(1 + g). Both are
passed to the lane's `evaluate(..., e_override=...)`:

- e_total prices renters' gross extra rent and owners' value, at a constant price-to-rent ratio,
  the lane's convention.
- e_land prices the land-rent transfer to landlords and the welfare net, the lane's Z item.

The difference between the two is cost pass-through: landlords' structure costs fall with their
rents. Pass-through π is 0.750, 0.726 or 0.701 by level, and the land part a(1 − e_D)·π is 0,
0.076 or 0.161. The tests check π and e_d against the supply–demand formula, that the land part
vanishes at e_D = 1, that zero cost change reproduces the housing lane to 1e-9, the additive log
rent change, the share-weighted cost change, and that every premium adds to its A part.

### 4.1 Central case: A_central, central housing parameters, uniform geography, central ownership

| Quantity | Demand only (housing lane) | With supply | Offset |
|---|---:|---:|---:|
| Construction cost, with vs without | 0 | −0.75% | |
| Long-run rent level | +5.14% | +4.57% | |
| Long-run housing stock | +9.75% | +10.17% | +0.38% more housing |
| Other renters' extra contract rent, $bn/yr | 33.47 | 29.91 | **3.56** (10.6%) |
| of which the land-rent transfer to landlords | 33.47 | 33.10 | 0.37 |
| of which cheaper structures (cost pass-through) | 0 | −3.19 | 3.19 |
| Other owner-occupiers' home-value gain, $tn (stock) | 1.910 | 1.707 | **0.203** (land part 0.021) |
| Group renters' extra rent, $bn/yr | 4.07 | 3.64 | 0.43 (to the group) |
| Housing lane's frame net, $bn/yr | 2.638 | 2.608 | −0.029 |
| Housing lane's welfare net (Z item), $bn/yr | 0.708 | 0.700 | −0.008 |

The offset is $91 per other renter household (38.99m households), $11.9 per other resident and
$87 per group member. The structure part of owners' value, $0.18tn, is a lower replacement cost:
owner-occupiers hold a cheaper asset and consume correspondingly cheaper housing services, so only
the $0.02tn land part changes their net position.

In the metro-local geography, each area's cost change is scaled by its union share of
construction-trades earnings relative to the national 21.4%. The offset there is $3.44bn and the
welfare net moves from $3.508bn to $3.482bn.

**Break-even.** The group's net long-run rent effect would vanish only if construction were
4.3%, 6.9% or 10.9% cheaper with the group present (low, central, high levels). That is 6–15
times case A.

### 4.2 Every specification computed

There are 180 cells: 10 cost cases × 3 housing levels × 2 geographies × 3 ownership variants
[DATA: `derived/supply_grid.csv`; central-ownership subset `derived/supply_headline.csv`]. The
central column is the central level, uniform geography and central ownership. Each range spans
the case's levels, geographies and ownership variants. "Z change" is the with-supply minus
demand-only welfare net.

| Case | d ln c | of which premium | Rent | Stock | Offset $bn (central) | Range | Share of demand-only | Per other resident | Per group member | Owners' offset $tn | Range | Land part $bn | Z change $bn | Z range |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A_low | −0.53% | 0 | +4.73% | +10.05% | 2.52 | 2.2–2.7 | 7.5% | $8.4 | $62 | 0.14 | 0.12–0.15 | 0.26 | −0.006 | −0.05 to 0.00 |
| **A_central** | **−0.75%** | 0 | +4.57% | +10.17% | **3.56** | 3.2–3.7 | 10.6% | $11.9 | $87 | 0.20 | 0.18–0.21 | 0.37 | −0.008 | −0.07 to +0.01 |
| A_high | −1.17% | 0 | +4.25% | +10.40% | 5.55 | 4.9–5.8 | 16.6% | $18.5 | $136 | 0.32 | 0.27–0.33 | 0.58 | −0.013 | −0.10 to +0.01 |
| A_central_below_ba | −0.80% | 0 | +4.53% | +10.20% | 3.78 | 3.3–4.0 | 11.3% | $12.6 | $92 | 0.22 | 0.19–0.23 | 0.40 | −0.009 | −0.07 to +0.01 |
| B_state | −1.60% | −0.85% | +3.92% | +10.65% | 7.62 | 6.8–8.0 | 22.8% | $25.5 | $186 | 0.43 | 0.38–0.46 | 0.80 | −0.017 | −0.14 to +0.01 |
| B_metro | −2.38% | −1.63% | +3.34% | +11.09% | 11.35 | 10.1–11.9 | 33.9% | $37.9 | $278 | 0.65 | 0.56–0.68 | 1.18 | −0.026 | −0.21 to +0.02 |
| B_high | −3.08% | −1.91% | +2.81% | +11.48% | 14.73 | 13.1–15.5 | 44.0% | $49.2 | $360 | 0.84 | 0.73–0.88 | 1.53 | −0.033 | −0.27 to +0.02 |
| C_wage | −2.23% | −1.48% | +3.45% | +11.00% | 10.66 | 9.5–11.2 | 31.8% | $35.6 | $261 | 0.61 | 0.53–0.64 | 1.11 | −0.024 | −0.20 to +0.02 |
| C_price_excl_licensed | −3.25% | −2.50% | +2.68% | +11.58% | 15.57 | 13.9–16.4 | 46.5% | $52.0 | $381 | 0.89 | 0.77–0.93 | 1.62 | −0.035 | −0.29 to +0.02 |
| C_price_all | −8.22% | −7.47% | −0.95% | +14.43% | 40.06 | 36.2–42.6 | 119.7% | $133.9 | $980 | 2.29 | 2.01–2.41 | 4.10 | −0.088 | −0.73 to +0.06 |

- **Account-consistent (A) cases:** $2.2–5.8bn a year, 4.5–27% of the demand-only transfer; owners
  $0.12–0.33tn.
- **Premium cases (B and C_wage):** $6.8–15.5bn; owners $0.38–0.88tn.
- **C_price_all** passes the central break-even: other renters would pay $6.6bn a year *less*
  with the group than without. It rests on cost-based price indices that include immigrants'
  lower pay, and it is driven by two licensed trades. It is an upper bound, not a candidate central
  (§5).
- Across all 180 cells the welfare net moves by −$0.73bn to +$0.06bn; in the A cases, by −$0.10bn
  to +$0.01bn.

### 4.3 Who pays for a construction-specific premium [CALCULATION: `derived/supply_premium_incidence.csv`]

A premium lowers the wages of every construction worker in its cell, the group's and everyone
else's. Buyers of construction gain the lower wages paid to other residents, which is a transfer,
plus a triangle over the group's own earnings in the cell. Only the triangle is net for
non-members.

| Premium (cases) | Wage change in cell | Group earnings in cell $bn | Other residents' earnings in cell $bn | Transfer from other residents' construction wages $bn/yr | Net triangle $bn/yr | Other residents' share of triangle $bn |
|---|---:|---:|---:|---:|---:|---:|
| Monras state (B_state) | −4.32% | 91.0 | 291.5 | 12.6 | 2.0 | 1.7 |
| Monras metro (B_metro, B_high) | −8.27% | 91.0 | 291.5 | 24.1 | 3.8 | 3.3 |
| Bratsberg–Raaum wage (C_wage) | −4.68% | 116.6 | 499.4 | 23.4 | 2.7 | 2.4 |

The other residents' share assumes the group buys construction in proportion to its population
share of 12.0% [ASSUMPTION]. The housing offsets in §4.2 are part of the buyers' gross gain.

### 4.4 Local-transport arm: Monras's long-run rent coefficients [CALCULATION: `derived/supply_monras_transport.csv`]

The housing lane's short-run arm transports local demand estimates to the national stock. The
matching treatment here transports Monras's local long-run rent coefficients, which combine the
demand and supply effects, to the national stock. His regressor is Mexican immigrants relative to
low-skilled workers. The main dose is Mexico-born low-skill employed over other low-skill
employed, 0.106 (his treatment). The union dose, 0.236, also removes the US-born members, whom
his variation does not cover.

| Coefficient | Dose | Point: other renters' rent change $bn/yr | 95% CI |
|---|---|---:|---:|
| State, −0.548 (0.366) | Mexico-born | −41.0 (rents −6.0%) | −98.4 to +12.2 |
| Metro, −1.171 (0.518) | Mexico-born | −90.6 (rents −13.2%) | −178.9 to −11.4 |
| State | union | −94.7 (rents −13.8%) | −238.6 to +26.9 |
| Metro | union | −218.3 (rents −31.9%) | −463.0 to −25.7 |

This arm is not credible nationally, and it is reported for symmetry only. A local long-run price
decline includes natives and other migrants moving away from high-immigration places, and that
relocation nets out nationally. Monras's own finding is that "Internal relocation dissipates this
shock spatially". Transport therefore overstates a national supply effect, just as transporting
local demand estimates can understate a national demand effect [INFERENCE]. The housing lane's
short-run arm and this arm are mirror sensitivities, and neither enters the account.

## 5. Causal evidence, graded alike (task 2)

Every estimate and quote below was re-found in the text read, and the version is named.
`quote_check.py` re-finds 96 strings from the nine sources, with 0 missing; altered strings fail
it. The files in `reads/` carry their own checks: 43 strings in `search_gaps.md` and the
Bratsberg–Raaum file's own list. "For" means the evidence supports a supply channel through which
the group lowers construction costs or raises building.

| Study (version read) | Population, period | Design | Estimates (SE or CI) | Reading |
|---|---|---|---|---|
| Howard, Wang and Zhang, "Cracking Down, Pricing Up: Housing Supply in the Wake of Mass Deportation", working paper, 10 Nov 2025 (`_cache/papers/hwz_nov2025.pdf`) | US counties; CoreLogic sales of 4.59m new homes and resales, 2005–2012; Secure Communities rollout 2008–2013 (identifying variation 2009–2013); about 300,000 removals | Staggered DiD (Borusyak et al. 2024), county FE, house-price-appreciation-bin and population-bin × region × year FE | New units −0.165 (0.068) per 1,000 residents (−5.7%); new-home price +4.5% (1.1), quality-adjusted +4.4% (1.0); resale price +0.1% (1.1), by quartile of undocumented share +3.4 (0.9), +2.0 (0.9), −1.0 (1.4), −4.1 (2.0); construction workers −1.014 (0.371) per 1,000 = −2.7% (low-education foreign-born −0.772 (0.109), US-born −0.163 (0.337)); low-education foreign-born construction wages +4.2% (1.3), US-born −0.3% (1.1); RSMeans union wage-cost index −0.64 (0.44) points, "a decline of 77bps" of a mean of 83; ACS and QCEW log wages −0.01 (0.01) | **For** a short-run bottleneck on new homes. **Against** a short-run cost channel: no construction wage-cost measure rose, and existing-stock prices are flat on average. The dose is small (2.1% of construction workers). The brief's description, "labour shortages and housing affordability", fits this paper; no search was made for another title. |
| Monras, "Immigration and Wage Dynamics: Evidence from the Mexican Peso Crisis", *JPE* 128(8): 3017–3089, 2020 (accepted manuscript, 21 Oct 2019, doi:10.1086/707764) | US states (51) and metros (135), 1990–2000 | Decade IV on the relative inflow of Mexicans (over low-skilled workers), instrumented with the peso-crisis shift-share | Long-run log rent −0.548 (0.366) state, −1.171 (0.518) metro; house-price index −0.780 (0.424), −1.430 (0.704); first-stage F 42.73 and 15.89. Native low-skill wages in construction −0.454 (0.213) and −0.765 (0.330) against all sectors −0.255 (0.160) and −0.384 (0.232). New single-family construction 1994–2000 (states) +2.159 (0.329) | **For**: lower long-run local prices, attributed to construction costs, and more building. The state rent CI includes zero. The paper's back-of-envelope, "prices should decrease by around .6*1.4=.84", adds a composition term: the 0.4 is the native–Mexican wage gap, "around 40 percent", so lower Mexican pay counts as a cost saving. The native-wage term is a local elasticity of about −1. The estimates are local and relative. |
| Bratsberg and Raaum, "Immigration and Wages: Evidence from Construction", *EJ* 122(565): 1177–1205, 2012 (CReAM DP 06/10, April 2010, read; journal text not read) | Norway, full-time workers in 16 construction activities, 1998–2005; 8 activities with price indices (63 activity-years) | Activity, year and individual FE; licensing kept immigrant shares flat in electrical, plumbing and road work | Native daily wage −0.724 (0.202) per unit ln(1 + M/N), stock elasticity −0.06; building-cost price −1.155 (0.214), without plumbing and electrical −0.387 (0.088); placebo outside construction −0.018 (0.127) | **For**, within construction. Effects are relative across trades (year FE absorb the sector). The price indices are "largely cost-based" with fixed input weights, so they include immigrants' lower pay, and the full-sample price result leans on the two licensed trades. [`reads/bratsberg_raaum_ej_2012.md`] |
| González and Ortega, "Immigration and Housing Booms: Evidence from Spain", *J. Regional Science* 53(1): 37–59 (IZA DP 4333, July 2009, read) | 50 Spanish provinces, 1998–2008 (500 province-years) | IV on historical settlement by origin | New units per immigrant 0.462 (0.033) (Table 5 col. 5, levels); normalised 0.906 (0.383) (Table 4 col. 5); house prices +3.2% per immigrant inflow of 1% of population | **For** higher quantities, but a total demand-plus-supply effect: it cannot separate a cost channel. The authors' "the supply of housing would probably have been much more inelastic" is not estimated. Spanish boom decade. |
| Cabral and Steingress, "Immigration and US Shelter Prices: The Role of Geographical and Immigrant Heterogeneity", Bank of Canada SWP 2024-40, updated 24 Oct 2024 | 3,079 US counties, 5-year differences, 1985–2019 | IV on ancestry composition, F = 19 (col. 3) | House prices 3.486 [0.862] per 1% inflow, × immigrant education 1.377 [0.487]; rents 2.041 [0.446], × education 0.854 [0.252]; single-family permits −0.134 [0.065], multifamily +0.711 [0.085] | **Neutral**. Low-education inflows lower prices, which "could be a result of outmigration of current residents or a change in preferences of natives". Neither that nor a cost channel is tested. Multifamily supply responds to demand. |
| Wilson and Zhou, "The Impacts of Unauthorized Immigration on U.S. Labor and Housing Markets: New Evidence from Administrative Microdata", Dallas Fed WP 2607, 6 Mar 2026 | 343 MSAs, 2021m3–2024m3 | Shift-share IV on unauthorized worker flows (UIWF), F 14.05 | Permits per initial housing units per 1% of employment: total −0.208 (0.213), single-family −0.227 (0.170), multifamily +0.010 (0.065); house prices +2.189 (0.741), rents +1.438 (0.344) | **Against** a short-run supply response: "UIWF acted primarily as a housing demand shock in an environment of relatively fixed short-run housing supply". The window is three years and the first stage is modest. |
| East, Luck, Mansour and Velásquez, "The Labor Market Effects of Immigration Enforcement", IZA DP 11486, April 2018 (published *JOLE* 41(4): 957–996, 2023, with Hines added; not read) | PUMAs, ACS 2005–2014, men 20–64 | Secure Communities staggered rollout, PUMA and year FE, PUMA trends | Construction employment per 100k: low-skill non-citizen men −90.4 (25.4) on a mean of 535.8 (−17%); citizen men −15.4 (50.6) on 3,836 (−0.4%, CI −3.0% to +2.2%) | **Neutral**: removals cut the group's construction employment without detectable citizen gains or losses. No cost or price outcome. |
| Cravino, Levchenko, Ortega and Pandalai-Nayar, "The Economic Impact of Mass Deportations", NBER w34790, Feb 2026 | Calibrated multi-region, multi-sector US model, 2024 ACS shares; removal of 50% of unauthorized workers (about 3.7 million; the unauthorized are 3.2% of US workers) | Model (ε = 3, η = 1.6); no sampling error | Construction's long-run relative producer price change is "small on average", reaching "0.8-0.9% in some regions"; some construction occupations' native wages +0.8% | **Model, not evidence.** A general-equilibrium relative-price effect of the same kind as case A, not a premium. Used only as a magnitude cross-check (§3). |
| Bohn and Santillano, "Local Immigration Enforcement and Local Economies", *Industrial Relations* 56(2), April 2017 (journal text, read by the reader lane) | 187–274 US counties, 50–55 with 287(g) agreements, against contiguous neighbours; QCEW 2004Q1–2010Q4 | Contiguous-pair DD on 287(g) coverage, pair × quarter FE (preferred col. 4) | Construction employment −0.020 (0.016), 95% CI −5.1% to +1.1%; construction weekly wages −0.023 (0.009), CI −4.1% to −0.5%; all-industry employment +0.001 (0.009) | **Against** a shortage-driven cost rise: removals lowered construction wages. The authors read this as lower local demand. QCEW averages would rise by composition if low-paid workers left the books, so the fall is not a composition artefact [INFERENCE]. [`reads/search_gaps.md` §A1] |

**Grading, rules 1–3.** The same flaw is graded the same on both sides:

- **Local-to-national transport.** Monras and Bratsberg–Raaum are local or relative estimates, so
  they enter as sensitivity arms (B, C and §4.4). The housing lane's local demand estimates enter
  its short-run arm on the same footing. Both lanes' centrals are the long-run model.
- **Short windows.** Wilson–Zhou's three-year, F-14 window and HWZ's 2009–2013 bust-period window
  are both treated as short-run evidence outside the stationary frame.
- **Composition in cost measures.** Monras's back-of-envelope and Bratsberg–Raaum's cost-based
  price indices both count lower immigrant pay as a cost saving; both are graded as upper bounds.
- **Interpretive readings.** Two claims are untested readings, not estimates, and are flagged as
  such: Cabral–Steingress's out-migration reading of the low-education price pattern, and HWZ's
  complementarity reading of US-born job losses (whose construction coefficient, −0.163 (0.337),
  is insignificant).
- **Affiliation.** Working papers from the Federal Reserve, the Bank of Canada, NBER, IZA and
  university authors carry the same weight: none.

**Lean, rule 4.** There are eight empirical studies with a construction outcome; Cravino et al.
is a model and is not counted.

- **For a supply channel (four):** HWZ on quantities, Monras, Bratsberg–Raaum and González–Ortega.
- **Against a short-run cost channel (two):** Wilson–Zhou and Bohn–Santillano. HWZ's own
  wage-cost measures point the same way.
- **Neutral (two):** Cabral–Steingress and East et al. The 2025–26 surge studies below measure
  construction jobs only.

The audited set leans toward a supply channel on quantities and prices, but against rising
construction costs when immigrant workers are removed.

This lane's choices lean toward a smaller offset. Case A as the central gives the smallest
offset computed. The case for A is that it is the account's own factor prices and needs no
unmodelled segmentation. Taking B_state instead would double the gross offset to $7.6bn. But the
premium's net value to other residents is only its $1.7bn share of the triangle; the rest is a
transfer from other residents' construction wages (§4.3). The choice of central therefore moves
the gross distributional flows by up to about four times, and the net by at most $3.3bn.

The two enforcement studies with construction wages, HWZ and Bohn–Santillano, give no sign of a
construction-specific native wage premium. A premium is what cases B and C assume. On that
evidence, A is the better-supported central, not merely the smaller one.

**Search gaps** [`reads/search_gaps.md`, quote-checked by the reader lane]:

- **287(g), E-Verify and Arizona.** Bohn–Santillano is the only enforcement study besides HWZ
  with a construction estimate (in the table). The Legal Arizona Workers Act papers (Bohn and
  Lofstrom 2012; Bohn, Lofstrom and Raphael 2014) and the E-Verify papers (Orrenius and Zavodny;
  Amuedo-Dorantes and Bansak; Ayromloo, Feigenberg and Lubotsky) use construction only as a
  validity check or a control. The last two were checked by full-text search, not read line by
  line.
- **The 2025–26 surge.** Three studies rank construction among the hardest-hit sectors:
  - Cox and East (NBER w35129) find the largest negative sector effect in construction, shown in a
    figure only and mostly insignificant by sector.
  - Escobari, Seyal and Beach (Brookings, 29 May 2026) put construction employment "nearly 4%"
    below its counterfactual, against 1.48% overall, with no interval in the text.
  - Wilson's FRBSF letter (17 Feb 2026) lists construction among the largest slowdown effects.

  None measures starts, permits or building costs. A search summary attributed a "5% construction
  workforce → 7.8% fewer permits" result to the Dallas Fed. No such study exists in its
  publications, so the claim is treated as fabricated and not used.
- **Mechanisation and productivity.** No construction-specific causal study links immigrant labour
  to slower mechanisation, prefabrication or capital deepening. D'Amico, Glaeser, Gyourko, Kerr
  and Ponzetto (NBER w33188) attribute construction's productivity stagnation to land-use
  regulation and contain no immigration term. Lewis (the working version of QJE 2011) studies
  manufacturing. Ting and Jin (Singapore, 2000) is descriptive.

Hernandez (2026), which Cox and East cite for foot traffic at construction-related locations, and
four other surge papers were located but not read.

## 6. Overlap ruling (task 4)

The account's production term is a one-good CES economy with constant returns: capital adjusts,
native labour supply is fixed in the central, and substitution is perfect within skill. Construction
output is part of that one good. The table takes the supply effect channel by channel.

| Channel | Size (central; range) | Where it sits | Why |
|---|---|---|---|
| Structure-cost pass-through to renters and owners (case A) | $3.19bn of the renters' offset; $0.18tn of owners' value | **Inside P**: side view, not added | It is the buyers' side of the low-skill wage fall that P already counts on the workers' side. The aggregate's zero-profit condition makes construction cheaper only as skill-intensive goods get dearer, so at the aggregate it nets to zero. It reapportions the housing lane's gross flows: renters pay $29.9bn rather than $33.5bn more. |
| Land-rent part (lower land rents when structures are cheaper and e_D < 1) | $0.37bn of renters' offset; $0.02tn of owners' value; Z item −$0.008bn | **Correction to the housing lane's demand-only arm**, applied to its disclosed Z item | The one-good account has no land, so land rent is outside P and F; the housing lane priced it with d ln c = 0. The correction is −$0.10bn to +$0.01bn across the A cases, well inside the lane's own range. |
| Construction-specific wage premium (B, C_wage) | Triangle $2.0–3.8bn; transfer $12.6–24.1bn | **Beside P, in the nest class**; not added | A sector premium is segmentation that the account's single labour market per skill cannot contain. Only the triangle is net; the transfer cancels at fiscal weight 1. It must not be stacked on the production-nativity nest lane's ε arms without a joint model, because both change how much natives' wages fall. |
| Cost-index premium (C_price_*) | Offset $13.9–42.6bn | Upper bound only | Includes the lower pay of immigrant workers (composition), which the account's efficiency units treat as lower productivity. |
| Local long-run transport (Monras) | −$41bn to −$218bn in rent | Sensitivity only; not added | It includes spatial relocation that nets out nationally (§4.4). The mirror of the housing lane's short-run arm. |
| Short-run bottleneck (HWZ: new-home prices +4.5% for 2.7% fewer construction workers) | Not priced | Outside the stationary frame | A transition effect on the flow of new homes. Resale prices on average did not move. |

The fiscal account is unchanged: $203.2–249.6bn. The housing lane's Z item becomes +$0.70bn to
+$3.48bn (it was +$0.71bn to +$3.51bn in the central cells).

**What the other lanes cover, so nothing is counted twice:**

- **Housing transfer (cost side, `../housing_transfer_2026_09_23/`)**: the demand side of the same
  market. This lane is its supply-side correction and uses its code and geography.
- **Wage distribution (`../wage_distribution_2026_09_23/`)**: the workers' side of the same factor
  prices. Less-educated natives' wage losses of −$66–166bn a year include the construction
  workers' losses that finance the structure-cost pass-through. Both are inside P.
- **Consumer prices (`../consumer_price_benefit_2026_09_18/`)**: prices childcare, housekeeping,
  lawn care, laundry, apparel repair, personal care, elder and adult day care, pest control,
  moving and food away from home (`compute.py` `MAP`). It prices no shelter, construction or home
  repair, so there is no overlap.
- **Care and household services (`../care_household_services_2026_09_23/`)**: cheaper household
  services and native women's hours. It does not cover construction.
- **Labour mobility and insurance (`../labor_mobility_insurance_2026_09_23/`)**: the group's
  greater mobility across local shocks. Monras's spatial dissipation belongs there; §4.4 is not
  added here.
- **Scale spillovers (`../scale_spillovers_2026_09_23/`)**: agglomeration and human-capital
  spillovers, a distinct channel.
- **Congestion, crime victim cost, criminal-justice use, uncompensated care (cost lanes)**: these
  are distinct channels with no housing-supply term.
- **Distribution weights (`../distribution_weights_2026_09_23/`)**: the offset moves about $3.6bn
  a year of housing cost from renters, who have lower incomes, to the construction wage bill.
  Distributionally weighted, it counts for more than its dollar value. That lane should take the
  with-supply renter flows.

## 7. Limits

- **Intermediates at the numeraire.** Materials are 46.6% of single-family output. Suppose half
  their cost were labour with a 30% low-skill share, against the economy's 21%. Case A would then
  grow by about 0.14 points, to −0.89% [INFERENCE, assumed shares].
- **The premium cases transport relative estimates.** Monras's are across US places (1990–2000)
  and Bratsberg–Raaum's across Norwegian trades (1998–2005); both become a national
  construction-versus-rest premium. HWZ's null US-born construction wage response to enforcement,
  −0.3% (1.1), is weak evidence against a large native premium. Its dose was about a tenth of the
  group's.
- **Lower pay as a cost saving.** If the group's workers are paid below their marginal product
  (an undocumented wage penalty), buyers capture a transfer that the account's efficiency-unit CES
  does not contain. It is not priced here.
- **One national cost change** in the uniform geography. The metro-local variant scales it by the
  local union share, which assumes local construction labour markets and so sits uneasily with the
  national CES; it is a sensitivity.
- **Form A only.** The housing lane's forms B and C were not re-run. The dollar offset is roughly
  invariant across forms, since it is about the rent base × π × |d ln c|.
- **Joint extremes in A.** A_low and A_high move σ and θ together, so they are extremes rather
  than every combination.
- **ACS count.** The ACS union is 3.7% below the CPS count. Rescaling would raise the construction
  shares proportionally, but the cost change uses the account's CPS wage changes and ACS earnings
  shares.
- **Other construction.** The cost change applies to all structures. Cheaper non-residential and
  public construction is inside P by the same argument and is not priced separately.

## 8. What the parent must check

1. Accept or reject the overlap ruling that the structure-cost pass-through is inside P. If it is
   accepted, the housing lane's headline flows should be quoted with supply: renters $29.9bn, and
   owners $1.71tn, of which the land part is $0.02tn lower.
2. Whether to adopt a construction-specific premium. If so, add only the triangle ($1.7–3.3bn to
   other residents) in the nest class, alongside the production-nativity nest lane rather than on
   top of it.
3. Version gaps. The Bratsberg–Raaum numbers come from the 2010 discussion paper, and East et
   al.'s from the 2018 discussion paper; the journal versions were not read. The Brookings
   construction figure ("nearly 4%") has no interval in the text read.
4. Do not use the "Dallas Fed: 5% construction workforce → 7.8% fewer permits" figure that
   circulates in search summaries; no source for it exists (`reads/search_gaps.md` §B5).

## 9. Reproduce

From the repository root:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/construction_housing_supply_2026_09_23/tabulate.py   # ACS PUMS, about 10 min
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/construction_housing_supply_2026_09_23/metro.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/construction_housing_supply_2026_09_23/inputs.py     # needs _cache/bea/
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/construction_housing_supply_2026_09_23/supply.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/construction_housing_supply_2026_09_23/ -q
uv run --no-project python3 infra/immigration-fiscal/construction_housing_supply_2026_09_23/quote_check.py   # needs _cache/papers/ and ~/Projects/corpus
```

`tabulate.py` reads `sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip`.
`metro.py` reads the employment-entry lane's Geocorr crosswalk and the hedonic lane's 2013
county→CBSA file. `inputs.py` reads BEA files in `_cache/bea/` (AllTablesIO.zip, GrossOutput.xlsx,
ValueAdded.xlsx, Section6All_xls.xlsx; download log in `_cache/bea/download.log`). `supply.py`
imports `../housing_transfer_2026_09_23/arms.py` and reads
`../matched_benefits_2026_09_19/derived/scenarios.csv`.

## 10. Files

| File | Content |
|---|---|
| `tabulate.py` | ACS 2024 PUMS: employment, earnings and hours by trade, industry, education and group, with replicate SEs |
| `metro.py` | PUMA cells → 2013 CBSAs on the housing lane's geography |
| `inputs.py` | BEA cost shares |
| `supply.py` | cost cases, the supply offset in the housing lane's model, premium incidence, Monras transport |
| `test_supply.py` | 6 tests |
| `quote_check.py` | re-finds the 96 quotes and source numbers this RESULT takes from the papers read in the lane |
| `derived/construction_national.csv` | national shares by dimension, category, education, measure and group, with SEs |
| `derived/construction_puma.csv`, `derived/construction_metro.csv` | PUMA cells and metro shares |
| `derived/inputs_bea.csv` | BEA items with source cells |
| `derived/supply_grid.csv`, `derived/supply_headline.csv` | all 180 cells; central-ownership subset |
| `derived/supply_premium_incidence.csv` | transfer and triangle for each wage premium |
| `derived/supply_monras_transport.csv` | the local-transport arm |
| `derived/supply_parameters.csv`, `derived/supply_checks.json`, `derived/tabulate_checks.json` | parameters with sources; cost changes; row counts |
| `reads/INDEX.md`, `reads/bratsberg_raaum_ej_2012.md`, `reads/search_gaps.md` | reader-lane extractions with their own quote checks: Bratsberg–Raaum, 287(g), E-Verify and Arizona, the 2025–26 surge, mechanisation |
| `_cache/` (ignored) | papers, BEA files, logs |

## 11. Covered and skipped

- **Covered.** Tasks 1–4. All ten cost cases in every housing level, geography and ownership
  variant.
  - Seven of the nine studies in the §5 table were read in full text in this lane and their
    numbers re-found with `quote_check.py` (Monras and Wilson–Zhou from the corpus parses).
  - Bratsberg–Raaum and Bohn–Santillano were read by the reader lane and quote-checked there; the
    numbers used from both are also re-found by `quote_check.py`.
  - The reader lane also covered 287(g), E-Verify and Arizona, the 2025–26 surge, and
    mechanisation (`reads/search_gaps.md`).
- **Skipped.**
  - The housing lane's forms B and C and its alternative household rules: the offset is roughly
    form-invariant (§7).
  - The short-run arm: it has no supply channel.
  - A nest-consistent construction premium: that needs the production-nativity nest lane's model.
  - The published versions of East et al. (JOLE 2023) and Bratsberg–Raaum (EJ 2012): not read;
    the discussion papers were.

## Revisions

2026-09-23: Connecticut planning regions (09110–09190) now map to 2013 CBSAs in the shared crosswalk (`metro.py` and `supply.py` rerun); `construction_metro.csv` goes 424 → 428 areas. The §4.1 central case uses uniform geography and is unchanged ($29.91bn after the $3.56bn offset). Metro-local A_central: $30.41bn → $30.42bn with supply, offset $3.44bn → $3.44bn (+$0.001bn); the largest move in any cell is +$0.01bn (C_price_all, low, metro-local offset $42.57bn → $42.58bn). In the §4.2 table, one printed range changes: C_price_all owners' offset goes from $2.01–2.41tn to $2.02–2.41tn (largest stock move +$0.6bn, C_price_all low metro-local, $2.369tn → $2.370tn). Detail: [`CT_PLANNING_REGIONS.md`](../hedonic_composition_2026_09_19/CT_PLANNING_REGIONS.md).
