# Cumulative fiscal cost 2005–2024: what is measured and a back-cast

Date: 2026-09-20. [MODEL / FRAMING-SENSITIVE] Calculation record; narrative authorship remains operator-owned.

**Result:** No historical cost is measured here. The account exists for income-year
2024 only. Combining measured national budgets and measured Mexican-origin population
for each year with the group's **2024 relative position** gives, for the main
CBO-informed net cost to other residents ($165–197bn in 2024), about **$1.4–2.0tn
over 2015–2024, $2.0–3.1tn over 2010–2024 and $2.4–3.8tn over 2005–2024**, in 2024
dollars without interest. The ranges span three back-casting rules and the low/high
2024 anchor; they are not confidence intervals.

## What is measured and what is assumed

[SOURCE: [lane README, pins and commands](../infra/immigration-fiscal/historical_backcast_2026_09_20/README.md)]

Measured for every year: government current receipts and expenditures (BEA Table 3.1),
the GDP deflator, resident population, and the ACS Mexican-origin count, 26.8m in
2005 rising to 39.0m in 2024. Measured for 2008–2024: the group's per-capita income
relative to the nation, **0.519 in 2008, 0.509 in 2013, 0.563 in 2019 and 0.611 in
2024**, and its median age, 25.7 to 29.8 against 36.9 to 39.2. Assumed: everything
about the group's own taxes and spending before 2024.

## Cumulative totals, $tn in 2024 dollars

| 2024 concept | Rule | 2015–2024 | 2010–2024 | 2005–2024 |
|---|---|---:|---:|---:|
| Net cost, CBO-informed services ($165–197bn) | flat | 1.57–1.88 | 2.30–2.74 | 2.92–3.49 |
| | ratio | 1.41–1.69 | 2.04–2.44 | 2.41–2.91 |
| | income | 1.74–2.02 | 2.69–3.09 | 3.32–3.81 |
| Net cost, full proportional services ($270–289bn) | flat | 2.57–2.75 | 3.75–4.01 | 4.77–5.10 |
| | ratio | 2.34–2.51 | 3.35–3.58 | 4.02–4.31 |
| | income | 2.67–2.84 | 3.99–4.23 | 4.93–5.22 |
| Gap against the average resident ($274bn, shared) | flat | 2.61 | 3.81 | 4.85 |
| | ratio | 2.48 | 3.44 | 4.30 |
| | income | 2.81 | 4.09 | 5.21 |

[DERIVATION: `derived/backcast_windows.csv`; annual rows in `derived/backcast_annual.csv`.]

`flat` holds the 2024 per-person cost constant in real terms. `ratio` holds the
group's receipts at 0.566 of national receipts per capita and its charged spending at
the 2024 ratio to national spending per capita. `income` also scales the receipts
ratio by the measured relative income. Under `ratio` and `income` the net-cost
concepts follow the national deficit. The main case under `income` is $91–107bn in
2005, $221–244bn in 2010, $149–173bn in 2015 and $293–326bn in 2020; under `ratio`
it is $45–61bn, $162–185bn, $85–109bn and $264–297bn. The gap against the average
resident cancels a deficit everyone shares and stays between $150bn (2009, `ratio`)
and $313bn (2022, `income`).

## Reading

[INFERENCE] The measured income series is the one piece of disconfirming evidence
available for the constant-position assumption, and it cuts against it: the group
was relatively poorer before 2015, so constant 2024 receipts ratios understate past
costs. That is why `income` exceeds `ratio` by 13–37%, most in the main case over
twenty years. The spending side could move
either way: more pupils and fewer retirees per head, no Medicaid expansion before
2014, and pandemic business support that did not follow population.

Every conditional assumption behind the 2024 anchors carries over: the response
cases, fully adjusted private capital owned by other residents, defense, general
government and existing interest held fixed, production gains of $8.8–13.3bn, and
crime, housing, innovation and institutions unpriced. See the
[complete annual account](immigration-complete-annual-account-2026-09-20.md).
These are resident-stock accounts, not the effect of an admission policy, and the
comparison population includes other immigrants.

## What would make it measured

Rebuild the base account on each CPS ASEC public file, 2005–2025: Census-modelled
taxes and credits, reported transfers with year-specific administrative ratios,
coverage-based medical transport and public pupils. Files before 2019 are
fixed-width with changing variable names, and the 2014 and 2019 redesigns break
income series. The repository holds 2022–2026 only.

[INSTRUMENT] LLM-assisted modelling on a politically charged topic; the measured
series and each assumption are separately inspectable.
