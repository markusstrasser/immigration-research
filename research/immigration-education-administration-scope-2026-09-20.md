# Education and general administration: current cost scope

Date: 2026-09-20. [MODEL SCOPE / SENSITIVITY] Billions of nominal calendar-2024 dollars per year, for the current observed Mexican-origin population, including descendants. These are neither all-immigrant totals nor estimates of new staff headcounts.

**Finding:** Education and staff within ordinary services already enter the main long-run result. Broad general public services are in the accounting ledger but assumed unresponsive in the main welfare case. No separate federal marginal-hiring model has been estimated.

## Already included

The preferred account assigns **$193.37bn shared / $199.57bn personal** of education current consumption. Its incidence proxy combines measured public-school enrollment with postsecondary exposure and reconciles to the BEA education envelope. The named education social-benefit category is separate. This is not just teachers' wages or the earlier stand-alone K–12 subtotal. [SOURCE: [spending builder](../infra/immigration-fiscal/full_account_spending_2026_09_20/builder.py), `education_services`; its `derived/allocations.csv`; [school enrollment builder](../infra/immigration-fiscal/school_enrollment_2026_09_20/builder.py).]

BEA government consumption includes employee compensation, purchased inputs and depreciation, net of relevant sales. Therefore school administrators, teachers, and staff producing other included services are already costed. Adding their wages again would double-count. The main case makes ordinary service costs fully responsive; it does not estimate the actual staffing response from population changes. [SOURCE A2: [BEA chapter 9](https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-09.pdf), pp.9-2–9-5; [current welfare calculation](../infra/immigration-fiscal/full_account_2026_09_20/welfare.py).]

## General public services held fixed

| Scope | National current consumption | Population-assigned target amount |
|---|---:|---:|
| Federal | 97.070 | 11.672 |
| State/local | 304.538 | 36.619 |
| Consolidated | 401.608 | 48.291 |

[SOURCE / DERIVATION] Pinned BEA Section3 workbook, Table3.17 consumption rows 2/12/22; national totals multiplied by 40.896574m / 340.110988m = 12.02448%. Workbook SHA256: `69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e`. See [spending reproduction](../infra/immigration-fiscal/full_account_spending_2026_09_20/README.md).

This function includes executive/legislative, tax collection/financial management and other general services. It is broader than payroll, and state/local “other” includes unallocable expenditure. The classification labels come from Table3.15.5; its investment-inclusive dollars are not substituted for Table3.17 current consumption.

The existing code combines this function with defense in `public_goods`. Its common response parameter therefore cannot isolate administration. The main case sets both responses to zero and leaves existing interest fixed. Zero is an assumption, not evidence that additional residents need no administration.

## Isolated arithmetic sensitivity

Keeping defense, existing interest and all other model assumptions unchanged, at fiscal-dollar weight one:

| Fraction of assigned general-service cost treated as responsive | Added federal-only cost | Added all-government cost |
|---|---:|---:|
| 10% | 1.17 | 4.83 |
| 25% | 2.92 | 12.07 |
| 50% | 5.84 | 24.15 |
| 100% | 11.67 | 48.29 |

[MODEL SENSITIVITY] Formula: assigned current consumption × response fraction. These fractions are illustrative assumptions, not estimated elasticities or a confidence interval. The table is an isolated calculation, not a change to the headline model or an estimated federal staffing bill. A defensible refinement would separate administration from defense and use agency caseloads, staffing and compensation, avoiding overlap with staff already in education, health, public safety and benefit administration.

Federal-to-state grants are consolidated once. Annual current consumption includes depreciation but not gross construction investment; adding an entire building's price to recurring annual costs would mix account bases. The model does not estimate short-run construction/hiring paths or separate casework requirements for each immigration status.

Validation: executable service partition/response mapping, preferred allocation outputs and pinned workbook federal/state rows checked; input/output hashes matched the existing audit. No generator changed or model rerun.
