# FY2024 detention spending: reconciliation and remaining identification gap

**Verdict, 2026-09-20:** Actual spending is measurable, but a complete national
detention-only total is **not identified by the public records acquired here**.
This is not impossibility in principle. Federal accounts reconcile; their public
program classifications lose the necessary custody split. National local-finance
records lack the matching purpose and reimbursement fields.

The reporting window is federal FY2024, October 1, 2023–September 30, 2024.
The target is actual ICE civil-custody payments and consolidated state/local costs,
not criminal imprisonment, all immigration enforcement, a policy's marginal cost,
or a Mexican-origin share. CBP short-term custody and ORR care require separate
program accounts and overlap checks if included in a wider custody definition.

## What we can establish

| Observed payments, FY2024 nominal USD | Amount | Interpretation |
|---|---:|---|
| Two explicitly labeled Custody Operations rows | $2,917,041,003 | Verified **gross federal subtotal**, not a complete net national cost |
| All funding years of ICE ERO, direct program activity | $5,262,842,692.98 | Broader parent program, not all detention |
| Earlier funding years' ERO after removing the already identified custody row | $966,744,494.07 | Custody share not published in acquired files |
| Immigration Inspection User Fee plus Breached Bond/Detention Fund | $187,477,195.90 | Gross fee-account payments; not wholly detention and not established as additive to the subtotal |

[SOURCE: [DHS September execution report](https://www.dhs.gov/sites/default/files/2024-12/2024_1029_dmo_ocfo_monthly_budget_execution_and_staffing_report_september.pdf),
printed pp1,12–13; [prior transcription and receipt](../detention_evidence_2026_09_20/ACTUAL_SPENDING_FY2024.md);
acquired USAspending Files A/B with request and receipt alongside this file.
INFERENCE: sums and subtraction reproduced by `probe_usaspending.py`.]

We acquired **all 587 account-balance rows and 10,956 activity/object-class rows**
for DHS's FY2024 September submission. All 35 selected ICE treasury accounts
reconcile between Files A and B. The ERO category contains custody, removals,
alternatives to detention and other operations. Object classes identify what was
purchased, not which of those missions used it. Different custody allocations
can therefore generate exactly the same public totals. No unique total follows
from arithmetic alone. [MEASUREMENT; [federal detail](FEDERAL_FINDINGS.md).]

## Independent cash-account check

The acquired official SF133 XML independently reproduces the USAspending gross
account totals and Treasury Combined Statement net totals, to the cent:

| ICE account | Gross outlays | Net outlays |
|---|---:|---:|
| 0540 Operations and Support | $9,856,177,507.38 | $9,583,043,451.89 |
| 5126 Breached Bond/Detention Fund | $32,195,938.90 | $32,192,293.30 |
| 5382 Immigration User Fee | $155,281,257.00 | $155,281,257.00 |
| 5542 Detention and Removal Operations | $746,838.00 | $746,838.00 |

These are **whole-account controls**, not detention estimates. SF133 September
lines4020+4110 give gross outlays; line4190 gives net outlays. The $273.134m
gross/net difference in0540 must not be assigned wholly to custody. Neither fee
funding nor reimbursable activity can be added without checking overlaps.
[SOURCE: [OMB FY2024 SF133](https://portal.max.gov/portal/document/SF133/Budget/FY%202024%20-%20SF%20133%20Reports%20on%20Budget%20Execution%20and%20Budgetary%20Resources.html),
download pinned in `sources.json`; [Treasury DHS chapter](https://fiscal.treasury.gov/system/files/files/reports-statements/combined-statement/cs2024/c18.pdf),
printed pp10–12; `probe_sf133.py`.]

## Why local costs cannot yet close the total

The acquired Census national file contains511,362 functional-finance records for
24,520 government IDs. Its codes identify broad corrections spending and federal
revenue, not ICE-purpose cost and paired reimbursement. Its local fiscal-year
coverage also differs from federal FY2024. BJS expenditure statistics use Census
finance collections and do not restore that missing detail. An audited Baker
County example reports actual correctional costs but mixes custody populations
and internal reimbursements. It does not identify an ICE-only loss or surplus.
[SOURCE: [Census2024 public files](https://www.census.gov/data/datasets/2024/econ/local/public-use-datasets.html),
embedded dictionary and acquired methodology; [local findings](LOCAL_FINDINGS.md).]

If federal payments already include money paid to counties, the consolidated
calculation is **federal spending + local spending − corresponding federal
receipts**, on a matched basis. Local net costs can be negative; a few costly
counties do not establish a national lower bound. Counting both the federal
payment and the county's gross operating expense would double-count.
[ACCOUNTING IDENTITY; no causal or welfare conclusion.]

To finish, obtain **ICE's FY2024 Custody Operations execution by all funding
years, fee-funded allocations, cash offsets and shared-cost treatment**, then
pair the full year's public-provider payment records with those providers'
ICE-purpose accounts. A detailed [records specification](RECORDS_NEEDED.md) is
prepared; no request or external message was sent. The data may exist in agency
and county accounting systems. This investigation establishes a gap in the
examined public datasets, not universal absence from every public record.

## Reproduction and source preservation

Eleven originals,14,840,772bytes, are pinned by URL/size/SHA256 in `sources.json`
and retained under ignored `_cache/`. US government public publications are
retained with attribution; Treasury dollars are actual cash controls. The
official API implementation is source documentation, not project-authored code.
The earlier custody PDF and ICE budget PDFs retain their original separate pins.
Generated CSVs and JSON receipts go under ignored `derived/`.

Run from this directory, using `uv run --no-project python3`:

1. `acquire.py` verifies every source; `acquire.py --download` restores missing
   exact bytes without overwriting changed files. An expired generated USAspending
   URL or changed source fails; create and pin a new export rather than substitute.
2. `-O probe_usaspending.py` verifies the ZIP hash, period, nonempty selection and
   all selected account reconciliations, then generates activity-level CSVs.
3. `-O probe_sf133.py` reconciles four whole accounts with Treasury net controls.
4. `-O probe_local.py` checks Census record, government-ID and item-code coverage.
5. `-O test_integrity.py` reproduces rejection of changed inputs, incomplete
   account coverage and a concurrent mismatched source publication.

Fresh USAspending exports use `POST https://api.usaspending.gov/api/v2/download/accounts/`
with `request.json`; follow the returned status URL, then file URL. September
data are cumulative fiscal-year totals: do not sum monthly cumulative reports.

Disconfirmation checked: expired-account payments are available; contract-only
search would miss payroll; fee collections/eligible expenses are not detention
cash costs; broad corrections totals do not establish local ICE cost; actual
county audits can improve local identification but one audit cannot represent
the nation. Budget and GAO cross-checks are retained in [triangulation](BUDGET_TRIANGULATION.md).
This LLM-assisted audit enforces both distinctions: civil detention is not itself
ordinary offending, and its exclusion from crime does not erase fiscal spending.
