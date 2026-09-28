claude-opus-5-5

# NAS 2017, Table 8-1, and the dependents definition behind it

This check was not blind: the ratios 0.79 and 0.90 were known before the run, and the ±0.05 tolerance was written
down after it. It is scored as a disclosed comparison, not a pre-registered test.

Source: National Academies of Sciences, Engineering, and Medicine (2017), *The Economic and Fiscal Consequences of
Immigration*, https://doi.org/10.17226/23550. Local PDF `sources/immigration-fiscal/data/external/nas_2016/23550.pdf`,
sha256 `c6fffc8f764e257b6a19794171e61e6b1bfc7e29f36187db0aaef532b475d68f`. Table 8-1 is on printed p. 389 (PDF page
414). `score.py` parses the populations and the Total rows from that page with `pdftotext -layout`.

## Table 8-1: Net Per Capita Fiscal Impacts, in 1994 and 2013 (Total rows) [SOURCE: NAS 2017, p. 389]

| Year | Group (population) | Outlays | Receipts | Receipts/Outlays |
|---|---|---:|---:|---:|
| 1994 | 1st Generation and Their Dependents (29.9 million) | 13,511 | 8,985 | 0.665 |
| 1994 | 2nd Generation and Their Dependents (20.8 million) | 18,454 | 12,681 | 0.687 |
| 1994 | 3rd Generation and Their Dependents (212.2 million) | 13,617 | 11,635 | 0.854 |
| 2013 | 1st Generation and Their Dependents (55.5 million) | 15,908 | 10,887 | 0.684 |
| 2013 | 2nd Generation and Their Dependents (23.3 million) | 19,194 | 14,534 | 0.757 |
| 2013 | 3rd Generation and Their Dependents (237.3 million) | 17,894 | 14,286 | 0.798 |

> "NOTE: “Dependent” and “independent” are defined as in Box 8-2. Outlays include all government spending, including
> interest payments and public goods, which are allocated equally to all groups on a per capita basis. Population
> counts are the sum of independents and dependents in each group. [...] Data are from March Current Population
> Surveys. Estimates are for scenario 1 (see Box 8-1) which assigns the average costs of public goods to new
> immigrants, as opposed to the marginal cost, and includes interest payments." [SOURCE: NAS 2017, p. 389]

Ratios to the population-weighted average of the three groups [CALCULATION: `score.py`]:
- first generation, 2013: receipts 0.794 and outlays 0.902, the 0.79 and 0.90 of the frozen tolerance;
- first generation, 1994: receipts 0.787 and outlays 0.966.

## Box 8-2: Definitions of Dependent and Independent Persons [SOURCE: NAS 2017, p. 377]

> "Dependent: For the purpose of the panel’s estimates, we consider dependents to be anyone: (1) under age 18,
> (2) ages 18 through 21 and in high school full time, or (3) ages 18 through 23 and in school full time or part time
> with income below half of the poverty level for one person. We also consider single individuals who are ages 18
> through 23 and not in school but with income below half of the poverty level (for one person) who live with at
> least one independent person (typically a parent) as a dependent person; 1.2 percent of the population are in this
> category and they are treated as dependents but are not assigned education costs."

The account's grouping counts only the under-18s as dependents (`PREDICTIONS.md`, check 2). The 18–23 clauses are
the dependent-definition gap named at the freeze.

## Institutionalized persons

Chapter 8's methods section adjusts the age profiles "to reflect the total U.S. resident population instead of just
the household-resident population", because "the CPS does not include persons in institutions" (NAS 2017,
pp. 468–469). Table 8-1 is from the March CPS; its note does not say whether that adjustment reaches it.
[SOURCE: NAS 2017, p. 468; INFERENCE on its reach]
