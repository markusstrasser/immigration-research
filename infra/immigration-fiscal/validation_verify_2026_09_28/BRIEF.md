# Lane brief: reproduce and check the validation memo's claims

Date 2026-09-28, 03:40 JST. Parent session immigration-research-1c. Operator, on the updated
`research/immigration-validation-and-backtesting-2026-09-28.md` (af2d01b): "parallelize .. if true".
Another session wrote the memo and its five lanes (df05631). This lane checks them. Do not edit them.

## Tasks

1. Rerun each lane with `scripts/rerun_lane.py`, using the reproduction commands in its README or RESULT:
   `validation_audit_2026_09_28`, `validation_schools_2026_09_28`, `validation_medical_2026_09_28`,
   `validation_fiscal_years_2026_09_28` and `validation_mariel_2026_09_28`. Run their tests too. Record rc,
   IDENTICAL or DIFFERS, and any NOT RUN script.
2. Put every number in the memo's verdict and sections 1–3 in a table: memo value, lane value (file and column),
   match or mismatch. Cover at least:
   - GSS 4.59 / 2.80 / 3.39 against 5.67 / 5.16 / 9.24, and 3.29 against 2.72;
   - SNAP MAE 5.16 → 5.69 and RMSE 8.13 → 8.79;
   - schools .182 / .202 / .169 / .175, $5.86m / $7.09m, −3.46% / +5.50% / +1.99%, and 46 of 51;
   - medical 1.114 / 1.009 / .106 (.186), .420 (.177), 85.1%, .374 / .411 / .293, and −.074 against −.202;
   - fiscal years .495 → .415, 25.20 / 2.43 / 24.06, and 4.77pp / $90.86bn;
   - Mariel 39.75% / 26.65% against 16.02%;
   - the section 1 table.
3. Check each test's construct, not just its arithmetic:
   - Was the baseline fixed before scoring? Do training and test years overlap?
   - Is each score on the unit the memo names (pupil-weighted or unweighted; dollars or logs)?
   - Does the medical 2022 comparison use the same populations as 2023?
   - Is "corroborates" in `external_benchmarks_2026_09_24/benchmarks.py:27–35` the materiality rule the memo
     describes?
4. List any memo claim that goes beyond what the lanes compute.

## Rules

- Write `RESULT.md` first with `**Verdict:** pending`, and append as you go. Write only inside this directory.
- No commits, staging or stash.
- Final message: the RESULT path and at most ten lines. Name every mismatch.
