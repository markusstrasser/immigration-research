# Legal status of Mexico-born parents of US-born children, by education

**Verdict:** About half of the low-education Mexico-born parents of US-born minor children are
imputed unauthorized, not almost all. Among parents without a high-school diploma, 47% are
imputed unauthorized under the paper's rules and 62% with the Medicaid clause dropped; outside
California, where the clause matters least, 54% and 62%. High-school-only parents: 37% and 52%.
Of the 1.35M US-born minors whose best-educated resident parent lacks a diploma, 45–62% have no
legal parent in the household; across all 5.0M US-born minors with a Mexico-born parent, 30–41%.
A rule granting citizenship only when a parent is legal would, on current status, exclude about
half of the children in the lowest-education Mexican families and about a third overall.
[CALCULATION: `parent_status.py`; DATA: CPS ASEC 2025 public use, 160-replicate SDR]

Date: 2026-09-23. Question from the operator: "almost none of the low skill parents are legal?"

## Method

- Status: the Borjas (2017) residual imputation of `status_impute_2026_09_16` (rules quoted in its
  `impute_status.py`), imported unchanged. The script reproduces that lane's published Mexico-born
  25–64 unauthorized counts (3.917M paper rules, 4.778M without Medicaid) before tabulating.
- Two rule sets. The paper's rule (c) calls any Medicaid recipient legal; California's Medi-Cal
  covered income-eligible unauthorized adults in 2024, so that rule moves California's
  low-education parents from 61% to 26% unauthorized. Dropping the clause instead calls legal
  noncitizens on Medicaid unauthorized. The truth sits between the two columns.
- Parents: Mexico-born (`PENATVTY` 303) people named in `PEPAR1`/`PEPAR2` by a co-resident
  US-born (`PRCITSHP` 1) person under 18. Education from `A_HGA`.
- Children: US-born minors with at least one co-resident Mexico-born parent; "no legal parent"
  means no co-resident parent (Mexico-born, other foreign-born or native) is imputed legal.

## Parents of US-born minors, share imputed unauthorized (SDR se)

| Education | Parents | Paper rules | No Medicaid rule | Rest of US, paper | Rest of US, no Medicaid |
|---|---:|---:|---:|---:|---:|
| Below high school | 1.51M (n 743) | 47% (2.2) | 62% (2.0) | 54% (2.7) | 62% (2.4) |
| High school only | 1.40M (n 684) | 37% (2.6) | 52% (2.6) | 45% (2.9) | 55% (3.0) |
| Some college | 0.47M (n 233) | 24% (3.3) | 30% (3.5) | 25% (3.7) | 32% (3.9) |
| Bachelor's or more | 0.34M (n 162) | 22% (4.1) | 29% (4.2) | 28% (5.1) | 33% (5.1) |
| All parents | 3.71M (n 1,822) | 38% (1.6) | 51% (1.5) | 45% (1.8) | 53% (1.8) |
| All Mexico-born adults 25–64 | 9.46M | 41% (1.2) | 51% (1.2) | 49% (1.3) | 55% (1.4) |

California alone, below high school: 26% (4.3) paper rules against 61% (4.2) without Medicaid.
[DATA: `derived/mexico_born_parents_by_status.csv`]

## US-born minors with a Mexico-born parent, share with no legal parent present

| Highest resident parent's education | Children | Paper rules | No Medicaid rule |
|---|---:|---:|---:|
| Below high school | 1.35M (n 604) | 45% (3.3) | 62% (3.2) |
| High school only | 1.88M (n 847) | 33% (2.7) | 46% (3.1) |
| Some college | 1.00M (n 471) | 17% (2.7) | 22% (3.0) |
| Bachelor's or more | 0.77M (n 333) | 14% (2.8) | 19% (3.2) |
| All | 5.01M (n 2,255) | 30% (1.5) | 41% (1.6) |

[DATA: `derived/usborn_children_by_parent_status.csv`]

## Limits

- Status is the parent's imputed status in March 2025, not at the child's birth. Parents who
  legalized after the birth count as legal here, so the share unauthorized at birth is higher.
- The residual method over-assigns unauthorized status overall (Borjas says so), while rules (c)
  and (i) (Medicaid, legal spouse) pull mixed-status parents into the legal cell. The Mexico-born
  total (4.57M all ages) sits near Pew's 4.3M for mid-2023; the split by education and
  parenthood is not validated against an external source.
- Co-resident parents only; the CPS under-samples 2022–24 arrivals.
- Imputed legal includes naturalized citizens and green-card holders; the imputation cannot
  separate them.

---

# Children's outcomes by their parents' status (added 2026-09-23)

**Verdict:** While the parents are unauthorized, their US-born children do worse than the children
of legal Mexican immigrants: poorer as minors and less often in college as young adults, after
holding parental education, age, state and two-parent families fixed. When the parents entered
illegally but later legalized, as the 1986-amnesty generation did, their children turned out the
same as the children of legal entrants on schooling, income, arrests and incarceration. The handful
whose mothers never legalized did much worse, on seven cases. Descriptive, not causal: status is
imputed in the CPS and recalled by the adult child in IIMMLA, and unauthorized parents differ in
ways coarse controls do not capture (time in the US, English, occupation).

## Adults, Los Angeles 2004 (IIMMLA)

US-born Mexican-origin respondents aged 20–40 with a Mexico-born mother, by how the mother entered
(Q127A–Q128). Unweighted quota sample. The script first reproduces the IIMMLA lane's Mexican
second-generation row (n 553; no diploma 19.0%, BA+ 16.8%, arrested 17.4%, incarcerated 11.2%).

| Mother entered | n | Years of school | No diploma | BA+ | Employed | Arrested | Incarcerated | Mother without diploma |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| With a green card | 231 | 13.46 | 16% | 20% | 68% | 19% | 10% | 37% |
| Without one | 150 | 13.47 | 19% | 20% | 73% | 15% | 10% | 60% |
| of which with no papers at all | 54 | 13.56 | 19% | 24% | 66% | 13% | 6% | 65% |
| Not legal by 2004 | 7 | 11.43 | 57% | 0% | 71% | 14% | 14% | 43% |

Controlling for age, sex and both parents' education, "without a green card" minus "with one":
years of school +0.09 (SE 0.22), no diploma +2.1 points (4.2), BA+ +2.5 (4.2), employed +10.1
(4.9), personal income +$3.5k (2.0k), arrested −0.1 (4.0), incarcerated +2.1 (3.3). By the
father's entry, no papers at all (n 72): BA+ +11.3 (5.1) and arrested +10.5 (5.4); nothing else
separates. Fathers not legal by 2004: n 12. [CALCULATION: `iimmla_parent_entry.py`;
DATA: `derived/iimmla_second_gen_by_parent_entry.csv`, `derived/iimmla_entry_status_gaps.csv`]

These respondents were born about 1964–1984; nearly all their parents had legalized by 2004, most
of those who entered without papers presumably under the 1986 amnesty [INFERENCE from timing].
The "without papers" contrast is therefore an entry-status contrast, not a lifelong one.

## Children today (CPS ASEC 2025)

US-born children living with a Mexico-born parent. "No legal parent" = every co-resident parent
imputed unauthorized; "legal immigrant parents" = every co-resident parent foreign-born, at least
one imputed legal. Two rule sets (no Medicaid clause / paper rules); adjusted differences control
for child's single year of age, highest parental education (4 levels), California and two-parent
households; SDR standard errors.

| Outcome | No legal parent | Legal immigrant parents | Adjusted difference | White US-born parents |
|---|---:|---:|---:|---:|
| Minors: SPM poor | 36% / 33% | 16% / 24% | +19.7 (3.4) / +10.2 (3.6) | 6% |
| Minors: uninsured now | 18% / 25% | 12% / 9% | +4.8 (2.9) / +14.1 (3.4) | 4% |
| Minors: family resources per person | $12.6k / $13.1k | $16.8k / $15.3k | −$3.9k (0.8) / −$1.7k (0.7) | $29.9k |
| 19–24 at home: high-school diploma | 90% / 90% | 97% / 95% | −5.3 (1.8) / −3.4 (2.1) | 92% |
| 18–24 at home: in or ever attended college | 44% / 41% | 62% / 60% | −12.2 (4.1) / −13.6 (4.2) | 55% |
| 18–24 at home: employed | 56% / 55% | 64% / 63% | −8.5 (3.9) / −6.8 (3.9) | 58% |
| 18–24 at home: neither in school nor working | 15% / 15% | 11% / 11% | +4.1 (2.6) / +4.3 (2.8) | 13% |

Children: 2.1M / 1.5M with no legal parent, 1.5M / 2.1M with legal immigrant parents (n 922 / 666
and 690 / 946); young adults n 406 / 315 and 379 / 470. [CALCULATION: `cps_children_outcomes.py`;
DATA: `derived/cps_children_outcomes_means.csv`, `derived/cps_children_outcomes_gaps.csv`]

At the same parental education the Mexican-family young adults attend college more often than
white young adults living with parents: parents with a high-school diploma only, 48% / 44% (no
legal parent) and 62% / 61% (legal) against 29% (white, n 519). "In or ever attended college"
counts community-college enrollment and is not degree completion; the degree gap persists into
the third generation (FAQ 5, ladder 178). The white cell below high school is small (n 98) and
unusual (28% of its minors uninsured); it is not used.

## Limits of the children's comparison

- Status: imputed for current CPS parents (see above for the rule-set bias; rules on program
  receipt and government jobs put program users in the legal cell, which biases poverty and
  insurance comparisons in opposite directions under the two rule sets); recalled by adult
  children in IIMMLA.
- Young adults are observed only while living with a parent; CPS counts dormitory students at
  home, but co-residence still differs by group.
- IIMMLA is Los Angeles in 2004, unweighted; its never-legalized cells have 7 and 12 cases.
- Nothing here separates parental status from what goes with it: recency of arrival, English,
  informal work, fear of enforcement.
