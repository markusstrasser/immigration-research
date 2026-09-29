# Cumulative fiscal cost 2005–2024: what is measured and a back-cast

Date: 2026-09-20. [MODEL / FRAMING-SENSITIVE] Calculation record; narrative authorship remains operator-owned.

**Adopted main case (2026-09-29: the September 27 case with the pension accrual at payable benefits, long-run property taxes, the IRS income-tax key, state prices, roads by miles and five smaller keys; [decision](../decisions/2026-09-29-main-case-v4.md)):** on the $371–435bn anchor the whole-budget rules give **$3.2–4.1tn over 2015–2024, $4.5–6.0tn over 2010–2024 and $5.6–7.7tn over 2005–2024**. The September 27 case is carried back as before and v4's change line by line, each part on its own NIPA series: the pension accrual follows the OASDI and HI contributions that earn it, and the benefits it no longer charges follow their own benefit lines. The return on public capital is an imputed resource cost, not a cash flow, and is $0.30–0.50tn of the ten-year total under the ratio rule ($0.33–0.55tn flat). The cash set is not carried back as a concept of its own, and the programme-by-programme version below stays on the September 27 case.
[CALCULATION: `backcast.py --case sept29` → `derived/sept29/backcast_windows.csv`, concepts `*_sept29_*`; `derived/sept29/case_parts_windows.csv` (c4dd711)]

**September 27 case (return on public capital, long-run road and park responses, rental assistance at 1 and every government enterprise; [decision](../decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md)):** on the $322–387bn anchor the whole-budget rules give **$2.8–3.7tn over 2015–2024, $4.0–5.4tn over 2010–2024 and $4.8–6.8tn over 2005–2024**. The schools case is carried back as before, and each addition on its own national series: roads and parks on NIPA 3.17, rental assistance on NIPA 3.13, the enterprise surplus on NIPA 3.1 line 19, and the return on public capital on BEA Fixed Assets Table 7.1 net stocks at a constant real rate. The return is an imputed resource cost, not a cash flow, and is $0.29–0.49tn of the ten-year total under the ratio rule ($0.32–0.53tn flat). The enterprises' national operating loss was $3.4bn in 2005 and $2.8bn in 2015 but $47.5bn in 2024, so their part is small before recent years; the loss is a trend, not a 2024 spike (NIPA 3.8: transit −$54.1bn → −$66.7bn and public housing −$27.5bn → −$40.3bn, 2019 → 2024; 2020–22 are distorted by relief). The programme-by-programme version in the debt legacy lane, cash only (without the capital return and the capped programmes) and with 2020–2021 measured instead of held at the 2024 credit ratio (section below; cbaddcf), gives $2.61–3.00tn, $3.72–4.28tn and $4.51–5.21tn. The whole-budget rules charge the pandemic spike at the group's overall 2024 spending ratio, 0.62–0.65 of national spending per head, below its measured share of the payments, and do not move.
[CALCULATION: `backcast.py` → `derived/backcast_windows.csv`, concepts `*_sept27_*`; `derived/case_parts_windows.csv` (de468f2); `debt_legacy_2026_09_23/derived/adopted_backcast_windows.csv` (e03450b)]

Earlier anchors, kept as the calculation record ($tn in 2024 dollars, whole-budget rules unless stated):

| 2024 anchor | 2015–2024 | 2010–2024 | 2005–2024 | Source |
|---|---|---|---|---|
| Schools case (September 26), $258–292bn; programme version 2.47–2.75 / 3.50–3.89 / 4.21–4.72 | 2.2–2.8 | 3.2–4.2 | 3.9–5.2 | concepts `*_schools_full_*` (c0297e4); programme version `debt_legacy_2026_09_23/derived/adopted_backcast_windows.csv` (1db19c8) |
| First-year budget response and the September 24 case, $201–246bn; group receipts $488.5bn shared after the data corrections, $545.1bn before | 1.7–2.4 | 2.5–3.6 | 3.0–4.5 | concepts `*_corrected_*` |
| September 23, $203–250bn | 1.7–2.5 | 2.5–3.7 | 3.0–4.6 | concepts `*_adopted_*` |
| September 20, as published, $165–197bn; every rule, the programme version included, 1.3–2.2 / 2.0–3.3 / 2.4–3.9 | 1.4–2.0 | 2.0–3.1 | 2.4–3.8 | the tables below |

[CALCULATION: `backcast.py` → `derived/backcast_windows.csv`]

**Result on the September 20 anchor, which the tables below compute:** No historical cost is measured here. The account exists for income-year
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
With 2020–2021 measured (below), the first row is 1.56–1.86, 2.23–2.64 and 2.60–3.13 and the second
1.83–2.11, 2.75–3.14 and 3.33–3.82; under full proportional services the two rules give 2.51–2.93, 3.58–4.32
and 4.31–5.31. The third row removes about three times what the measurement supports.
[CALCULATION: `backcast_pandemic_measured_2026_09_28/derived/backcast_measured_windows.csv`, variant
`refundable_pandemic`, SSN rule `borjas` (cbaddcf)]

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
year. The programme rule attributes the 2020–2021 credits at the group's 2024 ratio (2.34
times other residents per person, an EITC and child-credit pattern), which makes the pandemic
years 35–38% of its ten-year total. Measured on CPS ASEC 2020–2025 with each payment's statutory
SSN rule (`backcast_pandemic_measured_2026_09_28`, cbaddcf), the group got the 2020 payments at
0.87 times other residents per person (1.02 before the SSN rule) and the 2021 payments at 1.03,
against the 2.34 charged (2.16 high). The exclusion is statutory (CARES Act §2201, IRC 6428(g)):
the advance payment excluded every joint return with a spouse lacking an SSN, the children
included (military families aside), until CAA 2021 §273 restored the SSN spouse and children as a
2020 credit. The SSN rule is about a tenth of the payment cut; per-head pricing is the rest. With
the payments at their measured shares, 2020–2021 supply 31–33% of the programme-rule total
(29–31% income-adjusted). CPS ASEC reports programme receipt by origin in every year: in 2019–2023
the relative use of SNAP, SSI and Social Security stays within 10% of 2024, one noisy SSI cell
aside; unemployment ran 13–14% lower in 2020; smaller keys (veterans' pensions, cash assistance,
WIC, energy) move more but are noisy; workers' compensation's 2024 value (1.80 times other
residents) exceeds every earlier year (0.76–1.23). Replacing every CPS-keyed line in 2019–2023
barely moves the totals. Medical, age, school and resource keys stay at 2024, and the group's
relative use of other programmes before 2024 is unmeasured.

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

2026-09-29: the main case of 2026-09-29 ($371–435bn; [decision](../decisions/2026-09-29-main-case-v4.md), ladder 275) is carried back: $3.2–4.1tn over ten years, up from $2.8–3.7tn. v4's change is carried line by line, the pension accrual on the contributions that earn it (c4dd711). The September 27 paragraph stays below it as the record of how that case's additions were carried. Concept affected: the cumulative figure's anchor.

2026-09-29, cleanup: the stacked paragraphs for earlier anchors are one table, and the dated notes are folded into the text. The programme version now quotes only the measured pandemic years; its figures with 2020–2021 at the 2024 credit ratio ($2.65–3.03tn, $3.77–4.31tn and $4.56–5.24tn) stay in `adopted_backcast_windows.csv` at e03450b. No figure changes. Concept affected: none; organization only.

2026-09-28, later: the pandemic years are measured (`backcast_pandemic_measured_2026_09_28`, cbaddcf; ladder 251). The group got the 2020–2021 payments at 0.87–1.03 times other residents per person, not at the 2024 credit ratio of 2.34, so the programme rule's ten-year total falls by $0.12–0.13tn on the September 20 anchor and $0.04–0.05tn on the September 27 case. The whole-budget rules and the headline do not move. Concept affected: the programme-by-programme back-cast's 2020–2021 attribution.

2026-09-28: the main case of 2026-09-27 ($322–387bn; [decision](../decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md)) is carried back: $2.8–3.7tn over ten years, up from $2.2–2.8tn. Each addition follows its own national series, the capital return stays in as an imputed resource cost, and the programme version is now cash only. Concept affected: the cumulative figure's anchor.

2026-09-26, later: the main case charges schools at their full average cost ([decision](../decisions/2026-09-26-main-case-schools-full-cost.md)). On that anchor the whole-budget rules give $2.2–2.8tn over ten years, up from $1.7–2.4tn, and the programme version gives $2.47–2.75tn. Concept affected: the cumulative figure's anchor.

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

2026-09-24, data corrections: `backcast.py` adds the main case with the September 24 corrections as
concepts with a `_corrected` suffix, anchored on `main_case_2026_09_24/derived/main_case_bands.csv`.
The corrections lower the group's receipts, so these concepts split each 2024 anchor on the corrected
receipts ($488.5bn, shared allocation, from that lane's `summary.json`; before them $545.1bn).
Every earlier row and column is unchanged, checked value by value. The whole-budget rules give
$1.73–2.43tn (10 years), $2.49–3.64tn (15) and $2.98–4.48tn (20); with full proportional services,
$2.64–3.23tn, $3.76–4.76tn and $4.54–5.94tn. Under the ratio and income rules 2020–2021 supply 28–32%
of the ten-year total. Concept affected: the back-cast's 2024 anchor and its split between receipts
and spending. [Decision](../decisions/2026-09-24-main-case-audit-and-outside-checks.md).
