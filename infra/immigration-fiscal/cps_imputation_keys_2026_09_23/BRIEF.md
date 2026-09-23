# CPS ASEC imputation: how much of the group's taxes and benefits are Census Bureau fill-ins?

Date: 2026-09-23. Operator: "Any other in our analysis we could get a better answer on (not
rounding errors but actual bigger conceptual wrongtakes?)"

## Why

Today's crime lane found that the 2000 census filled in a missing birthplace for 68% of
institutionalized Mexican-origin men, and made 98% of them US-born
(`crime_selection_cohorts_2026_09_23`, ladder 196).

The complete account's receipt and benefit keys come from CPS ASEC 2025
(`gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip`, read by
`full_account_receipts_2026_09_20/builder.py` and `full_account_benefits_2026_09_20/builder.py`).
The ASEC fills in missing income and benefit amounts by hot deck, and whole supplements for
nonrespondents. If donors are not matched on Hispanic origin or birthplace, imputed
Mexican-origin incomes drift toward other people's (Bollinger and Hirsch's "match bias"). That
would overstate the group's taxes. Imputation and underreporting of benefits could push the other
way.

No lane has tested this. The account's standard error of about $12bn (ladder 184) covers
sampling only.

## Task

1. **Flags.** From the ASEC 2025 record layout and technical documentation
   (`sources/immigration-fiscal/data/external/cps_asec_doc/`), list the allocation or imputation
   flag for every income and benefit item the account uses, plus the whole-supplement imputation
   flag. The items: earnings, self-employment, property income, Social Security, SSI, public
   assistance, SNAP, housing, school lunch, Medicaid and Medicare coverage, and EITC inputs. Quote
   the documentation on the hot deck's match variables. State plainly whether Hispanic origin or
   nativity is one of them, quoting the source or marking it `[UNVERIFIED]`.
2. **Shares imputed**, by item, for the union (the account's 40,896,574 definition) and for other
   residents. Weighted, with replicate-weight SEs.
3. **Match bias test.** Within cells of the documented match variables, compare reported and
   imputed amounts for the union and for others. Does the union's imputed mean sit closer to
   others' than its reported mean does?
4. **Recompute the union's receipts and benefits** two ways:
   - (a) Drop imputed items and reweight reported records by inverse probability within
     age × sex × education × nativity × union cells.
   - (b) Re-impute the imputed items from union donors matched on the documented variables plus
     union membership and nativity. Use a simple sequential hot deck and state the seed and the
     cell-collapse rule.

   Run the account's own incidence code where possible. Otherwise reproduce its keys and gate them
   on its published numbers (`full_account_receipts_2026_09_20/derived/scenario_totals.csv`,
   `full_account_benefits_2026_09_20/derived/`) before perturbing anything.
5. **Translate into the main case.** Report the change in the union's receipts, benefits and net,
   in $bn with replicate SEs, and whether it moves the adopted $203.2–249.6bn
   (`main_case_2026_09_23`). If the income-distribution lane (`distribution_weights_2026_09_23`)
   uses the same keys, report how its quintile inputs change.
6. **Disconfirmation.** Make the case that imputation makes no difference, for example because
   the match variables absorb the gap, and say what would show it.

## Rules

- Do not edit fingerprinted `.py` files in `gen_ledger_extension_2026_09_16` or
  `ledger_absolute_2026_09_17`. Copy the logic into the lane instead.
- **Deliverables.** A `RESULT.md` that opens with `**Verdict:**` and contains:
  - flags, shares and the match-bias table;
  - both recomputations, with gates;
  - the main-case translation;
  - every specification computed;
  - limits.
- Commit scripts and `derived/*.csv` aggregates only. No microdata; raw files go in `_cache/`
  (add a `.gitignore` with `_cache/`).
- Run with `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` from the repo root.
- Write only in the lane directory. Do not commit.
