# Cumulative fiscal cost 2005–2024: what is measured and a back-cast

Date: 2026-09-20. [MODEL / FRAMING-SENSITIVE] Calculation record; narrative authorship remains operator-owned.

**Adopted main case (2026-09-23):** on the $203–250bn anchor the operator adopted on September 23,
the whole-budget rules give **$1.7–2.5tn over 2015–2024, $2.5–3.7tn over 2010–2024 and $3.0–4.6tn
over 2005–2024**. The programme-by-programme version has not been re-run on that anchor. The
figures below are on the September 20 anchor ($165–197bn) and stay as a record.
[CALCULATION: `backcast.py` → `derived/backcast_windows.csv`, concepts `*_adopted_*`]

**Result:** No historical cost is measured here. The account exists for income-year
2024 only. Combining measured national budgets and measured Mexican-origin population
for each year with the group's **2024 relative position** gives, for the main
CBO-informed net cost to other residents ($165–197bn in 2024), about **$1.3–2.2tn
over 2015–2024, $2.0–3.3tn over 2010–2024 and $2.4–3.9tn over 2005–2024**, in 2024
dollars without interest. The ranges span every back-casting rule below, including the
programme-by-programme version, and the low/high 2024 anchor; they are not confidence
intervals. The whole-budget rules alone give $1.4–2.0tn, $2.0–3.1tn and $2.4–3.8tn.

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

## Programme-by-programme version

[DERIVATION; added 2026-09-21] National spending on each benefit programme and
government function, and collections on each household receipt line, are measured
for every year in the same BEA cells the complete account cites. Each of the group's
2024 lines is carried back with its own national series; only the group's **relative
use of each programme** stays at its 2024 value. All four 2024 anchors reconstruct
the account to six digits.

| Main net-cost case, $tn | 2015–2024 | 2010–2024 | 2005–2024 |
|---|---:|---:|---:|
| Programme rule | 1.70–1.98 | 2.36–2.77 | 2.74–3.25 |
| Programme rule, income-adjusted receipts | 1.97–2.24 | 2.88–3.26 | 3.46–3.94 |
| Same two rules with 2020–2021 set to the 2019/2022 mean | 1.32–1.88 | 1.98–2.90 | 2.36–3.58 |

Full proportional services: 2.25–3.06, 3.33–4.44 and 4.06–5.43. [SOURCE:
`derived/backcast_categories_windows.csv`, `backcast_categories_annual.csv`.]

Real national spending per resident, 2024 = 1, for the group's largest lines
[SOURCE: `derived/national_programme_index.csv`]:

| Line (group's assigned 2024 $bn, shared) | 2005 | 2010 | 2015 | 2019 | 2021 |
|---|---:|---:|---:|---:|---:|
| Medicaid, CHIP, other medical (117) | 0.58 | 0.66 | 0.78 | 0.82 | 0.91 |
| Education (193) | 0.85 | 0.91 | 0.90 | 0.93 | 0.98 |
| Medicare (64) | 0.53 | 0.72 | 0.78 | 0.89 | 0.94 |
| Social Security (63) | 0.63 | 0.73 | 0.82 | 0.88 | 0.90 |
| Public order and safety (62) | 0.90 | 0.98 | 0.95 | 1.01 | 0.99 |
| Refundable tax credits (55) | 0.42 | 0.97 | 0.75 | 0.86 | 4.36 |
| SNAP (14) | 0.54 | 1.05 | 0.96 | 0.70 | 1.81 |

Benefits did change: Medicaid and Medicare were 42–47% smaller per resident in 2005,
and refundable credits quadrupled in 2021. Police, courts and prisons were flat, and
the account charges them per capita, so no group-specific policing cost exists in any
year. The pandemic years supply 35–38% of the ten-year programme-rule total, because
2020–2021 credits are attributed at the group's 2024 ratio (2.3 times other residents
per person, an EITC and child-credit pattern). Pandemic payments were close to uniform
per head and the first round excluded households filing without Social Security
numbers [TRAINING-DATA; not verified here], so that attribution is too high; the
third row removes it. The group's relative use of each programme in earlier years is
still unmeasured. CPS ASEC reports programme receipt by origin in every year.

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

## Measured trend in the group's relative position

[SOURCE: ACS 1-year Selected Population Profile S0201, self-identified Mexican group over the
total population; `inputs/acs_mexican_origin.csv`. Published means and medians; no standard
errors pulled, no nativity or generation split.]

| Ratio to the national figure | 2008 | 2013 | 2016 | 2019 | 2021 | 2022 | 2023 | 2024 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Per-capita income | 0.519 | 0.509 | 0.535 | 0.563 | 0.585 | 0.591 | 0.599 | 0.611 |
| Median household income | 0.781 | 0.782 | 0.809 | 0.851 | 0.873 | 0.889 | 0.905 | 0.907 |
| Median earnings, full-time year-round men | 0.641 | 0.640 | 0.641 | 0.735 | 0.703 | 0.734 | 0.756 | 0.754 |
| Median earnings, full-time year-round women | 0.713 | 0.699 | 0.701 | 0.733 | 0.742 | 0.764 | 0.781 | 0.760 |

Flat from 2008 to about 2016, rising since. Per-capita and household income gained about one
point a year from 2013 to 2023. In 2024 per-capita income kept that pace (+1.2 points) and
household income did not (+0.2). The median-age gap to the nation narrowed from 11.2 to 9.4
years, so part of the income gain is fewer children and more earners per household. Workers'
pay is the cleaner measure: men gained in 2016–2019 and 2021–2023 and not in 2024 (−0.2);
women fell back in 2024 (−2.1). Three of the four series paused in 2024. [INFERENCE] Those two bursts coincide with tight
low-wage labour markets, so a group-specific convergence is not identified, and one flat
year does not establish a plateau. Across generations the flattening is clearer: the
same-age tax shortfall is $12.1k, $8.4k and $7.0k for the first, second and third-plus
generations.

## Relation to the interest-on-gap calculation

The September 18 [interest lane](../infra/immigration-fiscal/gap_interest_2026_09_18/README.md)
(ladder 137) reports $3.05tn of debt after ten years. It compounds a constant **−$263bn
absolute balance forward** at 3.22%; that balance is superseded, includes the group's share
of a deficit every resident runs, and carries its own correction banner. The totals here run
**backward**, use the conditional net cost to other residents, vary with each year's
population and budgets, and add no interest. The two must not be compared or summed.

## What would make it measured

Rebuild the base account on each CPS ASEC public file, 2005–2025: Census-modelled
taxes and credits, reported transfers with year-specific administrative ratios,
coverage-based medical transport and public pupils. Files before 2019 are
fixed-width with changing variable names, and the 2014 and 2019 redesigns break
income series. The repository holds 2022–2026 only.

[INSTRUMENT] LLM-assisted modelling on a politically charged topic; the measured
series and each assumption are separately inspectable.

## Revisions

2026-09-21: added the programme-by-programme version and the 2020–2021 sensitivity. The
coarse totals are unchanged; the combined range widens slightly to $1.3–2.2tn, $2.0–3.3tn
and $2.4–3.9tn because measured programme growth and the pandemic attribution pull in
opposite directions.

2026-09-21, trend wording: "no slowdown through 2024" held for per-capita income only.
Household income gained 0.2 points in 2024 after about 1.1 a year, so three of the four
series paused that year. Ladder 163 carries the same correction. No total changes.

2026-09-23, adopted main case: `backcast.py` also reads the adopted 2024 bands from
`main_case_2026_09_23/derived/main_case_bands.csv` and adds them as concepts with an `_adopted`
suffix. Every September 20 row and column is unchanged, checked value by value. On the adopted
anchor the whole-budget rules give $1.75–2.49tn (10 years), $2.52–3.74tn (15) and $3.00–4.62tn (20);
with full proportional services, $2.68–3.30tn, $3.82–4.88tn and $4.61–6.02tn. Concept affected: the
back-cast's 2024 anchor. [Decision](../decisions/2026-09-23-main-case-general-government-and-use-keys.md).
