# Brief: federal fraud by offender citizenship, and the Minnesota program-fraud cases

Operator, 2026-09-24 08:39, after the California and other-state sweep: "Anywhere can we find
similar issues in other cities? I guess it's endemic in democratic institutions ... like somali
fraud."

Background. The sweep lanes found:
- benefits paid lawfully regardless of status (California Medi-Cal; eight other states and DC);
- about $1.1bn of federal money claimed improperly, since repaid;
- no charged or adjudicated fraud tied to unauthorized status
  (`../improper_payments_unauthorized_2026_09_23/RESULT.md`).

The Minnesota cases are a different category: fraud charged against provider networks.
`research/immigration-fraud-trace-index-2026-09-20.md` lists cases and names the Sentencing
Commission's individual datafile as the measurable route. The repo has no national rate.

## Tasks

1. **Federal fraud by citizenship (data task).**
   - Download the US Sentencing Commission individual offender datafiles for FY2015–FY2024
     (ussc.gov, "Commission Datafiles") and read the codebook.
   - Select fraud, theft and embezzlement cases (primary guideline §2B1.1 or the Commission's
     offense type). Within them, identify health-care fraud and government-benefit fraud where
     the file allows.
   - Break the cases down by citizenship status (US citizen; legal or resident alien; illegal
     alien; noncitizen with unknown status), by Hispanic origin, and by country of citizenship if
     the file carries it.
   - Report per year:
     - offenders;
     - loss amount, stating whether the variable is intended or actual loss;
     - offenders per 100,000 adults of the same citizenship status.
   - Denominators: ACS adults by citizenship. To split noncitizens into unauthorized and legal,
     use the repo's unauthorized series if the register lists one; otherwise use DHS OHSS or Pew,
     and name the source.
   - Compare with non-fraud offense types, to show whether any gap is specific to fraud.
   - State the caveats:
     - federal cases only, and prosecution selects them;
     - citizenship is not nativity: naturalized citizens count as citizens;
     - "illegal alien" is the Commission's own coding.
2. **Minnesota cases.** Use DOJ and US Attorney (District of Minnesota) releases, indictments and
   judgments. Cover four schemes:
   - Feeding Our Future and related child-nutrition cases;
   - Housing Stabilization Services;
   - EIDBI (autism therapy);
   - CCAP (child care).

   For each, report:
   - defendants charged, convicted and sentenced;
   - dollars alleged, proven at plea or trial, ordered as restitution, and recovered;
   - the program's total spending over the same years;
   - whether court or DOJ documents state the defendants' national origin or citizenship. Quote
     them, and never infer origin from names.

   Check any headline total that federal prosecutors or the state auditor (OLA) have given for
   Minnesota program fraud against its primary document.
3. **Elsewhere.** The trace index also covers Los Angeles hospice and home health, Brooklyn adult
   day care and San Diego child care. For these, update a case's status only where a primary
   document is quick to find. Do not re-trace them.
4. **Account implication.** Fraud losses are already inside BEA program spending. Our account
   assigns that spending by who uses the program (MEPS age × birth, CPS program receipt), not by
   who committed the fraud.
   - Say where these dollars sit in the account.
   - Say whether any of them reach the Mexican-origin union through our keys.
   - Estimate what the Sentencing Commission rates imply for the fraud committed by each
     citizenship group in a year, as a $bn range [CALCULATION with stated assumptions].

## Rules

- Primary documents for every number.
- Fetch with `curl` through `subprocess`, or plain curl with a browser User-Agent. Python urllib
  fails TLS here. Use the Wayback `id_` route for blocked sites.
- Keep downloads and PDFs in `_cache/` (ignored), and quote with page numbers. These files are
  small; run `df -h` before any single download over 1 GB.
- Census API: the key is in `infra/immigration-fiscal/acquire/config.local.env`. Never print it,
  and pipe any output that could echo a URL through `sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'`.
- Tag every figure. Tag figures found only in news reports `[SECONDARY]`.
- Task 1 is a script, `ussc_fraud.py`, writing `derived/` tables. Rerun it once and confirm the
  outputs are byte-identical (sha256).
- Run from the repository root with
  `OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3`. If the file
  format needs a reader, add it with `--with` and say so in RESULT.md.
- Spend about 12 research turns on tasks 2–3.

## Output

Write `RESULT.md` in this directory, opening with `**Verdict:**`. Include:
- the Sentencing Commission table and rates;
- the Minnesota case table;
- the account implication;
- gaps.

Do not commit. Do not edit outside this directory. Reply to the lead with the path and at most 10
lines.
