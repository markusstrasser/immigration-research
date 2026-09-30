---
date: 2026-09-30
concepts: [legacy, debt, public-pensions, comparison-basis, cost-allocation]
status: adopted
supersedes: []
relations:
  - qualifies: decisions/2026-09-29-main-case-v4.md
evidence: infra/immigration-fiscal/legacy_comparators_2026_09_30/verification-2026-09-30.md
---

# 2026-09-30: State the federal and pension legacies separately

## Decision

Use **2005–2023** for the main federal comparison, with interest-equivalent charges expressed in
2024 dollars. Show the earlier starts as sensitivity checks. State the public-employee pension
legacy alongside it, using the same group keys and headcount. Add neither to the annual fiscal
headline or the fiscal-plus-social total, and do not adopt their arithmetic sum as a reconciled
legacy total. The operator authorized completing the source checks and documentation and accepted
2005 as the window; the checks below change the proposed combined wording.

The federal comparison on the accrual convention is **+$72.64 / +$72.41bn** over a same-sized
third-plus non-Hispanic white slice; carrying the accrual with payroll instead of benefits gives
**+$63.71 / +$63.48bn**. Thus the existing carry-method sensitivity spans **$63.5–72.6bn**.
These are hypothetical annual financing charges: past accrued promises are compounded as if
borrowed at Treasury rates. They are not observed interest paid on an origin group's debt.
The cash-benefit convention gives **+$11.54 / +$11.31bn**; it still inherits NIPA's accrued
public-employee compensation and has not been reconciled to cash borrowing.
[CALCULATION: `legacy_comparators_2026_09_30/derived/legacy_differences.csv`]

The corrected public-employee pension comparison is **+$4.89 / +$4.68bn** of attributed 2024
interest expense, including imputed interest. The pension kernel weights service years
**1980–2023**; it is not restricted to the federal model's 2005 window.
[CALCULATION: `pension_legacy_2026_09_30/derived/summary.csv`, arm `adopted`,
group `mexican_origin_rough_minus_A1_white`; `derived/headcount_path.csv`]

## Why the proposed sum is not adopted

The strongest case for combining is that Treasury securities and public-employee pension
liabilities are distinct instruments, with distinct interest entries. However, the federal lane
does not observe group-specific securities: it capitalizes a modeled spending-minus-receipts gap.
Its `programme_federal()` carries BEA consumption from Table 3.17; `federal_path()` forms the
gap and `stock()` compounds it without converting public-employee pension compensation to cash.

BEA includes pension promises earned in compensation, even when employers have not paid them
into a fund. Unpaid contributions therefore can enter that modeled financing stock as well as
the pension liability. Excluding pension interest from the rate numerator does not settle this
overlap in the principal. The pinned Table 3.18B explicitly has a pension-and-insurance bridge
between federal budget and NIPA transactions. [SOURCE: [BEA accrual methodology](https://www.bea.gov/index.php/news/blog/2013-06-17/bea-move-accrual-accounting-defined-benefit-pension-plans),
[government pension treatment](https://www.bea.gov/help/faq/553);
DATA: `sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx`, T31800B-A lines 21–24;
CALCULATION: `debt_legacy.py` → `programme_federal`, `stock`; comparator `legacy.py` → `federal_path`]

The paired arithmetic sum would be **$77.53 / $77.09bn**, but it is **unreconciled**.
It is retained here as the rejected presentation, not as an additional cost estimate.
Different time windows are another reason to name each component's scope.
[CALCULATION: sum of the two paired differences above; FRAMING-SENSITIVE]

## Checks and alternatives

- Federal source checks rebuilt all 72 stocks from annual flows and raw OMB rates, checked
  all 16 group/basis/end input sets against the current white re-key, and spot-checked raw ACS
  income and age cells. Saved precision and the original lane's parity checks pass.
- Pension source checks verified pinned BEA, Federal Reserve and Treasury inputs. They found
  stale published-count comparator shares mixed with current row-4 adjustments. The fix uses
  the same gated export as the federal comparator lane and retains the engine union separately.
- Earlier federal starts give **$87.65–87.84bn** (2000) and **$112.83–112.84bn** (1990) on the
  original accrual carry. The main start follows annual ACS headcounts; earlier headcounts are
  interpolated from censuses. Even after 2005, some ACS gaps are interpolated and relative
  income before 2008 is held at its 2008 value. This is a modeled back-cast throughout.
- The pension service-year kernel, historical per-programme intensities, Treasury-rate
  capitalization and benefit/payroll carry are assumptions. Low/high denote paired case
  specifications, not confidence intervals. The overall historical-demography bias is unquantified.

## Revisit if

A common annual financing bridge separates paid and unpaid public-employee pension costs,
settlements and revaluations from borrowing, and reconciles both attributed stocks. That would
permit testing additivity. New historical group-specific service or accrual profiles would also
justify replacing the held-current-key back-casts. No change to the current headline is made here.
