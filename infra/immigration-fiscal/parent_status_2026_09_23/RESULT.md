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
