# Brief: California's unauthorized residents and Medi-Cal in our own data

Operator, 2026-09-23 20:10, on a City Journal piece claiming California spends "more than $180
billion annually to food, health care, and other programs for the poor" and "at least $11 billion
subsidizing illegal immigrants in the last fiscal year": "Can you confirm this from the data we
have?" A sister lane (`../california_program_costs_2026_09_23/`) collects the state's own budget
figures. This lane answers from **local data**, and tests our own status imputation where
California breaks it.

## Why the status imputation matters here

`status_impute_2026_09_16/impute_status.py` classes a foreign-born person as legal if they receive
Medicaid (rule c; `use_medicaid_rule=True` by default). Since January 2024, Medi-Cal has covered
income-eligible Californians of all ages regardless of immigration status (children since 2016,
ages 19–25 since 2020, 50+ since May 2022). In California the Medicaid clause therefore moves
unauthorized Medi-Cal enrollees into the legal column. `parent_status_2026_09_23/parent_status.py`
already runs a `no_medicaid_rule` variant (ladder 185); reuse its approach, read-only.

## Tasks

1. **Counts.** On CPS ASEC 2025 (the account's file, income year 2024; coverage items as the
   status lane reads them), for California (GESTFIPS 6) and, for comparison, the rest of the US:
   - imputed unauthorized under the paper rules and under `no_medicaid_rule`, with replicate SEs;
   - among the `no_medicaid_rule` unauthorized in California, the number and share reporting
     Medicaid/Medi-Cal coverage, by age band (0–18, 19–25, 26–49, 50–64, 65+);
   - the same on ACS 2024 PUMS for California if the status rules can be applied there (say which
     rules cannot be, and why). ACS 2024 is local; see `research/immigration-dataset-register.md`.
2. **Benchmark.** Fetch DHCS's published count of full-scope Medi-Cal enrollees with
   unsatisfactory immigration status (UIS) for 2024–2025 (DHCS Medi-Cal eligibility statistics or
   the Local Assistance Estimate; `curl` via `subprocess`, into `_cache/`; quote with page or
   table). Compare with the survey count. Report what share of DHCS's UIS enrollees the survey
   captures under each rule, and how many the paper rules move into the legal column.
3. **Scale of spending.** From the Census Annual Survey of State and Local Government Finances
   (cached zips: `local_spending_composition_2026_09_18/_cache/indunit_YEAR.zip`; the 2024 local
   file per `detention_reconciliation_2026_09_20/LOCAL_FINDINGS.md`), give California's latest
   state+local expenditure on public welfare (cash assistance, vendor payments, other), health and
   hospitals, the US total, California's share and rank, and per resident. State which definition
   comes closest to "more than $180 billion ... for the poor".
4. **Implication for our work.** How many people does the Medicaid clause misclassify nationally
   (California plus other states that fund coverage regardless of status: IL, NY, OR, WA, DC and
   others; list only what you verify), and what that does to the status lane's 4.567M
   unauthorized in the Mexican-origin union. Do not re-run or edit other lanes; report the size.
   The status lane is an input to the audit's on-books rows, so give the count, not a $bn effect.

## Rules

- `OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 <script>` from the
  repository root. Never print the Census or IPUMS keys (`acquire/config.local.env`); pipe Census
  API output through `sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'`. Microdata stays in `_cache/`.
- Gate first: reproduce the status lane's published 4.567M union unauthorized (paper rules) and
  `parent_status`'s `no_medicaid_rule` Mexico-born 25–64 figure (4.778M) before any new number,
  and stop with `[BLOCKED]` if either fails.
- Tag every number `[DATA]`, `[CALCULATION]`, `[SOURCE: url, page]` or `[UNVERIFIED]`. Survey
  Medicaid reports are themselves imputed for about 23% of persons (see
  `cps_imputation_keys_2026_09_23/RESULT.md` step 2); say so where it matters.

## Output

`RESULT.md` in this directory opening with `**Verdict:**`, scripts, `derived/` tables and a
reproduce block. Do not commit; do not edit outside this directory. Reply to the lead with the path
and at most 10 lines.
