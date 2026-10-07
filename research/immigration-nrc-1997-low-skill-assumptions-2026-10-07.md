# The 1997 and 2016 National Academies results for low-skill immigrants, assumption by assumption

**Verdict:** In every scenario the two National Academies reports publish by education, an immigrant
without a high-school diploma is a net fiscal cost. The 1997 baseline gives −$89,000 over the immigrant's own life and
−$13,000 with descendants (1996 dollars). The 2016 report gives −$109,000 to −$115,000 for the immigrant and
−$116,000 to −$185,000 with children and grandchildren (2012 dollars), and that is on its most favourable treatment of
public goods. The positive headline of 1997 (+$80,000 for the average immigrant) rests on a rule that froze federal
debt from 2016; without it the average is −$15,000, and the rule did not happen. The report's judgment calls do not all
lean one way: leaving out the taxes on capital that works with an immigrant leans against immigrants and is the largest
single adjustment in either direction (Clemens: +$237,000 for a dropout), and the low interest rates of 2009–2021 favour
them. Only that capital adjustment turns the dropout positive. [SOURCE: NRC 1997 Tables 7.5–7.6; Clemens 2023
Table 2 reproducing Blau et al. 2017; INFERENCE]

**Scope:** consolidated government budgets, net present value per new immigrant, as each report defines it. The 1997
report covers the immigrant and all descendants over 300 years at a 3% real rate in its baseline; the 2016 figures cover
75 years, children and grandchildren, 3%. The two are not on one basis, so the rows below are compared by sign and
direction, not subtracted. No labour-market or non-fiscal effects. [FRAMING-SENSITIVE: whether the budget is the right
welfare measure for natives]

## 1. What the reports say

National Research Council, *The New Americans*, chapter 7, Table 7.5, p. 334 (1996 dollars, baseline) [SOURCE:
https://www.nationalacademies.org/read/5779/chapter/9, table text read from the chapter page]:

| | Less than high school | High school | More than high school | Overall |
|---|---:|---:|---:|---:|
| Immigrant and descendants | −$13,000 | +$51,000 | +$198,000 | +$80,000 |
| Immigrant alone | −$89,000 | −$31,000 | +$105,000 | −$3,000 |
| Descendants | +$76,000 | +$82,000 | +$93,000 | +$83,000 |

The report's own sentence: the lifetime impact with descendants "is slightly negative for those with less than a high
school education; substantial and positive for those with a high school education, and strongly positive, at nearly
$200,000 per immigrant, for those with more than a high school education."

Table 7.6, the average immigrant by scenario (1996 dollars):

| Scenario | State and local | Federal | Total |
|---|---:|---:|---:|
| Baseline: debt/GDP frozen from 2016, half tax rises, half benefit cuts | −$25,000 | +$105,000 | +$80,000 |
| No budget adjustment | −$25,000 | +$10,000 | −$15,000 |
| 1996 welfare reform | −$22,000 | +$110,000 | +$88,000 |
| 1996 welfare reform and no budget adjustment | −$22,000 | +$15,000 | −$7,000 |
| Interest rate 2% | −$5,000 | +$223,000 | +$219,000 |
| Interest rate 8% | −$19,000 | +$27,000 | +$8,000 |

The report calls the no-adjustment path unrealistic (debt reaching 3.9 times GDP by 2050) and prefers the baseline. It
does not publish the education rows under any alternative scenario.

National Academies, *The Economic and Fiscal Consequences of Immigration* (Blau and Mackie, 2016), as reproduced in
Clemens (2023, CGD WP 632, Table 2, from Blau et al. 2017 pp. 445–7). Thousands of 2012 dollars, 75 years, immigrants
charged nothing for pure public goods (defense, existing interest) [SOURCE: Clemens PDF text; secondary reproduction,
primary tables not re-read]:

| Less than high school | Immigrant: taxes | benefits | net | With children and grandchildren: net |
|---|---:|---:|---:|---:|
| With already-legislated fiscal changes | 272 | 381 | **−109** | **−116** |
| Excluding all changes to fiscal policy | 213 | 328 | **−115** | **−185** |

When public goods are instead charged per head, the average immigrant of all education levels pays 0.633 of what he
receives, 0.716 with descendants (Blau et al. 2017, p. 454, quoted by Clemens §5.4). So on that treatment even the
average immigrant is a net cost.

## 2. Each assumption against what happened or the best evidence

| Assumption | Report | Leans | What happened or best evidence | Effect |
|---|---|---|---|---|
| Debt/GDP frozen from 2016 | 1997 baseline | toward immigrants | Debt held by the public 76.0% of GDP (2016) → 97.4% (2024) [SOURCE: OMB Historical Table 7.1; [back-test](immigration-projection-backtest-2026-09-19.md)] | Average +$80,000 → −$15,000; dropout row not published |
| Pure public goods and existing interest at zero marginal cost: "their costs are allocated to no one" | 1997, 2016 | toward immigrants | A legitimate marginal-cost choice; per-head charging makes the average immigrant negative in 2016 (0.633 / 0.716) | Sign of the average turns |
| No excess burden of the taxes that close a deficit | 1997, 2016 | amplifies either sign | Raising $1 costs payers about $1.25 (OMB A-94; range 1.10–1.50) [SOURCE: `infra/immigration-fiscal/excess_burden_2026_10_07/RESULT.md`] | Dropout with descendants −$13,000 → about −$16,000; own life −$89,000 → about −$111,000 [CALCULATION: × 1.25] |
| No behavioural response to the higher post-2016 taxes: "This assumption is unrealistic" | 1997 | toward immigrants | Higher rates lower the taxable income of the later generations credited with paying them | Unquantified |
| Capital-income taxes on capital working with the immigrant omitted | 2016 | against immigrants | Clemens: dropout −$109,000 → at least +$128,000; uses the nonfarm business sector's capital share 0.436 (BLS, owner-occupied housing excluded) for a dropout's job and charges no matching public capital [SOURCE: Clemens Table 3; repo method check `immigration-clemens-method-check-2026-06-24.md`] | Sign turns for dropouts |
| Discount rate 3% real | 1997 | neutral at the time | Real rates were near or below 1% for much of 2009–2021 [TRAINING-DATA]; at 2% the 1997 average is +$219,000 | Favours immigrants |
| Pre-reform benefit rules | 1997 baseline | against immigrants | The 1996 welfare reform passed; +$8,000 on the average | Favours immigrants |
| Descendants' schooling from estimated transitions | 1997 | neutral | GSS held-out cohorts: no general optimistic bias [SOURCE: back-test §2]; Mexican 1975–80 entrants' log income gap −0.415 (1990) → −0.419 (2023) [back-test §3] | Mixed |

Lean of these findings against the lean of the set (evidence-symmetry rule 4): of eight assumptions, three lean toward
immigrants, three lean against or turned out in their favour, two are neutral or mixed. The claim that every judgment
call in these reports favoured immigrants is wrong. What does hold: the one favourable assumption with an observed
outcome, the debt freeze, failed, and it carried the 1997 headline.

## 3. The descendant term changed sign between the reports

In 1997 a dropout's descendants add +$76,000 and nearly cancel his own −$89,000. In the 2016 figures his children and
grandchildren make the total worse: −$109,000 → −$116,000 with legislated changes, −$115,000 → −$185,000 without them.
Part of that is the window: 75 years catch the children's schooling but only part of their working lives, and 1997 ran
300 years with a debt rule that raised every later generation's taxes. The 1997 report's own Table 7.8 (r = 3%) shows
how much the window matters for the average immigrant: −23% of the 300-year value is reached at 25 years, 53% at 75 and
69% at 100. The two cannot be reconciled from the published
tables. The direction is still informative: on the newer data and a shorter horizon, the descendants of a low-skill
immigrant do not repay his deficit. [INFERENCE; would change it: the 2016 education rows on a 300-year horizon]

## 4. Disconfirmation searched

- The capital-tax omission (section 2) is the strongest evidence against a low-skill fiscal cost. It rests on applying
  the business sector's average capital share (0.436) to a dropout's job, whose own capital intensity is not measured,
  and on capital that is net new to the US tax base; matching public capital is not charged. [INFERENCE]
- Lower realized interest rates favour the 1997 average; the report did not publish the dropout row at 2%.
- The 1996 welfare reform happened and moved the average up $8,000.
- The GSS schooling back-test does not find the 1997 transitions optimistic.

None of these is a published dropout row with a positive sign other than Clemens's adjustment.

## 5. Open

- The 1997 dropout row without the debt freeze, at 2%, or with welfare reform: needs the report's model, not published.
- The 2016 per-head public-goods rows by education: Blau et al. 2017 pp. 445–54, not yet read from the primary.
- Clemens with matching public capital charged: the main case's return on public capital is the mirror item.
