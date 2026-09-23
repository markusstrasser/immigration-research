# Brief: how much unauthorized work is on the books (audit row 2)

Owner: `onbooks-share` agent. Write only inside `infra/immigration-fiscal/onbooks_share_2026_09_23/`.
Do not commit; the parent grades and commits. Result file: `RESULT.md`, first line
`**Verdict:** …`.

## Why

The account's receipt keys and its refundable-credit key come from the Census CPS ASEC tax model:
- receipts: federal and state liability, capped and uncapped wages, FICA workers;
- refundable credits: EITC plus the additional child tax credit.

That model assumes every respondent is a resident filer who complies fully. The dataset integrity
audit (`dataset_integrity_2026_09_23/cps.md` row 1; script `cps_status_keys.py`) re-keys these with
the status lane's rules. It zeroes EITC for the Latin-American-born imputed as unauthorized and
scales their other taxes and wages to an on-books share. On the main case ($203.2–249.6bn):

| On-books share | Effect |
|---|---|
| 44% (SSA's 2010 estimate, Actuarial Note 151) | +$15.2–17.0bn |
| 60% | +$9.9–11.3bn |
| 75% | +$5.0–6.0bn |

The share is the only unknown. The audit's central uses 60% without evidence for it.

## Question

In 2022–2025, what share of unauthorized immigrants' earnings (Mexico-born, if any source splits
it) is reported on W-2 payroll? What share of unauthorized households file federal income tax
returns (with ITINs or SSNs)? What is row 2 at the evidence-weighted share?

## Sources to find and read

Use primary sources. Quote each number with its page; grade each by year, population, method and
whether it is Mexico-specific.
- SSA Office of the Chief Actuary: Actuarial Note 151 (2013) and any later note on other-than-LPR
  immigrants. Also the Trustees Report assumptions on the "other-than-LPR" population's covered
  earnings, and OCACT letters (for example on DACA or immigration bills) that state an on-books
  fraction.
- SSA Earnings Suspense File statistics and the OIG, GAO and TIGTA reports on the ESF, ITIN
  filers and mismatched W-2s (2015–2025).
- ITEP 2024, *Tax Payments by Undocumented Immigrants*: its payroll and income-tax compliance
  assumptions and their source.
- CBO 2024 and 2025 on the immigration surge: the share of the surge population with on-books
  earnings. Also CBO's older unauthorized-population assumptions.
- NAS 2017 (*The Economic and Fiscal Consequences of Immigration*), chapter 8 assumptions; Pew,
  MPI, CMS or NBER work on unauthorized workers in payroll data. Examples: Borjas (2017) on the
  unauthorized in the CPS; Orrenius and Zavodny; E-Verify state-mandate papers that report shifts
  into informal work.

## Method

1. Build the source table and form an evidence-weighted central share and a range for 2024.
   Disconfirmation is mandatory: look for sources that put the share above 75% or below 44%.
2. Read `dataset_integrity_2026_09_23/cps_status_keys.py` and find how it takes the on-books share.
   Compute row 2 at your central and range. Rerun at 0.44, 0.60 and 0.75 first, as a gate against
   the audit's table.
3. State whether survey under-reporting of these workers' earnings, which the audit left
   unmeasured, pushes the other way, and by how much if a source quantifies it.

## Output

`RESULT.md` should open with the verdict: the share, the range, row 2 in $bn, and the evidence
level. Follow it with:
- the source table;
- the gate;
- the computation;
- disconfirmation.

Put scripts, if any, in the lane directory and outputs in `derived/`. Tag claims `[SOURCE: …]`,
`[CALCULATION: …]` or `[INFERENCE]`.

## Constraints

- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project [--with pkg] python3 <script>` from
  the repository root.
- No edits outside this directory.
- Never print keys.
- Stop after about 12 turns of search and report what you have.
