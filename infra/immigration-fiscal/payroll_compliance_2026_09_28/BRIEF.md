# Lane brief: do the group's credited payroll and income taxes assume full compliance?

Date 2026-09-28, 07:10 JST. Parent session immigration-research-1c. The operator said "ok do" to a receipt-side
red team of the adopted September 27 case ($321.82–387.37bn at specifications 48 / 11). This lane takes one
question from it, which runs against the other receipt items: are taxes credited to the group on pay that never
reaches a payroll or a tax return? Adoption is the operator's call. Build candidate items, never a new case.

## What the case credits (shared allocation, CBO rules; check at 48 and 11)

| Line | Key | Share | On the group ($bn) |
|---|---|---:|---:|
| employee and employer OASDI | `wage_oasdi` | 9.50% | 57.97 + 58.47 |
| employee and employer HI | `wage` | 8.78% | 17.28 + 15.37 |
| self-employment OASDI/HI | `self_payroll` | 10.68% | 9.27 |
| other domestic social contributions | `positive_fica_worker` | 12.10% | 11.30 |
| federal income tax | `federal_liability` | 5.74% | 137.94 |
| state and local income tax | `state_liability` | 5.37% | 28.78 |

National totals are BEA collections, so they already net out non-compliance. The group's share comes from survey
records. A survey that records cash pay the IRS never sees gives the group too large a share of taxes that were
actually collected. The correction is then a reallocation within fixed national totals.

## Read first

- `full_account_receipts_2026_09_20/builder.py` and its README: which survey (CPS ASEC or ACS, and which year) and
  which tax model build each key above, and whether FICA and income tax are imputed on all reported earnings.
- `tax_key_heldout_2026_09_28/RESULT.md` (ladder 249). It tested the income-tax gradient against IRS data by
  income, not compliance by group.
- `compliance_gap_2026_09_24/RESULT.md` (ladder 220) and `decisions/2026-09-25-weekly-audit-corrections.md`. The
  lane found $30–64bn of off-books pay in construction, landscaping, janitorial work and restaurants (central
  $37bn; a level check allows zero). The Mexico-born carry half, with $2.3bn of payroll tax. It called that tax
  "already inside the account" because national totals are collections. That holds for the total. It is
  untested for the allocation: a key built on survey wages that include cash pay credits the group with tax that
  other residents paid. Reuse its slopes and cells; don't redo them.
- `ledger_underreport_2026_09_16` covers benefit under-reporting, not taxes. It is context only.
- `main_case_long_run_2026_09_27/` (`package.cjs`, `derived/corrections.json`) and
  `receipt_long_run_probe_2026_09_28/probe.cjs` for the replica gate. Do not edit either.

## Items

1. **Trace the keys.** For each line above, state the source, the earnings concept, the tax model, and whether the
   earnings are self-reported or matched to records. Include how unauthorized workers enter the survey, and the
   weight or imputation that adds them. Then settle whether "already inside the account" holds for the group's
   share, line by line.
2. **Measure compliance by group from primary sources.** Candidates:
   - SSA Office of the Chief Actuary actuarial notes on unauthorized workers with and without payroll-tax records;
   - the Earnings Suspense File;
   - IRS tax-gap and National Research Program estimates of employment and self-employment tax misreporting, by
     industry where available;
   - CPS or SIPP records matched to SSA or IRS earnings, by nativity or Hispanic origin;
   - ITIN filing counts.

   The group is mostly US-born, so the gap should sit mainly in its unauthorized first generation and its
   self-employed. Size each part and say which parts are measured and which assumed.
3. **Price it.** Move the non-compliant part of each line from the group to other residents within the national
   total, as `applyCorrections` does. Report each line alone at 48 and 11, then all together, with a range from
   the evidence.
4. **The other direction.** List anything the account misses that the group pays: payroll tax on Earnings
   Suspense File wages that the benefit keys never pay back, and sales or excise tax on cash income. Say whether
   each one is already in a key.

## Probe and rules

- Load the adopted package unchanged. Reproduce `evaluateFull` at 48 and 11 with both fill-in methods averaged
  (gate), then apply the payload.
- Re-keys hold national totals (gate). The 64 specifications hold 32 distinct ones.
- Work only in this directory. Scripts write to `derived/`. Write `RESULT.md` first with `**Verdict:** pending`
  and append as you go.
- Two runs through `scripts/rerun_lane.py` must be byte-identical.
- Never print the Census API key. Pipe Census output through a redaction filter.
- Tag every claim `[SOURCE]`, `[DATA]`, `[CALCULATION]` or `[INFERENCE]`. No commits, staging or stash.
- Final message: the RESULT path and at most ten lines, giving old → new at 48 / 11 for every item.
