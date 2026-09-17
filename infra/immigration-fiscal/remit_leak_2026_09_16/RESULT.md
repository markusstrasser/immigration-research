# Remittance leakage in the generation ledger

**Correction, 2026-09-17 — supersedes the ceiling and causal-loss claims below:** the $3.7bn US-born / 0.9%-of-G2-earnings bound is circular. CEMLA's 16.7% divides all US-to-Mexico remittances by first-generation earnings; treating that quotient as the actual first-generation sending rate assumes its unknown share. No independent first-generation lower bound is established. The per-adult tax changes remain model scenarios, not measured losses or empirically bounded generation rates; higher-rate arms are not ruled out by the asserted ceiling. National tax scenarios are $1.277–2.299bn with Mexico-born geographic weights, not an established $3–4bn loss. BEA's historical $69.94bn personal-transfer series covers foreign-born senders, with US-born transfers in another category. See the [source and algebra audit](../../../research/immigration-aggregate-and-generation-audit-2026-09-17.md) and [decision](../../../decisions/2026-09-17-separate-benchmark-gaps-and-lineage-claims.md). Original claims remain below for provenance.

**Verdict:** Remittance leakage is real, well sourced at the first generation, and fiscally
trivial in this ledger. Cutting each cell's imputed domestic consumption base by its modelled
remittance outflow moves the Mexico-born extended balance by **−$95 to −$188 per adult per year**
(0.8% to 1.6% of that cell's −11,522 gap) and the Mexican-second-generation balance by **−$19 to
−$93** (0.2% to 1.1% of −8,286). Nothing changes sign, no arm moves a gap by one standard error.

The substantive finding is not the ledger delta. It is that **CEMLA's 16.7% is an accounting
quotient, not a measured propensity**, and this lane's own aggregate check turns it into a binding
constraint on the second generation. CPS ASEC 2025 puts the Mexico-born wage-and-salary bill at
$352.0bn against CEMLA's $373.7bn (94%), so 16.7% of the CPS bill is $58.8bn against Banxico's
$62.5bn actually received from the US. That leaves **at most $3.7bn of headroom for every US-born
sender in the country**. A second-generation rate of 1.6% of wage income already overshoots Banxico
by $2.9bn. The balance of payments therefore caps the Mexican-second-generation remittance rate at
roughly **0.9% of wage income**, and the 2.5% and 5.2% arms below are ruled out by that ceiling,
not by any survey.

Model self-report: claude-opus-5[1m] (environment block: "Opus 5 (1M context)").

`[UNVERIFIED]` — every second-generation rate in this file is bounded, not measured. No survey
publishes a Mexican-origin second-generation remittance rate.

## Validation, run and pasted

```
-- VALIDATION (a): baseline sales/excise line, third_plus_nh_white --
0.35 taxable-share arm: 1,049.7  (gen-ledger lane published 1,050)  deviation -0.3
ITEP arm:               1,812.5  (gen-ledger lane published 1,812)  deviation +0.5
[validation a] PASS (both within $5)
```

Validation (b): Banxico, *Ingresos y Egresos por Remesas, diciembre de 2024* (4 February 2025),
verbatim: "Para 2024 en su conjunto, el valor de los ingresos por remesas fue de **64,745 millones
de dólares**, monto mayor al de 63,319 millones de dólares reportado en 2023 y que significó un
incremento anual de 2.3%." Also verified in the same release: 99.1% by electronic transfer
($64,136mn), cash and in kind 0.7% ($481mn), money orders 0.2% ($128mn), outbound remittances from
Mexico $1,308mn, net surplus $63,437mn. **PASS.**
[SOURCE: https://www.banxico.org.mx/publicaciones-y-prensa/remesas/%7BD08E80AC-6031-C7CF-D792-28CBEF70658F%7D.pdf]

## 1. Remittance rate by nativity and generation

### The CEMLA note, verified, and what its wage bill actually is

CEMLA *Notas de Remesas* 2025-3, "Los trabajadores mexicanos inmigrantes en Estados Unidos enviaron
en 2024 el 16.7 por ciento de su ingreso laboral a sus familiares en México", by Jesús A. Cervantes
González and Juan Antonio Ortega, February 2025. Wage-bill construction, verbatim:

> "La nota se elaboró combinando cifras del Banco de México sobre remesas enviadas a México desde
> Estados Unidos con extracciones de la base de datos de la **Current Population Survey (CPS)**, que
> es una encuesta mensual en hogares que recaba la Oficina de Censos en Estados Unidos."

and the residual, stated explicitly by CEMLA:

> "Lo anterior significa que 311,197 millones de dólares de la referida masa salarial tuvieron como
> destino los mismos Estados Unidos, es decir, los trabajadores mexicanos inmigrantes dedicaron el
> **83.3% de su ingreso laboral a erogaciones locales** en manutención, salud, pago de impuestos, de
> seguridad social y cubrir pasivos, incluyendo el pago de hipotecas, y posiblemente una parte
> también se ahorró."

| Year | Remittances from US ($mn) | Mexican-immigrant US wage bill ($mn) | Share remitted |
|---|---|---|---|
| 2015 | 24,260 | 226,843 | 10.7% |
| 2020 | 39,934 | 256,875 | 15.5% |
| 2021 | 49,983 | 282,818 | 17.7% |
| 2022 | 56,367 | 319,940 | 17.6% |
| 2023 | 60,925 | 340,903 | 17.9% |
| 2024 | 62,529 | 373,726 | **16.7%** |

[SOURCE: CEMLA *Notas de Remesas* 2025-3, Gráfica 2, https://www.cemla.org/foroderemesas/notas/2025-03-notas-de-remesas.pdf]

**The construction is a quotient, not a behaviour.** The numerator is every dollar Banxico records
arriving from the US; the denominator is only the CPS wage bill of Mexican *immigrants*. Any dollar
sent by a US-born Mexican-American, by a non-Mexican sender, or out of non-wage income is loaded onto
the immigrant rate. 16.7% is therefore an **upper bound on the first-generation rate**, and the
second-generation rate and the first-generation rate cannot both be large. This is the single most
important thing the lane found and it is not stated in the CEMLA note or in memo §14.

State dispersion in the same table is wide and is a reminder that the rate is a composition
statistic: Colorado 30.1%, NY+NJ 27.0%, California 17.1%, Texas 12.7%, Arizona 7.4%. CEMLA's own
determinants list (Nota 3, 2023) has it falling with citizenship share, with mortgage-paying share,
and with pre-2000 arrival share.

### Participation and amounts

| Population | Share sending remittances | Source |
|---|---|---|
| Latino immigrants, 2006 | 51% | Pew Hispanic, 2006 National Survey of Latinos |
| Latino immigrants, 2009 | 54% | Pew Hispanic, 2008/09 survey |
| All Latino adults, 2006 / 2009 | 35% / 36% | same |
| Latino immigrants, ≤10 yrs in US | 63% | Pew 2006 NSL |
| Latino immigrants, 20–29 yrs in US | 48% | Pew 2006 NSL |
| Latino immigrants, 30+ yrs in US | 33% | Pew 2006 NSL |
| Asian immigrants, 2022–23 | 32% | Pew 2022-23 Survey of Asian Americans |
| **US-born second-generation Asian adults** | **15%** | same |
| Third-or-higher-generation Asian adults | 4% | same |

[SOURCE: https://www.pewresearch.org/race-and-ethnicity/2007/10/25/iv-remittances-property-ownership-and-civic-activity/,
https://www.pewresearch.org/hispanic/2013/11/14/2-remittance-trends/,
https://www.pewresearch.org/race-and-ethnicity/2024/05/02/asian-americans-who-send-remittances-to-their-ancestral-homelands/]

**No published Hispanic second-generation rate exists.** I searched Pew's Hispanic Trends reports
(2003, 2007, 2009, 2013), the 2006 Latino National Survey literature, and the remittance economics
literature; every Hispanic-specific cut is by years-in-US or country of origin, never by generation.
The Asian-American 2024 report is the only US survey that publishes the generational gradient at all.

### Bounding the second generation

Two independent routes, both [INFERENCE]:

1. **Back out the native-born participation rate from Pew's two published Latino figures.** 51% of
   foreign-born and 35% of all Latino adults sent in 2006; with the foreign-born at roughly 53% of
   Latino adults that year, the native-born rate solves to about **17%**. Repeating on the 2009
   pair (54% / 36%) gives about **15%**. Both land on Pew's measured Asian second-generation 15%.
   Participation ratio second-to-first ≈ 0.31 (Hispanic, derived) to 0.47 (Asian, published).
2. **Scale for amount and for income.** Amount per sender for the US-born is unmeasured; assume
   0.3–1.0 of the immigrant amount. Second-generation wage income is higher, which lowers the rate
   again for a given dollar amount. That puts the second-generation rate at **1.6% to 5.2%** of wage
   income before any aggregate constraint.
3. **The balance-of-payments ceiling, which binds tighter than either.** See the Verdict: at most
   $3.7bn of the $62.5bn is left for US-born senders once the Mexico-born send 16.7% of the CPS wage
   bill, so the Banxico-consistent second-generation rate is about **0.9%**.

Arms carried through the ledger: `r2_zero` 0.0%, `r2_low` 1.6%, `r2_central` 2.5%, `r2_high` 5.2%.
The Mexican third-plus self-ID cell gets 0.267 × the second-generation rate (Pew Asian 4%/15%).
The 0.9% Banxico-consistent value is between `r2_zero` and `r2_low`; the deltas are linear in the
rate, so interpolate.

## 2. Applying the haircut to the ledger

Person-level remittance = rate(person) × wage-and-salary income (`WSAL_VAL`, floored at zero), summed
into the SPM resource unit, subtracted from that unit's imputed consumption base
(0.90 × `SPM_RESOURCES`), floored at zero. The 0.25/0.35/0.45 taxable-share arms then apply the state
combined rate to the reduced base; the ITEP arm is scaled by the same reduced-to-original base ratio.
Rates are applied only to Mexico-origin persons, so the `all_native` and `all_second_gen` cells are
haircut only through their Mexican-origin members and are understated by construction.

Modelled remittance outflow, $ per adult 25–64 per year, `r2_central`, equal-all-members allocation
(which spreads a unit's outflow across every member, so a white-native adult sharing an SPM unit with
a Mexico-born earner carries a small share):

| Group | Remittance per adult | se |
|---|---|---|
| third_plus_nh_white | 17 | 2 |
| all_native | 84 | 3 |
| all_second_gen | 454 | 19 |
| mexican_second_gen | 1,290 | 44 |
| mexican_third_plus_selfid | 312 | 20 |
| **mexico_born** | **3,457** | 96 |

Change in the extended balance, $ per adult per year (only the sales/excise line moves):

| Arm | Group | Extended base | With haircut | Δ balance | Δ gap vs 3rd+ NH white |
|---|---|---|---|---|---|
| r2_zero / 0.35 | mexico_born | 4,462 | 4,367 | −95 | −95 |
| r2_zero / ITEP | mexico_born | 4,953 | 4,774 | −179 | −179 |
| r2_high / 0.35 | mexico_born | 4,462 | 4,361 | −101 | −101 |
| r2_high / ITEP | mexico_born | 4,953 | 4,765 | −188 | −187 |
| r2_zero / 0.35 | mexican_second_gen | 7,698 | 7,679 | −19 | −19 |
| r2_low / 0.35 | mexican_second_gen | 7,698 | 7,667 | −31 | −31 |
| r2_central / 0.35 | mexican_second_gen | 7,698 | 7,660 | −38 | −37 |
| r2_high / 0.35 | mexican_second_gen | 7,698 | 7,641 | −58 | −57 |
| r2_zero / ITEP | mexican_second_gen | 8,201 | 8,171 | −30 | −30 |
| r2_high / ITEP | mexican_second_gen | 8,201 | 8,107 | −93 | −93 |

At the Banxico-consistent 0.9% second-generation rate the Mexican-second-generation gap moves from
−8,286 to about **−8,304** on the 0.35 arm and from −8,546 to about **−8,563** on the ITEP arm.
The Mexico-born gap moves from −11,522 to −11,618 (0.35) and −11,794 to −11,972 (ITEP).

Every delta is far inside the sampling standard errors already carried on those gaps (443 and 402),
and all deltas run the same direction: remittances widen every gap, because the reference group
remits nothing. Full grid for all four arms × four taxable-share arms × six groups is in
`remit_leak_by_group.csv` and `remit_extended_balance.csv`; the printed run is `remit_result.txt`.

**Status split not run.** `status_impute_2026_09_16/status_ledger.py` rebuilds the whole ledger with
its own group construction and would need a second full CPS pass; given that the whole remittance
effect on the pooled Mexico-born cell is under $190, splitting it by imputed status cannot produce a
number worth the run. Not done, deliberately, and the omission is the lane's, not a failure.

### National forgone state and local sales tax

Remittances from the US to Mexico in 2024 ($62,529mn) × the population-weighted combined state and
local sales tax rate × the taxable share. Rates computed on the CPS ASEC 2025 person file from the
Tax Foundation 1 January 2024 combined-rate table staged by the gen-ledger lane.

| Weighting | Combined rate | Taxable share 0.25 | 0.35 | 0.45 |
|---|---|---|---|---|
| All US persons | 7.48% | $1,169mn | $1,637mn | $2,105mn |
| Mexico-born population | 8.17% | $1,277mn | **$1,788mn** | $2,299mn |

So the remitted dollars cost US state and local governments roughly **$1.2bn to $2.3bn a year** in
sales tax, against combined state and local general sales tax collections in the hundreds of billions.
The Mexico-born weighting is the right one and is 9% higher than the national one, because the
Mexico-born live disproportionately in California (7.25% state, high local add-ons), Texas and
Arizona rather than in the zero-rate states.
[SOURCE: Tax Foundation, *State and Local Sales Tax Rates, 2024*, staged at
`../gen_ledger_extension_2026_09_16/taxfoundation_2024_state_sales_tax_rates.csv`]

### Aggregate reconciliation, which is also a model check

```
Mexico-born persons (all ages, weighted):            12.23 M
Mexico-born adults 25-64:                             9.45 M
CPS ASEC 2025 Mexico-born wage+salary bill:         $352.0 bn   (CEMLA/CPS: $373.7 bn, 94%)
  x 16.7%                                          = $58.8 bn   (Banxico US->Mexico 2024: $62.5 bn, 94%)
  arm r2_zero    total modelled US->Mexico          = $58.8 bn
  arm r2_low     (2nd gen 1.6%)                     = $65.4 bn   OVERSHOOTS Banxico by $2.9 bn
  arm r2_central (2nd gen 2.5%)                     = $69.1 bn   OVERSHOOTS by $6.6 bn
  arm r2_high    (2nd gen 5.2%)                     = $80.2 bn   OVERSHOOTS by $17.7 bn
```

The 6% shortfall against CEMLA's own CPS wage bill is expected: CEMLA extracts monthly CPS basic,
this lane uses annual ASEC `WSAL_VAL` and excludes self-employment income.

## 3. The return flow as US exports

US goods exports to Mexico in 2024 were **$334,492mn**; Mexico's total goods imports were about
**$625,310mn**, so the US supplied roughly **53.5%** of Mexico's imported goods.
[SOURCE: US Census Bureau, Trade in Goods with Mexico, https://www.census.gov/foreign-trade/balance/c2010.html;
INEGI 2024 annual trade release, total imports $625.31bn — secondary reporting, not read from INEGI directly]

That 53.5% is the wrong number to apply to a remittance dollar and I will not report it as the answer.
Two corrections run the same way:

- **Most of Mexico's goods imports are intermediate inputs to the export maquila sector**, not
  household consumption. Non-oil imports were $586.84bn of the $625.31bn, and the intermediate-goods
  share of Mexican imports runs around three quarters in INEGI's own split.
- **Remittance-receiving households are poorer and more rural than the Mexican average**, and their
  spending concentrates in food, housing, health and education, which are the least import-intensive
  categories. Airola (2007) finds remittance income in Mexico favours "goods that could be viewed as
  investments rather than consumption" — housing and health care — which cuts the same way; durables
  and construction materials are the one leg with meaningful import content. Woodruff & Zenteno
  (2007, *J. Dev. Econ.* 82(2) 509–528) find remittances fund roughly 20% of microenterprise capital
  in urban Mexico, which is investment, not import demand, and no study I found gives a marginal
  propensity to import for remittance-receiving households specifically.

So: **roughly 5% to 20% of a remitted dollar returns to the US as an export sale, central estimate
about 10%**, i.e. $3bn to $12bn of the $62.5bn. [INFERENCE — this is a range built from the aggregate
import share, the intermediate-goods correction and the consumption-basket correction, not a measured
elasticity; no study gives the number directly.] The corresponding US *fiscal* return is a further
fraction of that, since exports generate corporate and payroll tax, not sales tax, and are outside
this ledger entirely.

## 4. National-accounts statement

Remittances sent by US-resident workers are a **secondary-income debit in the US current account**
and do not reduce US GDP. GDP measures production on US soil, and the remitter's output and wage are
counted in full when earned; the transfer abroad is a redistribution of income already produced. What
it reduces is **gross national disposable income** and, through it, domestic consumption, which is
precisely the channel this lane models into the sales-tax base. BEA's International Transactions
Accounts carry the flow on Table 5, line 18, "Personal transfers", defined in BEA's own footnote as
"Personal transfers (sometimes called remittances) from U.S. resident immigrants to foreign
residents"; it sits inside private transfer payments within secondary income. The 2024 figure is
**$69,940mn** (preliminary), up from $65,917mn in 2023, within total secondary-income payments of
$408,581mn and a secondary-income balance of −$206,896mn.
[SOURCE: BEA, *U.S. International Transactions, 4th Quarter and Year 2024*, 20 March 2025, Table 5,
https://www.bea.gov/sites/default/files/2025-03/trans424.pdf]

**The reconciliation with Banxico does not work and that is worth saying.** BEA records $69.9bn of
personal transfers from US residents to *the entire world*; Banxico records $62.5bn arriving in
Mexico *from the US alone*. That would make Mexico 89% of all US personal transfers, which is not
credible against Mexico's roughly 23% share of the US foreign-born population. The two series are
built differently: Banxico counts every inbound money-transfer-operator and electronic transaction
crossing into Mexico regardless of who sent it or their residence status, while BEA builds personal
transfers from a modelled migrant-stock-times-propensity estimate anchored on survey data. Banxico's
number is the better-measured one for the Mexico corridor because it is a transaction census, not a
model; BEA's is the one that is internally consistent with the rest of the US accounts. Anyone
quoting both in the same paragraph should say which measurement they are using and not add them.

## Files

| File | What |
|---|---|
| `remit_leak.py` | The run. Imports `extend_ledger`, applies the haircut, writes the outputs. |
| `remit_result.txt` | Printed validation, remittance table, all arms, national forgone sales tax. |
| `remit_leak_by_group.csv` | arm × group × taxable-share arm: base sales line, haircut sales line, delta. |
| `remit_extended_balance.csv` | arm × sales arm × group: extended balance base, with haircut, delta, gap, delta gap. |
| `_cache/` | CEMLA note, Banxico December 2024 release, BEA trans424, extracted text (gitignored). |

## What this lane does not resolve

- No measured Mexican-origin second-generation remittance rate exists anywhere I could find. The
  0.9% Banxico-consistent ceiling is arithmetic on aggregates, not a survey estimate.
- CPS ASEC has no remittance field, so nothing here is observed at the person level; the whole line
  is a rate applied to wage income.
- Non-Mexican immigrants are not haircut, so `all_native` and `all_second_gen` understate leakage.
- Remittances out of non-wage income (self-employment, transfers, savings) are not modelled.
- The consumption base is `SPM_RESOURCES`, which the gen-ledger lane already flags as demonstrably
  low against ITEP's published effective rates; the haircut inherits that understatement.
