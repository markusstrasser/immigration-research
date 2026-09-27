**Verdict:** On the adopted main case (`sept27`, the account of $322–387bn a year), the evidence supports the
first claim in part and does not support the second as a measured claim. The schools case (`sept26_schools`)
points the same way (section D).
- **"The transfer leaks": supported in part.** Raising the revenue costs payers more than it raises (λ 1.16–1.5;
  1.29 implied by Hendren's weights). The account charges $335–396bn before its production feedback. About $50bn
  of that buys the group nothing it values, central: $41bn of offender processing and enforcement, and the
  $9.4–9.6bn by which Medicaid's value (0.92 per dollar) falls short of its cost. The Medicaid part is uncertain
  even in sign: for recipients with no implicit insurance, Finkelstein, Hendren and Luttmer's range runs from 0.76
  to 1.08 per dollar. Schooling ($214–227bn) is not a leak in the world frame, because its return is inside the
  second generation's premium. [SOURCE: reads/mcpf_sources.md, reads/hendren_2020_inverse_optimum.md,
  reads/finkelstein_hendren_luttmer_2019.md; CALCULATION]
- **"A dollar is worth less to the poorer, less productive recipient": not supported as a measured claim.** Both
  distributional weightings in the table give the group's dollars more weight than the payers', not less:
  Hendren's revealed weights give 1.02–1.05 against 0.98, and log weights give 2.7–3.3 against 2.1. The λ
  columns scale the payers' cost; that is the leak of the first claim, not a lower worth of the recipient's
  dollar. The version where payers would have invested the dollar is also a leak, through the tax its return
  would have paid. Even if all of that saving would have become domestic capital, it is $7.1–77.9bn a year, and
  the rich's added saving since 1982 financed other people's borrowing rather than investment. [SOURCE:
  reads/mian_straub_sufi_2025.md; CALCULATION] The claim survives only as the operator's moral weight w on the
  group. The US plus the group comes out behind when w is below 0.61 (equal weights; 0.69 at λ 1.16, 0.87 at
  λ 1.5), central; counting Mexico's residents, below 0.43–0.68. [FRAMING-SENSITIVE]
- **The second generation, the operator's other remark ("that's a loss... they don't send remittance").** To other
  US residents the second generation is a net fiscal cost, $128–153bn a year ($105–117bn on the schools case).
  [DATA: generation lane, convention (a)] In the world frame its row is the largest in the central, +$300bn a year
  at equal weights, mostly its place premium. The same people raised in Mexico by parents who stayed would earn
  about a quarter as much: a premium of $252bn ($241–260bn). Remittances do not decide the question. The second
  generation sends an assumed 1.6% of earnings ($5.4bn), and at equal weights remittances cancel as transfers.
  Counting only the fiscal channels, the US plus the second generation comes out behind only if its welfare weighs
  less than 0.47 of other residents' (0.64 if all of other residents' non-fiscal costs were charged to it).
  [CALCULATION: A and D; FRAMING-SENSITIVE]

Model: claude-opus-5-5. Lane: `infra/immigration-fiscal/world_ledger_2026_09_27/`. Brief: `BRIEF.md` (5296013,
corrected 2104b9e). Nothing here is committed.

## What each part rests on

| Part | Status | Depends on the fiscal case? |
|---|---|---|
| A. Place premium, G1 check, G2 rearing, G3+ bounds | built; gates pass | no |
| B. V/G per account line; Mexico's budget | ratios built; the dollar lines follow the case | lines yes, ratios no |
| C. λ, Hendren's g(y), log weights, payer conventions | built; gates pass | the others' channels yes |
| D. Party × weighting, break-even w | built on sept27 and sept26_schools | yes |
| E. Mexico's side | built; gaps marked | remittances no; the rest no |

Two full builds of both cases (`run_all.sh sept26_schools sept27`) exit 0 and give byte-identical outputs for all
32 derived files, including `acquire.py`'s source manifest, which it rewrites from the cache without downloading.
The first build started from an empty `derived/`. [CALCULATION: sha256 comparison, 2026-09-28] The repo's checker
reproduces them too (the command is under "The sept27 run").

## Tax basis: gross pay, each tax once

The ledger is on the output basis. The premium compares gross pay in both places at PPP: CPS earnings are before
taxes, and ENIGH's take-home pay is grossed up by the 2024 withholding (part A). Each country's taxes on the group
then appear once, as a transfer between the group and that country's residents:
- US: the group's row (`us_budget_value_*`) subtracts the US taxes the account counts as responding to the group,
  and `fiscal_others` credits the same taxes to other residents. On sept27 these are $394.6bn of the $492.7bn
  attributed to the group at the low end ($400.2bn of $492.5bn on the schools case). The account holds corporate
  taxes, property taxes on owners and business, government asset income and a few smaller receipts at zero
  response. The counted taxes include $88.7–88.8bn of sales, excise, customs and motor-vehicle taxes. [DATA:
  derived/valuation.csv]
- Mexico: `mexico_taxes_avoided_*` gives the group the taxes it would have paid there, and `mexico_taxes_lost_*`
  takes them from Mexico's residents. They never enter E_MX.

Every row names its basis in the `basis` column of `derived/world_ledger_rows.csv`, and a row without one stops
the run. [CALCULATION: world_ledger.py BASIS]

The Mexican taxes take three values, $bn a year. G3+ runs from its upper-premium bound to its zero-premium bound,
where it would earn its US pay in Mexico. [CALCULATION: derived/world_ledger_meta_*.json]

| Scenario | What it counts | G1 | G2 | G3+ |
|---|---|---|---|---|
| withheld (lower bound) | income tax and employee contributions on formal pay, 2024 statute | 8.4 | 6.3 | 6.5–26.4 |
| central | the withheld taxes, plus IVA, IEPS and the fuel excise on gross pay at the household decile's rate | 21.9 | 16.2 | 16.0–65.4 |
| proportional (upper bound) | all taxes in proportion to gross labor income | 68.2 | 50.0 | 48.5–197.7 |

The central's consumption taxes are SHCP's measured incidence for 2024, computed on the same ENIGH 2024. SHCP
orders households into deciles by monetary income per head, and gives the IVA and IEPS each decile pays as a share
of its autonomous income:
- decile I: 7.4%;
- deciles II–VII: 8.2–9.6%;
- deciles VIII–IX: 9.9–10.3%;
- decile X: 9.0%.

[SOURCE: reads/shcp_2026_incidence.md quotes 5–6] SHCP's incidence covers "el IEPS diferente a gasolinas y
diésel", so the fuel excise is added here. It raised MXN 403.6bn in 2024, against IVA's MXN 1,408.0bn. [SOURCE:
reads/shcp_2026_incidence.md quote 9] It is spread over the deciles the way SHCP spreads its own fossil-fuel IEPS,
by ENIGH gasoline and diesel spending: 2.5% of it falls in decile I and 24.1% in decile X. Each decile's share is
divided by that decile's income, which SHCP's IVA shares and rates imply; together they reproduce SHCP's 8.0%
average IVA rate (gate). The fuel excise comes to 2.0–2.7% of income by decile, 2.3% on average. [CALCULATION:
mexico.py `fuel_ieps_by_decile`]

Each ENIGH worker's gross pay bears the rate of their household's decile. The measurement handles three things a
flat rate would miss: zero-rated food and medicines, untaxed informal purchases, and the gap between income and
spending. The group's comparators pay 11.6% of gross pay (9.3% without the fuel excise), the same as Mexico's
workers on average. [CALCULATION: mexico.py; derived/mexico_meta.json] Five limits remain [INFERENCE]:
- the base is ENIGH's gross pay, while SHCP's is income adjusted to the national accounts;
- at the bottom deciles, the ratio includes spending out of transfers and remittances;
- IEPS is read from the data labels of SHCP's chart, to one decimal;
- the fuel excise follows households' own fuel spending, SHCP's proxy; diesel burned in freight reaches consumers
  through the prices of all goods, which would spread it more like IVA;
- import duties (MXN 137.8bn, 0.8% of income if spread like IVA) and the new-car tax are left out, so the central
  still understates the consumption burden slightly.

As a check, Mexico's 2024 taxes on goods and services over household consumption (WDI: MXN 2,065bn over MXN
23,682bn, 8.72%, the fuel excise included), applied to take-home pay, give 31% less: $9.3bn for G1 against
$13.4bn. [DATA: WDI GC.TAX.GSRV.CN, NE.CON.PRVT.CN; CALCULATION] The gap is mostly the base: SHCP's incidence is
per unit of income on its base, about MXN 17.7tn in 2024 as its IVA shares and rates imply, against MXN 23.7tn of
household consumption; the check also uses take-home rather than gross pay. An earlier build used the WDI rate as
the central and called it an upper-side proxy. The label was wrong: the proxy sits below the measured burden.

The central adds these taxes because the group's US row subtracts US sales and excise taxes. Without them,
Mexican consumption taxes would stay in the group's counterfactual income. PPP converts pesos at Mexican market
prices into dollars at US market prices. Once both countries' consumption taxes come off, the remaining error on
the Mexican side is the factor (1 + t_US)/(1 + t_MX): a few percent at most when both rates lie between 5% and
10%. [INFERENCE]

These taxes are transfers, so they leave the world total at equal weights unchanged. They do move the weighted
totals and the world break-even w. Going from the withheld bound to the central moves $62.2bn from Mexico's
residents to the group, $39.0bn of it from G3+'s zero-premium bound. It raises the world break-even w from 0.39 to
0.45 on sept27, and from 0.29 to 0.36 on the schools case. [CALCULATION]

CMP's Mexico ratio is also gross against gross: the US side is "gross earnings before taxes", and the ENIGH 2002
question read "declare su ingreso bruto". Their selection factor Ro/Re therefore applies unchanged.
[SOURCE: reads/clemens_montenegro_pritchett_2009.md quotes 6–7]

## A. The place premium, by generation (case-independent)

The premium is E_US − E_MX per person, zeros included, so employment and hours differences are part of it. Both
sides are gross pay. CPS ASEC 2025 gives E_US (PEARNVAL). ENIGH 2024 gives E_MX: take-home pay, with pay from
formal jobs grossed up by the 2024 statutory withholding, at GDP PPP 9.9166 pesos per dollar. [DATA: CPS ASEC
2025; ENIGH 2024; WDI PA.NUS.PPP; CALCULATION: g2_premium.py, mexico.py]

| $bn, 2024 | Persons (m) | E_US | E_MX gross, central | Premium low | central | high | E_US/E_MX central |
|---|---|---|---|---|---|---|---|
| G1, born in Mexico | 12.22 | 378.4 | 115.4 | 241.9 | 263.0 | 285.0 | 3.28 |
| G2, US-born, a Mexico-born parent | 14.33 | 336.4 | 84.6 | 240.5 | 251.8 | 259.8 | 3.98 |
| G3+, US-born, no Mexico-born parent | 14.34 | 334.8 | not identified | 0 | — | 252.7 | — |

[CALCULATION: derived/g2_premium.csv. G1 central: own schooling, CMP selection p56, diploma re-read 0.25; low
p70; high p50 at private-consumption PPP. G2 central: rearing, the midpoint of inheriting none and all of the
selection; low: priced at own US schooling with all of it; high: rearing at consumption PPP with none.]

**Employment and hours in each place.** These are measured, not assumed equal. G1 aged 15+ are employed 67.2% in
the US against 70.5% for the same cells in Mexico, and work 38.7 against 46.4 hours a week. For G2 the figures are
65.5% against 64.6%, and 37.5 against 44.9 hours. [DATA: CPS WORKYN, HRSWK; ENIGH trabajo_mp, htrab] At Mexico's
wage the hours not worked in the US are worth $19.2bn (G1) and $13.7bn (G2); this is reported beside the tables
and not added. [INFERENCE: leisure valued at the forgone wage; derived/world_ledger_meta_*.json hours_beside]

**The rearing convention (audit §3).** G2's comparator is the same person raised in Mexico by parents with the
same schooling who stayed. It is a controlled rearing comparison, not a history in which nobody migrated: that
history changes who is born and what Mexico's wages are. The steps:
- Parents' schooling comes from IPUMS-CPS parent links by the child's birth cohort (88.7% of children matched).
- Own schooling is drawn from ESRU-EMOVI 2017 transitions P(own | parents, sex, cohort), pooled below 30 cases.
- Ages 15–24 are priced at Mexicans of that age whose co-resident parents have the given schooling.
- The 4.18m under 15 earn nothing in either place.

[DATA: IPUMS-CPS extract sha a510e7a9…; EMOVI 2017; CALCULATION: g2_premium.py]

**Selection.** G1 sits at CMP's 56th percentile of Mexico's residual wages (δ = Ro/Re − 1 = +0.028), with a range
from the 50th (−0.093) to the 70th (+0.216). G2 inherits none or all of it, and the central takes the midpoint;
the choice moves G2 by $2.4bn. [SOURCE: reads/clemens_montenegro_pritchett_2009.md quotes 2–4; CALCULATION]

**Check against CMP.** Among G1 aged 25–64 who arrived at 20 or older, the group closest to CMP's Ro, the direct
2024 ratio at p56 is 3.00 per person. Per worker (dividing out the employment gap) it is 3.15. CMP report Ro 2.53
and Re 2.46. [CALCULATION: g2_premium.csv own_schooling_25_64_arrived_20plus; SOURCE: CMP Table 1 and p. 24]
Grossing up ENIGH closed part of the gap: the per-person ratio was 3.27 on take-home pay. CMP's Mexican wages are
gross; the ENIGH 2002 question read "declare su ingreso bruto". [SOURCE: reads/clemens_montenegro_pritchett_2009.md
quote 6] Three candidates, none measured here, may explain the rest [INFERENCE]:
- PPP vintage: CMP's 1999 dollars on World Bank (2007) factors;
- national cells rather than one urban 35-year-old male cell;
- relative wage growth between 2002 and 2024.

The CMP-based G1 premium (Re 2.46 on $378.4bn) is $224.6bn. The central uses the direct method instead, because
it prices the group's own cells. [CALCULATION]

**G3+ is bounded, not estimated.** The counterfactual is two moves removed. The lower bound is no premium; the upper
bound applies G2's Mexico-to-US ratio by sex and age band. [INFERENCE]

**Short run (sensitivity only).** Mishra (IMF WP/06/86) finds that the 1970–2000 outflow of 16% of Mexico's labor
force raised stayers' wages 8%. [SOURCE: reads/mishra_2007.md] Scaled linearly to the group's 14.9m workers (22.6%
of Mexico's employed), Mexico's wages would be lower if they returned, which raises G1's premium $11.7bn and G2's
$7.8bn. With the group away, stayer workers gain $282bn and owners of fixed factors lose $315bn: a net −$34bn
to Mexico's residents. The stayers' gain scales with the shock, and the net loss, a triangle, with its square; the
owners lose both. [INFERENCE: linear demand; derived/world_ledger_meta_*.json short_run_block] The central is the long
run on both sides: the US account's wage channel lets capital adjust, so Mexico's average wage is left unchanged.

## B. What the group values the US budget at (ratios case-independent)

The ledger keeps five columns per line: gross spending G, the group's value V, third-party value, fiscal
feedback F, and net cost (audit §2). Only V/G is applied to the account's lines. MVPFs (V/(G+F)) are not used as
valuations. [SOURCE: reads/hendren_sprung_keyser_2020.md quotes 1–2, 6]

| Class | V/G low / central / high | Basis |
|---|---|---|
| Cash, tax credits | 1 | envelope theorem on observed flows (HSK p. 20) [SOURCE] |
| SNAP | 0.65 / 1 / 1 | Whitmore's trade value "at least 65%" (HSK fn 38); inframarginal central [SOURCE; INFERENCE] |
| Housing vouchers | 0.83 / 1 / 1 | HSK Table II, HCV rows [SOURCE] |
| Medicaid | 0.76 / 0.92 / 1.08 | FHL (JPE 2019): willingness to pay with no implicit insurance, below [SOURCE; INFERENCE] |
| Medicare, public health, social services | 1 | at cost, convention [INFERENCE] |
| K–12 schooling | 0 on the group's side | the return is in G2's premium; payers carry the full cost [INFERENCE] |
| Public goods, general government | average cost | the brief's convention [FRAMING-SENSITIVE] |
| Justice | protection share 0.4247 at average cost; offender processing and enforcement 0 | cj_use_allocation central split [DATA; INFERENCE] |
| Interest, business subsidies, foreign lines | 0 | no service to the group |

**Medicaid (audit §2).** Finkelstein–Hendren–Luttmer (JPE 2019) put Medicaid's cost at G = $3,600 per
recipient-year. Of that, N = $2,152 (60%) relieves the providers of uncompensated care, leaving a net cost of
$1,448. Recipients' willingness to pay is $793–1,675, 0.2–0.5 per dollar of G. [SOURCE:
reads/finkelstein_hendren_luttmer_2019.md quotes 10–12] The alternative here is residence in Mexico, where no US
implicit insurance exists. FHL estimate that case: if the uninsured had to pay all their medical costs,
willingness to pay would rise to $2,749 or $3,875, which is 0.76–1.08 per dollar of G (quote 13). They call the
extrapolation gross, and make it for two of their three approaches. The class uses that range, with its
midpoint, 0.92, as the central. Their bridge with recipients bearing N, (γ + 0.6G)/G, gives 0.8–1.1 (quote 14),
inside it. The 60% third-party column is kept for reference only and never added, because the alternative is a
patient absent from the US. [INFERENCE on the counterfactual] Before 2026-09-28 the class used the working
paper's bridge, 0.8 / 0.9 / 1.0; the published figures raise the group's central value by $2.4bn and widen
its span.

**K–12 and the stationary-flow argument (audit §3).** Payers carry the full cost of US schooling. On the group's
side schooling gets only its custodial value, which exists in both places and cancels. Its investment return
appears as G2's premium, measured against the Mexican schooling the same person would have had (EMOVI
transitions). Mexico's residents save that Mexican schooling cost ($20.8bn for G2). [INFERENCE; CALCULATION]
Charging today's schooling against today's adult premium assumes a stationary population, where this year's
pupils stand in for the schooling already embodied in this year's adult earners. The group is not stationary: G2
has 4.18m people under 15 against 1.39m aged 25–29. The cross-section therefore charges a growing cohort's
schooling against a smaller cohort's earnings, and so leans toward cost; a cohort model would raise the premium
relative to the schooling bill. [DATA: g2_premium_by_age.csv; INFERENCE]

**Dollars (sept27; the two account ends).** The group's US budget position as it values it is +$222.1bn to
+$245.1bn (value received less taxes paid). Others pay a net direct cost of $335.1bn to $396.2bn, before the
account's production term ($322–387bn after it). [CALCULATION: derived/valuation_meta.json] The $113.0bn gap
between cost and value at the low end is the sum of five lines [CALCULATION: valuation_by_class.csv]:
- schooling at V = 0: +$213.9bn;
- offender processing and enforcement: +$40.7bn;
- Medicaid below cost, central: +$9.4bn (at the high ratio, 1.08, it is valued above cost);
- the account's correction rows, which carry no value: −$5.2bn;
- public goods valued above their responsive cost, under the average-cost convention: −$145.8bn.

At the high end the gap is $151.0bn. Under the response-only convention (V = G for public goods), the group's
valued position falls to +$76.3bn at the low end. [CALCULATION; FRAMING-SENSITIVE]

On the schools case the position is +$187.7bn to +$198.6bn against a direct cost of $271.8bn to $300.7bn. The
low-end gap is $84.1bn: schooling +$201.6bn, offender processing +$40.1bn, Medicaid +$9.4bn, corrections −$5.2bn
and public goods −$161.8bn; response-only leaves +$25.9bn. The sept27 case adds the capital return, which raises
the cost of schooling and of public goods, and long-run road and park responses, which raise the responsive cost
of public goods further. Public goods' responsive cost rises $27.7bn and their average-cost value $11.7bn, so
their excess shrinks. [CALCULATION: valuation_by_class.csv]

## C. The cost of raising the revenue, and the weights (case-independent except the channels)

| Weighting | What it does | Measured or assumed |
|---|---|---|
| equal | $1 is $1 | — |
| λ 1.16 / 1.5 | others' fiscal cost, Mexico's budget savings and Mexico's lost taxes × λ | 1.16: HSK's lowest top-rate MVPF (2013) [SOURCE: reads/mcpf_sources.md 1–2]; 1.5: Heckman–Smith's convention, "in the range suggested by Browning (1987)" [SOURCE: reads/mcpf_sources.md 6–8]; 1.25 (OMB A-94) is in weights_meta |
| λ_h = 1.286 | the MCPF Hendren's g(y) implies when payers bear tax shares: Σ share / g | [CALCULATION: g digitized × the distribution lane's tax shares] |
| Hendren a / b | each party's surplus × g(y) at its US money-income position; tax-share payers' weighted loss equals revenue (a), per-person cuts weighted by g (b) | g(y) measured: Figure 6 of NBER w20351 digitized, 1.13 at q1, minimum 0.57, 0.70 at q100, crossing 1 at q57, matching the text's "around 1.15 ... to 0.65" [SOURCE: reads/hendren_2020_inverse_optimum.md 6, 8; CALCULATION: weights.py gates]. Mexico's residents 1.15 **assumed** (the weights are US-specific, quote 12) |
| log a / b | money-metric log utility: others' channels × y_ref/y per head (floored at p5), the group by finite log changes, Mexico's residents × y_ref/y | incomes measured: y_ref = other residents' mean money income per head, $52,256 [DATA: CPS ASEC 2025]; Mexico median $5,902 and remittance households $4,716 per head [DATA: ENIGH 2024 at GDP PPP]. ε = 1 **assumed** |

The group's positions on the US scale are measured [DATA: derived/income_positions.csv]:
- G1: mean money income per head $28,362, mean percentile 35, mean g 1.052;
- G2: $29,192, percentile 38, g 1.042;
- G3+: $36,650, percentile 44, g 1.016;
- other residents: $52,256, percentile 50.5, g 0.980.

Future taxpayers are **assumed** to be financed like today's taxpayers.

**Finite changes (audit §3).** The group's log rows chain log changes in a fixed order:
1. Mexico's budget lost, net of Mexican taxes;
2. the premium, log(E_US/E_MX);
3. the US budget as valued;
4. remittances;
5. in-group victimization and care.

No endpoint income approximates a finite change. [CALCULATION: world_ledger.py group_log]

**Payer conventions (ladder 194).** Under log weights the convention matters. Per-person cuts, which are
regressive, nearly double other residents' weighted loss: −$979bn against −$517bn, central, on sept27 (−$809bn
against −$448bn on the schools case). Under Hendren's weights it matters little: −$401bn against −$407bn
(−$329bn against −$334bn). [CALCULATION: derived/world_ledger.csv; FRAMING-SENSITIVE]

## D. The world ledger (sept27, with the schools case beside it)

There are three scenario columns: the low outer span, the central and the high outer span. The low (high) outer
span holds every row at its least (most) favourable value. The three generations' US budget rows are the
exception: they move together, at the account end where the group's valued total is lowest (highest), so an
outer span never mixes the two ends' allocations (judgment call 18). The alternative world is the same for every
row: the group's 40.9m people in Mexico (descendants raised there by parents who stayed), and the US without them
as the account removes them. The window is one year, 2024.

Central scenario: G3+ premium at its lower bound (zero), public goods at average cost, Mexican taxes at the
central (withheld taxes plus consumption taxes). $bn a year, sept27. [CALCULATION: derived/world_ledger.csv;
FRAMING-SENSITIVE: every weighted total]

| Party | equal | λ 1.16 | λ 1.5 | λ_h | Hendren a | Hendren b | log a | log b |
|---|---|---|---|---|---|---|---|---|
| Other residents today | −386.6 | −440.4 | −554.6 | −482.8 | −407.3 | −400.6 | −517.0 | −979.4 |
| Future taxpayers | −13.4 | −15.6 | −20.1 | −17.2 | −13.4 | −13.4 | −10.3 | −10.3 |
| G1 | +264.9 | +264.9 | +264.9 | +264.9 | +278.8 | +278.8 | +696.0 | +696.0 |
| G2 | +299.8 | +299.8 | +299.8 | +299.8 | +312.3 | +312.3 | +1,027.1 | +1,027.1 |
| G3+ (lower bound) | +96.6 | +96.6 | +96.6 | +96.6 | +98.1 | +98.1 | +205.0 | +205.0 |
| Mexico's residents | +102.7 | +109.0 | +122.6 | +114.1 | +118.1 | +118.1 | +1,048.9 | +1,048.9 |
| World total | +363.8 | +314.3 | +209.1 | +275.2 | +386.6 | +393.3 | +2,449.7 | +1,987.3 |
| Break-even w, world | 0.45 | 0.52 | 0.68 | 0.58 | 0.44 | 0.43 | none | none |
| Break-even w, US residents only | 0.61 | 0.69 | 0.87 | 0.76 | 0.61 | 0.60 | 0.27 | 0.51 |

The same on the schools case (sept26_schools) [CALCULATION: derived/world_ledger.csv; FRAMING-SENSITIVE]:

| Party | equal | λ 1.16 | λ 1.5 | λ_h | Hendren a | Hendren b | log a | log b |
|---|---|---|---|---|---|---|---|---|
| Other residents today | −314.4 | −356.5 | −445.8 | −389.6 | −334.4 | −329.1 | −447.7 | −809.2 |
| Future taxpayers | −12.4 | −14.4 | −18.6 | −15.9 | −12.4 | −12.4 | −9.5 | −9.5 |
| G1 | +254.3 | +254.3 | +254.3 | +254.3 | +267.7 | +267.7 | +678.9 | +678.9 |
| G2 | +285.6 | +285.6 | +285.6 | +285.6 | +297.6 | +297.6 | +1,000.3 | +1,000.3 |
| G3+ (lower bound) | +80.8 | +80.8 | +80.8 | +80.8 | +82.1 | +82.1 | +175.1 | +175.1 |
| Mexico's residents | +102.7 | +109.0 | +122.6 | +114.1 | +118.1 | +118.1 | +1,048.9 | +1,048.9 |
| World total | +396.6 | +358.9 | +279.0 | +329.2 | +418.7 | +423.9 | +2,445.9 | +2,084.3 |
| Break-even w, world | 0.36 | 0.42 | 0.55 | 0.47 | 0.35 | 0.35 | none | none |
| Break-even w, US residents only | 0.53 | 0.60 | 0.75 | 0.65 | 0.54 | 0.53 | 0.25 | 0.44 |

Break-even w solves N + wM = 0, where M is the group's total and N the other parties'. "World" counts Mexico's
residents in N. Under log weights they gain so much that N is positive and no w breaks even. The US-only column
leaves them out. Mexico's row is the same in both cases, because none of its rows depends on the US account.

Break-even w (US residents only) across the scenarios, sept27 [CALCULATION; FRAMING-SENSITIVE]:

| Public goods | Mexican taxes | Scenario | equal | λ 1.16 | λ 1.5 | Hendren a | log a | log b |
|---|---|---|---|---|---|---|---|---|
| average cost | central | low outer | 0.83 | 0.93 | 1.15 | 0.82 | 0.41 | 0.70 |
| average cost | central | central, G3+ zero | 0.61 | 0.69 | 0.87 | 0.61 | 0.27 | 0.51 |
| average cost | central | central, G3+ upper | 0.46 | 0.53 | 0.66 | 0.47 | 0.19 | 0.36 |
| average cost | central | high outer | 0.33 | 0.39 | 0.50 | 0.35 | 0.14 | 0.28 |
| response only | central | central, G3+ zero | 0.74 | 0.84 | 1.06 | 0.74 | 0.30 | 0.57 |
| average cost | withheld (lower bound) | central, G3+ zero | 0.67 | 0.76 | 0.96 | 0.67 | 0.31 | 0.58 |
| average cost | proportional (upper bound) | central, G3+ zero | 0.46 | 0.52 | 0.66 | 0.46 | 0.18 | 0.34 |

The same on the schools case:

| Public goods | Mexican taxes | Scenario | equal | λ 1.16 | λ 1.5 | Hendren a | log a | log b |
|---|---|---|---|---|---|---|---|---|
| average cost | central | low outer | 0.71 | 0.80 | 0.97 | 0.72 | 0.37 | 0.60 |
| average cost | central | central, G3+ zero | 0.53 | 0.60 | 0.75 | 0.54 | 0.25 | 0.44 |
| average cost | central | central, G3+ upper | 0.40 | 0.45 | 0.56 | 0.41 | 0.17 | 0.31 |
| average cost | central | high outer | 0.29 | 0.33 | 0.43 | 0.31 | 0.12 | 0.24 |
| response only | central | central, G3+ zero | 0.68 | 0.77 | 0.97 | 0.69 | 0.28 | 0.51 |
| average cost | withheld (lower bound) | central, G3+ zero | 0.59 | 0.66 | 0.83 | 0.59 | 0.28 | 0.50 |
| average cost | proportional (upper bound) | central, G3+ zero | 0.39 | 0.45 | 0.56 | 0.40 | 0.16 | 0.29 |

A w above 1 means the US-plus-group sum is negative even at equal weight. On sept27, with the central Mexican
taxes, it happens in the low outer span and once in the central [CALCULATION: derived/world_ledger.csv]:
- average cost, low outer: λ 1.5 (1.15) and λ_h (1.01);
- response-only, low outer: every weighting except log, from 1.04 (Hendren b) and 1.06 (equal, Hendren a) to
  1.19 (λ 1.16), 1.30 (λ_h) and 1.48 (λ 1.5);
- response-only, central: λ 1.5 (1.06).

At the withheld lower bound the same cells are higher, up to 1.72 (response-only, low outer, λ 1.5); the average
cost low outer span then exceeds 1 at λ 1.16 as well (1.05). At the proportional upper bound one cell comes near
1: response-only, low outer, λ 1.5 (0.99). On the schools case, with the central taxes, w exceeds 1 only in the
response-only low outer span, at λ 1.16 (1.08), λ_h (1.17) and λ 1.5 (1.32); the average-cost low outer span
comes to 0.97 at λ 1.5.

At equal weights the world total is positive in every scenario: +$60.8bn (response-only, low outer) to +$782.2bn
(average cost, high outer) on sept27, and +$102.4bn to +$792.9bn on the schools case. The Mexican-tax scenario
does not move it, since those taxes are transfers. [CALCULATION]

**Each generation alone.** Against its own net fiscal cost to other residents (the generation lane's, the mean of
the two account ends), each generation's equal-weight row breaks even at [CALCULATION: world_ledger_meta_*.json
generation_breakeven; FRAMING-SENSITIVE]:
- G1: $86.0bn ($78.3–93.8bn) against +$264.9bn, w 0.32;
- G2: $140.3bn ($127.6–153.0bn) against +$299.8bn, w 0.47;
- G3+: $128.3bn ($100.5–156.1bn) against +$96.6bn at its zero-premium bound (w 1.33) and +$299.9bn at its upper
  bound (w 0.43).

On the schools case: G1 $67.3bn, w 0.26; G2 $111.2bn, w 0.39; G3+ $96.7bn, w 1.20 (zero premium) and 0.34
(upper).

The other residents' non-fiscal channels (wages, rents, crime, congestion, unreimbursed care and, on sept27, the
displaced beneficiaries of capped programs) are not split by generation, so they are left out; together they cost
other residents $50.7bn, central ($51.8bn on the schools case). Charging all of them to G1 or G2 would raise its
w to 0.52 or 0.64 (0.47 or 0.57). G3+ is the only generation that can be a net loss at equal weight, and only at
its zero-premium bound, where it would earn its full US pay in Mexico. [CALCULATION: generation_breakeven]

The proportional Mexican-tax bound lowers the US-only w, because the group then "gains" $316bn of Mexican taxes it
does not pay, central. G3+'s zero-premium case alone is $198bn of that. The gain is a transfer from Mexico's
residents, which the world column counts and the US-only column does not.

**Every row carries** its beneficiary, initial state, alternative state, time window, comparator status and
quantity-or-transfer kind in `derived/world_ledger_rows.csv` (audit §3). The row families:

| Rows | Party | Kind | Comparator |
|---|---|---|---|
| premium_G1/G2/G3+ | the generation | quantity | measured (G3+ bounded) |
| us_budget_value_* | the generation | transfer, valued | account lines × V/G |
| fiscal_others, induced_receipts, fiscal_future | others today; future taxpayers | transfer | the account (pinned) |
| wages, renters, landlords, mobility | others today | transfer | the account |
| crime_victims, property_crime, congestion, unreimbursed_care | others today | quantity | US measured; the same offenders' harm in Mexico unknown, not zero |
| ingroup_victims_*, uncompensated_received_* | the generation | quantity; transfer, valued | Mexico counterpart unknown, not zero (homicide 24.9 against 5.8 per 100,000) [DATA: WDI VC.IHR.PSRC.P5] |
| remit_G1/G2, remit_mexico | the generation; Mexico's residents | transfer | measured total; the split a scenario |
| mexico_budget_lost_*, mexico_budget_saved_* | the generation; Mexico's residents | transfer | measured (ENIGH, WDI) |
| mexico_taxes_avoided_*, mexico_taxes_lost_* | the generation; Mexico's residents | transfer | withheld (lower bound), plus consumption taxes (central), proportional (upper bound) |

**The two crime unknowns have a sign.** The rows leave two comparators unknown: the group's own victimization if it
lived in Mexico, and the harm its offenders would do there. Mexico's homicide rate is 4.3 times the US rate (24.9
against 5.8 per 100,000, 2023). [DATA: WDI VC.IHR.PSRC.P5] Pricing either would add a gain: to the group, safer in
the US, and to Mexico's residents, spared the offenders. Leaving them unknown therefore understates the world
total and overstates the break-even w. [INFERENCE: national rates, not the migrants' origin regions] They are not
priced, because valuing mortality risk in two countries needs a value of a statistical life by income, which is
itself a framing choice. [FRAMING-SENSITIVE]

The group-frame CES rows (the group's own wage depression, E_US − E_US*) are not added. E_US is actual earnings,
which already contain that effect, so adding them would double count (audit §3). [INFERENCE]

## E. Mexico's side (case-independent)

| Item | $bn, central | Status |
|---|---|---|
| Remittances received | 62.8 | measured: Banxico 2024 via the winners lane [DATA] |
| … of which G2 | 5.4 (1.6% of earnings; 0–5.2%) | scenario, not a measurement [INFERENCE: remit_leak arms] |
| Budget not spent on the group (schools, health, cash, public services at 0.60–0.85 response) | 143.3 (G1 39.8, G2 50.0, G3+ 53.5) | measured per person × the group's ages [DATA: ENIGH, WDI; INFERENCE: response] |
| Taxes the group would pay: withheld income tax and contributions | G1 8.4, G2 6.3 | measured lower bound [CALCULATION: statute × ENIGH] |
| … plus IVA, IEPS and the fuel excise at the household decile's rate on gross pay | G1 21.9, G2 16.2 (consumption taxes 13.4 and 9.8, 11.6% of gross pay) | central; SHCP's measured incidence plus the fuel excise, spread by fuel spending; import duties and ISAN left out [SOURCE: reads/shcp_2026_incidence.md; CALCULATION: mexico.py] |
| Taxes the group would pay: all taxes proportional to labor income | G1 68.2, G2 50.0 | upper bound [CALCULATION: WDI GC.TAX 14.8% of GDP] |
| Stayers' wages | 0 in the long run; short run +$282bn to workers, −$315bn to owners | sensitivity [SOURCE: Mishra; INFERENCE] |
| Crime the same offenders would commit in Mexico | unknown | gap, not zero |
| Human capital (schooling Mexico would have paid for) | in the budget saved: G2 $20.8bn | measured [DATA] |

The brief's "$3.7bn cap on US-born senders" was withdrawn on 2026-09-17 as circular (remit_leak_2026_09_16/RESULT.md,
correction). G2's remittances are therefore scenario rates, not a cap. The central G2 share moves money between
G1 and G2 only. Remittances change the total only under unequal weights; under log weights they dominate Mexico's
row (recipients' weight 11.1). [CALCULATION; FRAMING-SENSITIVE]

## The operator's two claims

### Claim 1: "the transfer leaks"

**Steel-man.** Raising a tax dollar costs payers more than a dollar, because taxes distort work and saving.
The dollar then reaches recipients in forms they value below cost: in-kind benefits, and services such as
prosecution that do nothing for the recipient. Some of it never reaches them, like Medicaid dollars that relieve
hospitals. A dollar moved from payer to recipient therefore arrives as less than a dollar of value.

**Evidence.** Supported in part, on both sides of the transfer.
- *Payer side (measured):* every MCPF source puts λ above 1: 1.16 (HSK's lowest top-rate estimate), 1.25 (OMB),
  1.5 (Heckman–Smith), and 1.29 implied by Hendren's weights. Hendren's own statement of the leak: "Transferring
  $1 from the top of the distribution can generate around 0.65/1.15 = $0.57 of welfare to someone at the bottom."
  [SOURCE: reads/hendren_2020_inverse_optimum.md quote 6] In the ledger, λ 1.16–1.5 raises other residents'
  weighted cost from $387bn to $440–555bn a year, central, on sept27 ($314bn to $356–446bn on the schools case).
  [CALCULATION: derived/world_ledger.csv]
- *Payer side (bounded):* the saving the payers forgo would have paid tax on its return: $7.1–77.9bn a year under
  tax shares on sept27, $5.6–61.4bn on the schools case (claim 2, reading 2). [CALCULATION]
- *Recipient side (measured ratios):* the group values $40.7–41.0bn of justice spending at nothing (sept27),
  Medicaid at 0.92 per dollar ($9.4–9.6bn below its cost, central), and SNAP at 0.65 at the low end.
  [CALCULATION: valuation_by_class.csv] The Medicaid shortfall is not established: FHL's range for recipients
  with no implicit insurance, 0.76–1.08, includes values above cost. [SOURCE: reads/finkelstein_hendren_luttmer_2019.md quote 13] HSK's adult-program
  MVPFs mostly lie between 0.5 and 2 and often below 1. [SOURCE: reads/hendren_sprung_keyser_2020.md quotes
  9–11, 14]
- *Not a leak in the world frame:* schooling. Its $214–227bn cost (sept27; $202–208bn on the schools case)
  returns as G2's $252bn premium. HSK find "an infinite MVPF for increased K-12 spending" in Jackson et al.'s
  equalizations, though their other K–12 row (Michigan) is 0.65. [SOURCE: HSK quotes 16, 23] Under the average-cost convention, public goods deliver more to
  the group than their responsive cost. [FRAMING-SENSITIVE]

**What would falsify it.** Evidence of either of the following would falsify it:
- the taxes that actually finance the group's services have an MCPF near 1, for example if the marginal financing
  is borrowing that displaces nothing;
- the group values its in-kind services at or above cost against the Mexico alternative, for example a Medicaid
  V/G above 1 for people whose alternative is no US care at all. FHL's no-implicit-insurance estimate reaches
  1.08 in one of its two approaches, so for Medicaid this falsifier is partly met; for justice spending nothing
  comparable exists.

HSK's Oregon row (WTP 1.46 per programmatic dollar) is not such evidence: its units differ from FHL's.
[SOURCE: reads/finkelstein_hendren_luttmer_2019.md cross-reference]

### Claim 2: "a dollar in a lower-class (less productive) person is worth less than in the competent person who had it taken"

**Steel-man.** It has three readings.
1. *Efficiency:* by Kaldor–Hicks, the productive payer's lost dollar is a full dollar of surplus. The recipient's
   gain arrives through a leaky bucket and is smaller, so the transfer destroys value.
2. *Productive use:* a dollar left with a high earner is saved and invested at a higher rate, raising future
   output, while the same dollar spent by a low earner is consumed.
3. *Desert:* the payer earned the dollar; its moral weight in the earner's hands is higher whatever it buys.

**Evidence.** As a claim about how much a dollar is worth to the recipient, it is contradicted by both
distributional weightings:
- Hendren's inverse-optimum weights, the weights the US tax schedule reveals, are higher at the bottom (1.15)
  than at the top (0.65).
- The group sits at g 1.02–1.05 against other residents' 0.98. [SOURCE: reads/hendren_2020_inverse_optimum.md
  quote 6; DATA: income_positions.csv]
- Log utility weights the group's dollars 2.7–3.3 times the reference, against 2.1 for other residents
  [CALCULATION].
- Under these weights the group's weighted gain grows, and the break-even w falls (0.43–0.44 under Hendren
  against 0.45 at equal weights, world, sept27; 0.35 against 0.36 on the schools case). [CALCULATION;
  FRAMING-SENSITIVE]

The three readings fare differently:
- Reading 1 is true but is Claim 1. The $0.57 conversion measures the leak of the transfer, not a lower worth of
  the recipient's dollar.
- Reading 2 is also a leak, and a bounded one. The payer values the lost dollar at a dollar whether they would
  have saved it or spent it (the envelope theorem). Their higher saving therefore matters to others only through
  the tax that the forgone saving's return would have paid, and through any spillover. HSK apply the same logic
  throughout: private responses are valued by the envelope theorem, and their tax effects enter the net cost as
  fiscal externalities. [INFERENCE; SOURCE: reads/hendren_sprung_keyser_2020.md quotes 2, 5, 21] Per dollar
  paid, the leak is θ × s_p × τ × m [CALCULATION: world_ledger.py `saving_leak`]:
  - s_p, the payers' saving rate: 0.22 under tax shares and 0.07 under per-person cuts. These are Mian, Straub
    and Sufi's saving rates by wealth group (top 1% 54%, next 9% 20%, 51st–90th percentile 12%, bottom half
    zero), weighted by the payers' shares of the cost [SOURCE: reads/mian_straub_sufi_2025.md quotes 1–3; DATA:
    distribution lane];
  - τ, the tax on the return to a marginal investment: 9.3% (CRS, economy-wide, 2024 law) to 29% (CBO,
    business capital, 2014 law) [SOURCE: reads/capital_tax_wedge.md quotes 2–4];
  - m, the pre-tax return over the rate at which the lost revenue is discounted, with the saving held
    indefinitely: 1 at OMB's 7%, 3.5 at the main case's 2% [SOURCE: quote 5; FRAMING-SENSITIVE];
  - θ, the share of the forgone saving that would have become domestic capital, is set at 1, and the group is
    taken to save none of what it receives. Both favour the reading. [assumed]

  Under tax shares the leak is 0.02–0.22 per dollar. On sept27 that is $7.1–77.9bn a year on the $349.3bn that
  taxpayers finance, and it moves the US-only break-even w at equal weights from 0.61 to 0.62–0.72 (λ 1.16 gives
  0.69). Under per-person cuts it is $2.3–25.3bn. On the schools case: $5.6–61.4bn on $275.0bn, w 0.53 to
  0.54–0.63. [CALCULATION: world_ledger_meta_*.json saving_leak; FRAMING-SENSITIVE] The favourable θ is
  doubtful: Mian, Straub and Sufi find that the rise in the top 1%'s saving since 1982 "does not boost
  investment or capital formation but instead funds dissaving elsewhere, primarily among middle-class
  households". [SOURCE: quote 2] The largest item the group receives, schooling, is itself an investment: HSK
  find large MVPFs, some infinite, for spending on children (K–12 equalizations, college attainment), and G2's
  premium is the measured return on it in this group. [SOURCE: HSK quotes 23–24] Spillovers from capital beyond
  its taxed return are not measured. [GAP]
- Reading 3 is a moral weight. Evidence cannot settle it, and the break-even table is its answer. On sept27, the
  US-plus-group sum turns negative when w is below 0.61 (equal), 0.69 (λ 1.16), 0.87 (λ 1.5) or 0.83 (low outer
  span, equal). Counting Mexico's residents, it turns negative below 0.43–0.68, and never under log weights. On
  the schools case the thresholds are 0.53, 0.60, 0.75 and 0.71, and 0.35–0.55 counting Mexico's residents.
  [CALCULATION; FRAMING-SENSITIVE]

A related fact bears on "less productive". Observably similar people earn 3.3 times more in the US than in
Mexico at equal PPP (G1, matched on own schooling), and 4.0 times more (G2, matched on parents' schooling). A large
part of their measured productivity is a property of the place, not the person, which is CMP's point.
[CALCULATION: A; SOURCE: CMP]

**What would falsify the empirical versions.**
- A measured weighting in which the social value of a dollar rises with income: inverse-optimum weights
  increasing in income, or estimates of marginal utility rising with consumption.
- For reading 2 as more than a bounded leak: evidence that the payers' forgone saving would have become domestic
  capital (θ near 1), and that capital returns to others much more than its taxed share, through spillovers. The
  first runs against Mian, Straub and Sufi's finding; the second is unmeasured here.

None of these is in hand. [GAP]

## Judgment calls

1. Public goods and general government at average cost for the group (the brief's convention); response-only
   (V = G) as the alternative convention. [FRAMING-SENSITIVE]
2. Justice: the protection share (0.4247) at average cost; offender processing and enforcement valued at zero by
   the group.
3. Medicaid at 0.76–1.08 per dollar against Mexico, 0.92 central: FHL's (JPE 2019) willingness to pay if the
   uninsured had no implicit insurance, per dollar of G. The third-party share (60%) is kept for reference only.
   Unreimbursed care the group receives, and Mexico's public health spending forgone in the alternative, are
   valued the same way; `valuation.py` writes the ratios to `valuation_meta.json`, and `world_ledger.py` reads
   them there. Before 2026-09-28 the class used the working paper's bridge, 0.8–1.0.
4. SNAP at 0.65–1; housing vouchers at 0.83–1; Medicare, public health and social services at cost.
5. K–12 at zero on the group's side, with the stationary-flow argument and its stated bias toward cost.
6. The long run on both sides; Mishra's short run only as a sensitivity.
7. G3+ by bounds only; the central is reported at each bound.
8. G2's remittances at 1.6% of earnings (0–5.2% as scenarios), held at the central in the outer spans.
9. Mexican taxes run from the withheld income tax and contributions (lower bound) to all taxes in proportion to
   labor income (upper bound). The central adds consumption taxes to the withheld taxes. Each worker's gross pay
   bears the IVA and IEPS rate SHCP measures for their household's income decile (2024, as a share of autonomous
   income), plus the fuel excise that SHCP's incidence leaves out. The 2024 fuel excise, MXN 403.6bn, is spread
   over the deciles by SHCP's own proxy, ENIGH fuel spending, and divided by the decile incomes that SHCP's IVA
   table implies. Together they come to 11.6% of the group's gross pay, 2.3 points of it fuel. The central
   mirrors the US sales and excise taxes that the group's US row subtracts, and the tables use it.
   - Left out: import duties (0.8 points if spread like IVA) and ISAN, so the central is slightly low.
   - The fuel excise swings with Mexico's fuel-price smoothing: MXN 230.1bn in 2023 against 403.6bn in 2024
     [SOURCE: reads/shcp_2026_incidence.md quote 11]. Total IEPS was MXN 117.5bn in 2022 (quote 9); if the rest
     of IEPS was near 2023's MXN 215.0bn, the fuel part was negative that year [INFERENCE]. The central uses 2024,
     the year of every other input.
   - Before 2026-09-28 the central applied Mexico's average rate on household spending (8.72%, WDI) to take-home
     pay and called it an upper-side proxy. The measured burden, fuel included, is 44% higher, so that label was
     wrong. The WDI figure stays in the meta as a check.
10. Hendren's g for Mexico's residents assumed at 1.15, the bottom of the US schedule.
11. Future taxpayers weighted like today's taxpayers.
12. Log weights per head, on money income, with the reference at other residents' mean ($52,256) and a floor at
    the 5th percentile.
13. ENIGH gross-up rules:
    - a job is formal if it is subordinate and lists SAR or AFORE;
    - IMSS rules apply to every formal worker, which understates public employees' withholding under ISSSTE;
    - the minimum-wage exemption applies, but the northern border's higher minimum does not;
    - the inversion uses a 5-peso grid.
14. A Mexico-schooled "high-school diploma" is read as secundaria with probability 0.25 (0–0.5 as sensitivity).
15. Years 6–8 are coded primaria, CEEY's categories; EMOVI's 1983–92 cohort transitions are used for later cohorts.
16. G1's central is the direct cell method, with CMP's selection; CMP's Re is a check.
17. The central is at GDP PPP; private-consumption PPP gives the high end.
18. The group's budget flows are split by generation exactly as the generation lane splits the case, under its
    convention (a), each person in their own generation. `generation_lines.cjs` repeats that lane's evaluation line
    by line at the case's band ends. The low end is spec 48, where household flows are shared among members; the
    high end is spec 11, where they are personal. `valuation.py` values each generation's lines with the union's
    classes. A gate requires each generation's lines plus its production term to equal `generation_results.csv`
    at both ends to 1e-6. It holds on both cases, as does the same gate for the uncorrected models. [CALCULATION:
    generation_lines.cjs; valuation.py value_generations; derived/generation_split_check.csv]

    Each outer span takes all three generations at one account end: the end that sets the group's total there.
    Taking each generation at its own minimum would combine one end's allocation for one generation with the other
    end's for another. That would publish a split that neither end has, and it would widen the group's span by
    $10.4–10.5bn on each side.

    This replaces the earlier build's split, which divided each class's union total by keys that followed each
    person's own flows at both ends: taxes by the wage key, age-tied cash by persons 62+, Medicare 65+, schooling
    5–24 and the rest by population. What changed on sept26_schools, over every scenario unless noted
    [CALCULATION: builds compared cell by cell]:
    - totals at equal and λ weights: unchanged; break-even w: by 0.004 at most;
    - the generation rows in the tables' central (average cost, central Mexican taxes), equal weights: G1
      +$8.7bn, G2 +$6.5bn, G3+ −$15.2bn;
    - the group's Hendren totals: up $0.3–0.9bn; its log totals: down $1.6–5.7bn.

    **Why a keyed split misses the lane.** `split_residual.py` compares the lane's split with the corrected union
    line divided by the lane's own per-line keys (the preferred key, or the receipt cell). For G1, at the high / low
    end, $bn of direct cost before the production term [CALCULATION: derived/generation_split_residual_sept26_schools.csv]:
    - split by the per-line keys: 50.0 / 76.3;
    - the keys the specification applies instead of the preferred ones: +1.2 / +0.3;
    - the correction edits, which the lane splits by its own rules: +9.4 / +11.1;
    - the three correction-only lines (schools re-priced, colleges re-keyed, lane constants): +2.2 / −1.3;
    - the lane's figure: 62.7 / 86.5.

    The edits are the gap. The generation lane applies each generation's share of the case's corrections before
    the engine, splitting each source lane's edits by a written rule rather than by the line's key. A gate shows
    that every line moves by exactly its edit times the line's response. The largest G1 steps, high / low:
    - federal income tax: +9.8 / +7.9. The edit cuts receipts $26.8bn, and 66% of the cut falls on G1 at the
      high end, whose share of the line is 29%;
    - employee and employer OASDI together: +7.6 / +5.6;
    - refundable credits: −6.7 / −1.7. The edit falls 91% on G1 at the high end, against its 56% share of the
      line;
    - Social Security: −2.6 / −2.2;
    - state and local income tax: +2.2 / +1.7.

    The receipt edits come mostly from the tax-records stack. Its status rules change only the unauthorized, all
    of them born in Mexico. In the generation lane's own accounting, the stack adds $15.1–18.1bn to G1's cost,
    against −$0.2bn to +$3.2bn for each of the other generations. The CBO re-key's federal income tax edit, by
    contrast, splits almost evenly: −$4.3bn, −$4.5bn and −$4.4bn at the high end. The refundable-credit edit is
    mostly audit row 1, which keys premium credits as the EITC. It moves −$14.2bn, of which G1 takes −$11.4bn at the
    high end and −$4.0bn at the low end. [SOURCE: generation_account_2026_09_24/RESULT.md at 2441ac8, "Lane
    contributions by generation"; DATA: its external_by_generation.json] Two other suspects contribute nothing:
    the capital return is zero in this case, and both splits use convention (a).
19. Mexico's public services respond at 0.60–0.85, the US account's range, when valuing Mexico's savings.
20. Hours and leisure are reported beside the tables, not added.
21. The productive-use leak (claim 2, reading 2) is reported beside the tables, not added to λ. Its computed
    bound takes the reading's most favourable case: every forgone dollar of saving would have become domestic
    capital (θ = 1), and the group saves none of what it receives. Mian, Straub and Sufi's saving rates by
    wealth group are applied to the payers' income percentiles. The top 1% rate is their post-1982 54%. τ runs
    from 9.3% to 29%, and m from 1 to 3.5. [FRAMING-SENSITIVE: m]
22. The sept27 additions are valued by rules fixed before any sept27 number was seen ("The sept27 run", step 2):
    each capital-return component takes its function's class, enterprise surplus is a receipt at $1 per $1, and
    rental assistance is a housing voucher.
23. Capped programs (sept27: rental assistance and LIHEAP, $5.09bn) are paid for by the eligible households that
    go without them, in a `displaced_beneficiaries` row weighted by their incidence. λ does not apply, since no
    tax is raised, and the taxpayers' row leaves them out (the fiscal channel equals A − D + F, a gate).

## Corrections to the brief's figures

- The "$3.7bn cap on US-born senders" was withdrawn by the repo's 2026-09-17 audit; G2 rates are scenarios.
- MVPF is V/(G+F), not V/G (audit §2). The brief's ranges are MVPFs, confirmed verbatim in HSK's December 2019
  revision. SNAP's 0.62 is parents' WTP per dollar of food-stamp spending; the MVPF is 1.04.
  [SOURCE: reads/hendren_sprung_keyser_2020.md]
- Hendren's paper is NBER w20351, not w23216 (a different paper). The text gives no income levels for 1.15 and
  0.65; the schedule exists only as Figure 6, digitized here. [SOURCE: reads/hendren_2020_inverse_optimum.md]
- FHL has no "preferred" estimate. The working paper's baseline is $0.2–0.4 per dollar of G and its sensitivity
  range $0.15–0.85. The published JPE version normalizes by net cost ($0.5–1.2 per dollar) and revises the
  per-recipient figures: G $3,600, N $2,152 (60%), against the working paper's $3,596 and $2,222 (62%).
  [SOURCE: reads/finkelstein_hendren_luttmer_2019.md quotes 2, 4, 5, 10, 11]
- The claim that Heckman–LaLonde–Smith (1999) "assume a 50% deadweight cost" was not found in primary text. The
  1.5 is Heckman–Smith (1998)'s convention. [SOURCE: reads/mcpf_sources.md]
- ENIGH 2024 records take-home pay. A premium on it overstates the gross gain by the Mexican withholding, and
  adding Mexican taxes on top counts that withholding twice. Both are fixed here: the premium falls $9.0bn for
  G1 and $6.8bn for G2. [CALCULATION]

## Files covered and skipped

Covered:
- CPS ASEC 2025 through `distribution_weights_2026_09_23/distribute.py`, with the IPUMS-CPS 1994–2025 extract;
- ENIGH 2024 (poblacion, ingresos, trabajos, concentrado);
- ENOE 2024 Q1–Q2 as a cross-check;
- ESRU-EMOVI 2017;
- 15 WDI series;
- the winners lane at fa1bd3a (sept26_schools) and 62f1e5a (sept27, round 2): channels, fiscal_specs,
  group_frame;
- the distribution lane at 39b854b (sept26_schools) and 78766c2 (sept27): channel_by_percentile, and for sept27 its
  capped-program incidence (`inputs.json` `capped_programs`, `financing_columns`);
- the generation lane at 2441ac8 (sept26_schools) and 8654a0c (sept27): model_{G1,G2,G3plus}.json,
  generation_corrections.json and generation_results.csv, evaluated through each case's package, read-only
  (main_case_schools_full_2026_09_26, main_case_long_run_2026_09_27) by `generation_lines.cjs`;
- the cj_use_allocation central split;
- remit_leak_2026_09_16/RESULT.md;
- the papers in `reads/`: HSK 2019 NBER, Hendren w20351, FHL w21308 and the JPE 2019 version through its PMC
  author manuscript, Heckman–Smith w6542, OMB A-94, Mishra WP/06/86, CMP (SSRN 1211427), CEEY 2019, OECD Taxing
  Wages 2025, the DOF decree of 1 May 2024, LISR art. 96, LSS art. 36, the ENIGH 2024 questionnaire, SHCP's 2026
  incidence study (results for 2024) and its January–December 2024 public-finance report (table II.3), read
  directly from finanzaspublicas.hacienda.gob.mx, Mian–Straub–Sufi's
  "The Saving Glut of the Rich" (July 2025 revision), CRS R48153 (2024), and CBO's 2014 report on capital-income
  tax rates, read on its publication page because cbo.gov refuses non-browser clients.

Pins are read with `git show`, so peers' uncommitted files are never used.

Skipped, with reasons:
- ENOE Q3–Q4: INEGI's server drops the larger files. Q1–Q2 suffice for a cross-check.
- IPUMS-International: not needed, because EMOVI transitions and ENIGH cells cover the Mexico side.
- The REStat 2019 CMP version: the working paper was read; the published tables are unverified. FHL's JPE text
  was read in its author manuscript; the journal's typeset tables were not seen.
- Browning (1987), Ballard–Shoven–Whalley (1985) and Heckman–LaLonde–Smith (1999): not reached (mcpf_sources.md).
- SAT's aggregate wage withholding: the statute is validated against OECD's published rates instead.
- CEFP's analyses of SHCP's incidence studies: CEFP's server (cefp.gob.mx) refused the connection. SHCP's own
  study was reached instead and is used (Tax basis).
- Mexico's crime counterpart: left as an unknown.
- Import duties and ISAN in Mexico's consumption burden: left out, with their size noted (Tax basis).
- The Senate's IBD note on the fuel excise: its server returned a bot-check page instead of the PDF. SHCP's own
  December report gives the figure.
- The real-costs totals (73cc30c): not needed. The ledger reads each case's own account through the winners pin.

## The sept27 run

1. **Pins.** `pins.json` holds all four for sept27, sent by the parent on 2026-09-28: model
   `adopted_2026_09_27`, winners 62f1e5a (round 2), distribution 78766c2, generation 8654a0c. Every input is read
   with `git show` at its pin. The generation lines at 8654a0c reproduce `generation_results.csv`, corrected and
   uncorrected, to 1e-6. [CALCULATION: generation_lines.cjs --case sept27; split_residual.py --case sept27]
2. **Line classes, fixed before any sept27 number was seen.** A line without a class stops the run with
   `[BLOCKED]`. The rules for the Sept 27 additions (from `main_case_long_run_2026_09_27/RESULT.md`):
   - long-run road and park responses change existing lines (`economic_affairs_services`, `recreation_culture`):
     public_good, average cost, so the group's V is unchanged and the cost to others rises;
   - rental assistance at response 1 is `housing_subsidies`: housing_voucher, 0.83 / 1 / 1;
   - the capital return on a general-government function takes that function's class: public goods at average
     cost (their average cost includes the capital), schools at 0, hospitals and health at cost, justice by the
     protection split;
   - enterprise surplus is a receipt the group pays: $1 per $1;
   - enterprise capital return (water, transit, utilities) is a service at cost (V/G 1); the public-housing part is
     housing_voucher.

   By component of the main case's `meta.capital_return` (main_case_long_run_2026_09_27, f3031ab):
   - education, V = 0: `k12`, `college`;
   - justice, protection split: `pos_sl`, `pos_fed`;
   - health services at cost: `health_sl`, `health_fed`;
   - public goods at average cost: `gps_sl`, `gps_fed`, `hwy_sl`, `hwy_fed`, `air_fed`, `rec_sl`, `rec_fed`;
   - housing_voucher: `ent_housing_sl`;
   - services at cost: `ent_transit_sl`, `ent_airports_sl`, `ent_ports_sl`, `ent_power_sl`, `ent_water_sl`,
     `ent_sewer_sl`, `ent_tolls_sl`, `ent_power_fed`, `ent_other_sl`, `ent_other_fed`.

   Capped programs (rental assistance and LIHEAP, $5.09bn in the distribution lane at 78766c2) are paid for by
   the eligible households that go without them (judgment call 23):
   - other residents get a `displaced_beneficiaries` row, weighted by the distribution lane's incidence on those
     households;
   - λ does not apply to it, because no tax is raised;
   - the taxpayers' row (`fiscal_others`) leaves it out: a gate requires the winners fiscal channel to equal
     A − D + F;
   - the group's side is unchanged: `housing_subsidies` stays housing_voucher (0.83 / 1 / 1) and
     `energy_assistance` cash (1).

   **Outcome.** Every sept27 line took a class; none stopped the run. The winners lane carries the capital return
   as 24 `capital_<id>` lines per band end, one per component above, and no total line, so nothing had to be
   split. The valued lines equal the winners lane's A at each end, and the fiscal channel equals A − D + F
   (gates). The `displaced_beneficiaries` row is −$5.09bn. The parent reports that a peer's independent probe on
   the same pinned files agrees: the classifier accepts every line, and the A − D + F gate holds.
   [CALCULATION: valuation.py, world_ledger.py]
3. **Builds.** `run_all.sh sept26_schools sept27`, run twice, exits 0, and the two builds are byte-identical
   across all 32 derived files (2026-09-28, after the last change). The repo's checker runs the same steps one
   script at a time; `run_all.sh` only wraps them, so it is acknowledged rather than run:

   ```sh
   L=infra/immigration-fiscal/world_ledger_2026_09_27
   uv run --no-project python3 scripts/rerun_lane.py $L \
     "uv run --no-project python3 {lane}/acquire.py" \
     "uv run --no-project python3 {lane}/mexico.py" \
     "uv run --no-project python3 {lane}/g2_premium.py" \
     "uv run --no-project python3 {lane}/weights.py" \
     "node {lane}/generation_lines.cjs --case sept26_schools" \
     "uv run --no-project python3 {lane}/split_residual.py --case sept26_schools" \
     "node {lane}/generation_lines.cjs --case sept27" \
     "uv run --no-project python3 {lane}/split_residual.py --case sept27" \
     "uv run --no-project python3 {lane}/valuation.py" \
     "uv run --no-project python3 {lane}/world_ledger.py --case sept26_schools" \
     "uv run --no-project python3 {lane}/world_ledger.py --case sept27" \
     --allow-unrun $L/run_all.sh
   ```

   It reports IDENTICAL, 57 of 57 files unchanged, exit 0: the 32 derived files and every other file a commit of
   the lane would carry (2026-09-28). `acquire.py` downloads nothing when `_cache/` is complete; it rewrites the
   source manifest from the files there. [CALCULATION: scripts/rerun_lane.py]
4. The tables, claims and verdict above are on both cases, with sept27 first.

## Log of confirmed case-independent pieces

### Mexico side data (mexico.py)

- ENIGH 2024 person-level labor income: the 36 labor claves reproduce the concentrado's monetary labor income
  (ingtrab less remuneration in kind) to 1e-6; MXN 7,726.5bn a year over 101.2m persons aged 15+.
  [DATA: ENIGH 2024; CALCULATION: mexico.py gate `enigh_labor_claves_reproduce_concentrado`]
- ENIGH records take-home pay. The 2024 questionnaire asks "¿Cuánto dinero recibió por ...?" and tells the
  interviewer to add back only voluntary deductions: "Si le están descontando algún préstamo recibido, pagos que
  hace porque la empresa le prestó dinero para comprar su casa, pago que realiza si adquirió un seguro voluntario,
  por favor incluya ese monto en su ingreso." Income tax and social-security withholding are therefore not added
  back: Mexican earnings here are net of them, while CPS earnings are gross. [SOURCE: ENIGH 2024 Cuestionario
  para personas de 12 o más años, Apartado 2.2, `_cache/reads/enigh2024_cuest_personas_mayores.pdf`]
- ENIGH exceeds ENOE on earnings per employed person, more so with schooling (0.93× with no schooling, 1.67× with
  profesional); ENOE's income nonresponse rises from 7% to 22% over the same range. ENIGH is the central source.
  [CALCULATION: derived/mexico_enoe_check.csv]
- 2024 PPP: GDP 9.9166 and private consumption 10.8013 pesos per international dollar; market rate 18.30.
  [DATA: WDI PA.NUS.PPP, PA.NUS.PRVT.PP, PA.NUS.FCRF]
- A bug found and fixed before any use: the schooling map sent unknown years (-1) to "none"; unknown now stays
  unknown. EMOVI respondents with both schooling fields known fell from a spurious 100% to 93.2% (weighted 94.6%).
- 2026-09-28: gross-up to gross pay. Formal jobs (subordinate, with SAR or AFORE) are grossed up by the 2024
  statutory withholding: OECD's schedule, the pre-May credit and the 1 May 2024 decree's credit, employee IMSS
  contributions, the 1.125% retirement deposit, and the minimum-wage exemption.
  - The model reproduces OECD Taxing Wages 2025 Table 1.3 at the average wage: income tax 10.83% against 10.8%,
    contributions 1.41% against 1.4% (gate).
  - ENIGH's formal workers number 18.9m, 15.5% of them at or below the exemption.
  - Gross labor income is MXN 8,410.6bn against 7,726.5bn received. Withheld tax is MXN 639.6bn and retirement
    deposits MXN 44.5bn.
  - Gross over take-home runs from 1.007 (no schooling) to 1.047 (secundaria) and 1.151 (profesional).
  - Take-home columns are unchanged (regression check: every shared column identical).

  [SOURCE: reads/oecd_taxing_wages_2025_mexico.md; CALCULATION: mexico.py gates
  `withholding_reproduces_oecd_table_1_3`, `gross_up_closes`]
- 2026-09-28: Mexican consumption taxes. The group's US row subtracts its US sales, excise, customs and
  motor-vehicle taxes, but the withheld bound carried no IVA or IEPS, so those stayed in the group's
  counterfactual income. A new central Mexican-tax scenario adds them at 8.72% of take-home pay (WDI 2024; see
  Tax basis), and the tables now use it.
  - The withheld and proportional scenarios are unchanged: their rows match the previous build exactly.
  - Two rebuilds are byte-identical.

  [CALCULATION: world_ledger.py `mexico_consumption_tax_rate`; gates `wdi_*_mexico_2024`,
  `mexico_consumption_tax_rate_plausible`]
  - Stale: the rate was replaced by SHCP's measured incidence the same day, and its "upper-side proxy" label was
    wrong (the SHCP consumption-tax entry below).
- 2026-09-28: sept27 wiring on the distribution (78766c2) and generation (8654a0c) pins, ahead of the winners pin.
  - Displaced beneficiaries of the capped programs get their own row, and the fiscal gate becomes A − D + F. A
    smoke test (sept26_schools with the sept27 distribution file and a synthetic carved-out channel) gives:
    - the taxpayers' row falls by the displaced $5.09bn, and the equal-weight totals are unchanged;
    - the row's weights are g 1.12 and log 5.14.
  - New gates:
    - the valued lines equal the winners lane's A at each end, to $0.001bn (it holds for sept26_schools);
    - the log-weight bins match the pinned channel bins, to 1e-5 relative (they match at both distribution pins).
  - Capital-return lines take their pre-registered component classes.
  - `derived/generation_split_check.csv` is new (judgment call 18).
  - Superseded by the next entry: this build still split the group's flows by class keys.
  - The case files are now written so that a first build and a rebuild agree byte for byte. The sept26_schools
    outputs are unchanged, with two exceptions:
    - `world_ledger_rows.csv` has the same text, but its `basis` column now sits after `kind`, where the code puts
      it; the old order was left over from appending the column to an existing file;
    - `valuation_meta.json` lists only the pins of cases it valued.

  [CALCULATION: world_ledger.py, valuation.py]
- 2026-09-28: the generation rows are the generation lane's split (judgment call 18). The parent asked that the
  world ledger publish no second split of the same case.
  - `generation_lines.cjs` evaluates the lane's corrected and uncorrected models at the band ends (specs 48 and
    11). Both reproduce `generation_results.csv` convention (a) to 1e-6.
  - `valuation.py` values the lines by class. `world_ledger.py` gates the valued rows back to the lane's costs,
    and each outer span takes the three generations at one end.
  - `split_residual.py` locates the earlier gap in the correction edits (judgment call 18).
  - Changed outputs:
    - `world_ledger.csv` and `world_ledger_rows.csv` (the generation rows, and the Hendren and log totals);
    - `generation_split_check.csv`, which now shows the reconciliation, with a difference of 0.000000;
    - four new derived files: the corrected and uncorrected lines, `valuation_by_generation.csv` and the residual.
  - Totals at equal and λ weights, and the break-even w, are unchanged.

  [CALCULATION: generation_lines.cjs, split_residual.py, valuation.py, world_ledger.py]
- 2026-09-28: the central's consumption taxes come from SHCP's measured incidence. SHCP's 2026 report to Congress
  (results for 2024, on ENIGH 2024) gives IVA and IEPS as a share of autonomous income by household decile. Each
  ENIGH worker's gross pay now bears their household decile's rate.
  - Deciles are rebuilt as SHCP defines them: 10% of households each, by monetary current income per head (gate).
  - The group's comparators pay 9.3% of gross pay, 10.1% of take-home pay. The WDI average rate on take-home pay
    gave 14% less, so the earlier label "upper-side proxy" was wrong. The WDI figure is kept in the meta as a check.
  - The central's Mexican taxes rise, $bn: G1 17.7 → 19.2, G2 13.1 → 14.2, G3+ 13.0–53.2 → 14.1–57.6.
  - The world break-even w at equal weights moves 0.34 → 0.35; the US-only one 0.55 → 0.54.
  - The equal-weight world total, and the withheld and proportional scenarios, are unchanged. The shared columns of
    the Mexico and premium files are identical to the previous build.

  [SOURCE: reads/shcp_2026_incidence.md; CALCULATION: mexico.py `household_deciles`, gates
  `enigh_current_income_adds_up`, `household_deciles_hold_a_tenth_each`, `every_person_has_a_household_decile`]
  - Stale: the fuel excise was added the same day (entry below); the central is now 11.6% of gross pay, and its
    figures are in the Tax basis section.
- 2026-09-28: the Medicaid class takes the published FHL figures (JPE 2019, read in its PMC author manuscript):
  willingness to pay if the uninsured had no implicit insurance, 0.76 / 0.92 / 1.08 per dollar of G, replacing the
  working paper's bridge, 0.8 / 0.9 / 1.0 (judgment call 3). `valuation.py` now writes the ratios to
  `valuation_meta.json`, and `world_ledger.py` reads them there for unreimbursed care received and Mexico's public
  health, instead of keeping a second copy.
  - The group's valued US budget position rises $2.4bn central, to +$187.7–198.6bn. Medicaid's shortfall below
    cost falls from $11.8bn to $9.4bn at the low end.
  - The group's equal-weight total moves +$1.9bn in the central, −$7.0bn in the low outer span and +$11.1bn in the
    high outer span. Other residents', future taxpayers' and Mexico's rows are unchanged under every weighting.
  - Break-even w moves by 0.002 at most in the central and by 0.031 at most anywhere (response-only, withheld, low
    outer, λ 1.5: 1.54 → 1.57).
  - Only the valuation and world-ledger files change. Two builds, the first from an empty `derived/`, are
    byte-identical.

  [SOURCE: reads/finkelstein_hendren_luttmer_2019.md quotes 10–14; CALCULATION: valuation.py, world_ledger.py;
  builds compared cell by cell]
- 2026-09-28: claim 2's productive-use reading is bounded (judgment call 21). `world_ledger.py` `saving_leak`
  weights Mian, Straub and Sufi's saving rates by wealth group with the payers' shares of the cost. It takes τ
  from CRS and CBO and m from OMB and the main case, and writes the result to the case meta: the payers' saving
  rate, the leak per dollar and in dollars, and the US-only break-even w it implies.
  - sept26_schools, central, equal weights: payers' saving rate 0.22 (tax shares) and 0.07 (per-person cuts);
    leak $5.6–61.4bn and $1.8–19.9bn on $275.0bn of tax financing; break-even w 0.54 → 0.55–0.64.
  - Only `world_ledger_meta_sept26_schools.json` changes; the tables do not.
  - Stale on w: after the fuel excise, the schools case's break-even w runs 0.53 → 0.54–0.63 (claim 2).

  [SOURCE: reads/mian_straub_sufi_2025.md, reads/capital_tax_wedge.md; CALCULATION: world_ledger.py
  `saving_leak`, gates `saving_rates_cover_payers_*`, `payers_all_lose_*`, `saving_leak_central_totals`]
- 2026-09-28: a defect in the short-run sensitivity, fixed. `short_run_block` scaled the owners' loss linearly
  (6.4% of GDP × k) but the net loss with the square of the shock, so its three figures did not add up: the gain
  of $282bn and the loss of $306bn left −$24bn against the reported −$34bn. The owners now lose the stayers' gain
  plus the triangle, $315bn (G1 and G2) and $460bn (with G3+), and a gate checks Mishra's own figures add up
  (5.9% + 0.5% = 6.4%). Only `world_ledger_meta_sept26_schools.json` changes; the block is never in the tables.
  [CALCULATION: world_ledger.py `short_run_block`, `MISHRA`]
- 2026-09-28: each generation's own break-even w, against the net fiscal cost the generation lane assigns it
  (section D, "Each generation alone"). `world_ledger.py` `generation_breakeven` writes it to the case meta with
  other residents' non-fiscal total beside it. On sept26_schools: G1 0.27, G2 0.39, G3+ 0.34 (upper premium) to
  1.32 (zero premium). Only the case meta changes. Stale: after the fuel excise the schools case gives G1 0.26,
  G2 0.39 and G3+ 0.34–1.20; sept27 is in section D.
  [CALCULATION: world_ledger.py `generation_breakeven`, gates `generation_cost_at_two_ends_*`,
  `generation_row_positive_*`]
- 2026-09-28: the fuel excise joins the central's consumption taxes (Tax basis; judgment call 9). SHCP's incidence
  covers the IEPS other than on gasoline and diesel, so the central had left out MXN 403.6bn, about 2.3% of
  income. `mexico.py` `fuel_ieps_by_decile` spreads it by SHCP's fuel-spending shares (Tabla 2.9) over the decile
  incomes that SHCP's IVA shares and rates imply (Tabla 2.8); a gate checks that those incomes reproduce the 8.0%
  average. Old → new, on the schools case (sept27 was first built with the excise in):
  - consumption taxes on the comparators' gross pay: 9.3% → 11.6%;
  - central Mexican taxes, $bn: G1 19.2 → 21.9 (consumption 10.8 → 13.4), G2 14.2 → 16.2 (7.9 → 9.8), G3+
    14.1–57.6 → 16.0–65.4;
  - the rows at equal weights, central: G1 +251.6 → +254.3, G2 +283.7 → +285.6, G3+ +73.0 → +80.8, Mexico's
    residents +115.0 → +102.7;
  - break-even w, world: 0.348 → 0.361 (equal), 0.407 → 0.422 (λ 1.16), 0.531 → 0.551 (λ 1.5);
  - break-even w, US only: 0.537 → 0.527 (equal), 0.610 → 0.597 (λ 1.16), 0.763 → 0.748 (λ 1.5);
  - the equal-weight world total and the withheld and proportional scenarios: unchanged (largest difference 0).

  Import duties (0.8 points if spread like IVA) and ISAN stay out. [SOURCE: reads/shcp_2026_incidence.md quotes
  9–11; CALCULATION: mexico.py gates `shcp_decile_shares_add_to_100`,
  `shcp_iva_shares_and_rates_imply_its_average`; builds compared cell by cell]
- 2026-09-28: the sept27 run ("The sept27 run"). All four pins set; every line classified by the rules fixed in
  advance; 24 capital-return lines per band end ($37.3bn at the low end, $56.5bn at the high end), each in its
  component's class; `displaced_beneficiaries` −$5.09bn. Section D and the claims now lead with sept27, and the
  schools case is beside it. [CALCULATION: derived/valuation.csv, derived/world_ledger.csv]
- 2026-09-28: labels only. The central's row labels and the case meta's `mexico_consumption_tax.source` now name
  the fuel excise. `world_ledger_rows.csv` and both case metas change in text; no number moves. Two builds are
  byte-identical, and the checker reports 57 of 57 files identical. [CALCULATION: world_ledger.py]
