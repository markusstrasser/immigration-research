# Benefits by immigration status and migrant emergency spending: where the money goes and how the account charges it

Date: 2026-09-24. The operator pasted the City Journal article on California's "shadow welfare
system" (2026-09-23, 20:10) and asked us to "Find it in other places … sherlock" (20:58).

Five lanes answer it:
- [California program costs](../infra/immigration-fiscal/california_program_costs_2026_09_23/RESULT.md);
- [improper payments](../infra/immigration-fiscal/improper_payments_unauthorized_2026_09_23/RESULT.md);
- [ITIN credits and student aid](../infra/immigration-fiscal/itin_credits_student_aid_2026_09_23/RESULT.md);
- [state programs outside California](../infra/immigration-fiscal/state_programs_unauthorized_2026_09_23/RESULT.md);
- [migrant shelters](../infra/immigration-fiscal/migrant_shelter_costs_2026_09_23/RESULT.md).

A sixth lane, on federal fraud by offender citizenship and the Minnesota cases, is running
(`infra/immigration-fiscal/fraud_by_citizenship_2026_09_24/`).

**Verdict:** Money paid on account of immigration status is real, mostly lawful and concentrated in
California.

- **California:** Medi-Cal for undocumented residents costs about $10–11bn a year from the state's
  General Fund.
- **Other states:** status-blind health programs elsewhere add $1.0–1.4bn ($1.5–2.1bn counting New
  York, inferred).
- **Shelters:** migrant shelter and emergency response cost five places $4.7bn in calendar 2024.
  About 95% of that was state and local money.
- **Improper payments:** about $1.1bn of federal money was claimed for services the state had to
  fund alone. The money was repaid, so it moved which government paid, not how much was spent.
- **Fraud:** none of the audits or prosecutions the lanes read found charged or adjudicated fraud
  tied to unauthorized status.

None of this is missing from our account. Every dollar sits inside BEA's 2024 national totals,
which the account assigns through its keys. Keys and actual use diverge only for shelters. There
the account charges the Mexican-origin group 12.9–22.6% of the outlays, while Mexican nationals were
0.50–0.84% of the people served. Charging by use would lower the main case by about $0.5bn
($0.45–0.84bn; at most $1.16bn). That is proposed, not adopted.

## The table

Dollars are a year unless marked. Categories:
- **lawful:** paid under a statute or budget act;
- **improper:** wrong funding source, or paid in error;
- **fraud:** charged or adjudicated deception.

| Program | Place | $ | Category | In our 2024 account |
|---|---|---|---|---|
| Medi-Cal regardless of status (about 1.7M undocumented enrollees) | California | $10.8bn General Fund in 2025-26 (LAO); DOF: $12.5bn total, $11.2bn state | lawful; enacted in SB 75 (2015), SB 104 (2019), AB 133 (2021), SB 184 (2022); adult enrollment frozen from 2026-01-01 | Inside BEA Medicaid, charged by the MEPS use key. The medical-ethnicity lanes test the group's own use (ladder 175, 206) |
| Federal money claimed for state-only services, returned | California | $1.108bn, once (2025-26) | improper, repaid | Moves the cost from federal to state; total unchanged |
| CMS preliminary review | CA, IL, OR, WA, DC, CO | $1.35bn, mostly California; overlaps the row above | improper, preliminary; three states dispute it | Same |
| OIG audit, managed-care proxy | California | $52.7M (2018-19) | improper, refunded | Outside 2024 |
| Status-blind health programs | IL, OR, NJ, DC, WA, CT, CO, MN, UT | $1.0–1.4bn documented; $1.5–2.1bn counting NY [INFERENCE] | lawful; Illinois closed its adult program on 1 July 2025, and a 2025 Minnesota law ended adult eligibility | Same Medicaid category; no extra charge |
| Additional child tax credit for SSN children of ITIN filers | federal | about $2–3bn [INFERENCE]; ITIN-only households lose it from TY2025 | lawful | Inside the CPS tax model's credits; consistent |
| State ITIN tax credits | CO, WA, MD (California publishes no split) | $65–75M | lawful | Negligible |
| State grants to undocumented students | CA, WA, MN | about $83M | lawful | Negligible |
| IRS stimulus paid to ineligible ITIN holders | federal | $7.5M, paid 2025 | improper, IRS error | Outside 2024 |
| Screened ITIN returns flagged as possible fraud | federal | $0.57M (2010) | suspected, never adjudicated | Outside 2024 |
| Charged or adjudicated benefit fraud tied to unauthorized status | all audits read | $0 | fraud | None |
| Asylum-seeker services | New York City | $3.75bn FY2024, $3.02bn FY2025 (local 62% and 49%, state 35% and 48%, federal 3%) | lawful; people of mixed status | State and local spending under national keys: the group is charged 12.9–22.6%; it was 0.50–0.63% of those served |
| State-funded asylum aid | New York State | $0.90bn SFY2024, $1.18bn SFY2025, $1.60bn SFY2026 projected; most paid to NYC, so do not add it to the NYC row | lawful | Same |
| Emergency Assistance family shelter (all families) | Massachusetts | $894M FY2024, $978M FY2025; migrant families 40–50%, so $0.36–0.45bn in FY2024 | lawful | Same |
| New-arrival payments | Chicago | $255M (2023), $366M (2024, 39% federal) | lawful | Same; Mexican nationals were 0.84% of 2024 shelter exits |
| Newcomer response | Denver | $14.5M (2023, partial), $45.4M (2024 estimate) | lawful | Same |
| Office of Migrant Services | Washington DC | $52M FY2023, $63M FY2024 | lawful | Same |
| **Shelters, all five places** | NYC, NYS, MA, Chicago, Denver, DC | **$4.7bn in calendar 2024** ($4.6–5.2bn), about 95% state and local | lawful | **The group is over-charged by about $0.5bn** ($0.45–0.84bn; at most $1.16bn) |

[SOURCE: each lane's RESULT.md, which carries the primary documents, page numbers and quotes.
CALCULATION: calendar-2024 blends and keying in
`migrant_shelter_costs_2026_09_23/cy2024_outlays.csv` and `derived/account_keying.csv`]

## What the account does with it

- **Medicaid.** California's program is state money spent on Medicaid-type care, so it sits
  inside BEA's Medicaid line. The account charges the Mexican-origin group 12.25% of that line
  through the MEPS use key. Whether that share is right is a question about the group's own use,
  which the medical-ethnicity lanes test, not about California's statute. Adding California's
  $10–11bn on top would count it twice.
- **Improper claiming.** Repaying federal money moves the cost between governments. The account
  counts all governments together, so the total does not change.
- **Credits.** The CPS tax model already carries the child credit for SSN children of ITIN
  filers. State credits and grants are tens of millions of dollars.
- **Shelters.** This is the one keying mismatch. National keys (cash assistance 16.5%, population
  12.0%, health 7.7%, other state benefits 22.6%) charge the group for services that went mostly to
  Venezuelans, then Ecuadorians, Colombians and Guineans. The correction, about −$0.5bn, is 0.2–0.5%
  of the $203.2–249.6bn main case. It is proposed, not adopted, and would join the dataset audit's
  small keying rows.

## What would change it

- **Origins at the 2022–23 shelter peak** were not recovered. A higher Mexican share then would
  narrow the over-charge. Even a 2% allowance leaves the account charging 6.5–11 times use.
- **BEA's treatment of shelter contracts** (purchases, or payments to nonprofit institutions) is
  [INFERENCE]. Mappings A–D in the shelter lane bracket it.
- **California's $10.8bn** is a budget estimate that includes In-Home Supportive Services. LAO
  says the cost is "more than double the initial estimates". Mid-year corrections added $0.82bn
  (January 2026) and $0.29bn (May 2026). These were repayments of federal funds, part of the
  $1.1bn improper row.
- **Fraud outside status programs**, for example provider networks billing Medicaid or child
  nutrition, is not in this table. It is the running lane's question.

## Frame

The account asks what the Mexican-origin group costs other US residents. The operator's question
is wider: all immigrants, and whether the money is legitimate. On the wider question, the
California and other-state programs serve undocumented people of every origin, and the shelters
served mostly recent arrivals from South America and West Africa. On the account's question, the
only correction the sweep finds is the shelter keying, and it lowers the charge. [FRAMING-SENSITIVE]

## Revisions

None yet.
