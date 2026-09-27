# Lane brief: do subsets of the account reproduce what others published? (pre-registered)

Date 2026-09-28, 07:40 JST. Parent session immigration-research-1c. The operator asked for links "where our stuff
predicts some other reality", a subset that "shows up in some news headline or other papers". Earlier lanes already
compared the account with CBO's and Treasury's distributions, ITEP and SSA on unauthorized taxes, the Florida and
Texas hospital reports (`external_benchmarks_2026_09_24`), California's Medi-Cal counts and budget
(`california_medical_status_2026_09_23`, `california_program_costs_2026_09_23`) and NYC's shelter costs. Banxico's
remittances are an input to the consumption key, so they cannot test it. This lane adds three comparisons those
lanes did not make.

## Protocol: predict, freeze, then look

1. **Phase 1, predict.** Compute each prediction from the adopted September 27 account and its frame (CPS ASEC 2025
   and the key microdata). Write `derived/predictions.csv` and `PREDICTIONS.md`. Each check gets:
   - the account's prediction, on the other source's definitions;
   - a naive baseline;
   - the tolerance you declare now, allowing for definitional gaps you can name;
   - what a miss would mean.

   Read each source's methodology to match definitions, but not its results. If a result is already in the repo
   or you know it, mark that check "not blind".
2. **Freeze.** Message the parent "predictions frozen", with the file paths, and stop. The parent commits them.
3. **Phase 2, score.** Only after the parent says go: fetch the primary documents (hashes in `derived/sources.json`,
   quotes in `reads/`), score against the declared tolerances, and explain every gap by named definitional
   differences, or say that it is unexplained.

## Checks

1. **American Immigration Council, "New Americans" (Mexican immigrants).**
   - AIC publishes, by country of birth, taxes paid (federal, and state and local) and spending power, from the ACS
     with ITEP's tax rates.
   - Predict the same quantities for the Mexico-born from the account's frame on AIC's definitions: which taxes,
     whether the employer's payroll share is included, and the year.
   - This is an independent build of a subset of our receipts side.
2. **National Academies 2017, Table 8-1 (not blind).**
   - Its first generation and their dependents have receipts and outlays per capita at 0.79 and 0.90 of the
     all-group average (2013), as the external-benchmarks lane already read.
   - Compute the account's ratios on the same construction: all foreign-born and their dependents if the frame and
     keys allow, and the Mexico-born and dependents in any case.
   - Report where the method agrees and which conventions (public goods, interest, incidence) explain any gap.
3. **Hospital uncompensated care by state (CMS HCRIS, Worksheet S-10).**
   - Target: total uncompensated care cost by state from the latest complete cost-report year.
   - Prediction: the account's uncompensated-care key applied by state (the group's and others' uninsured use
     rates times each state's uninsured counts), scaled to the national S-10 total.
   - Baseline: each state's share of the uninsured.
   - Report the slope of the error on the group's share of each state's uninsured. Name Medicaid expansion as a
     confounder and show the fit with and without an expansion indicator.

## Rules

- A new lane in this directory. Import the builders, don't copy them. Gate: every national share you use reproduces
  the adopted key to 1e-9.
- Scripts write to `derived/`; raw pulls go in `_cache/`. Two runs through `scripts/rerun_lane.py` must be
  byte-identical.
- Never print the Census API key. Tag every number. No commits, staging or stash.
- Final message (after Phase 2): the RESULT path and at most ten lines, one per check: hit, miss or no power, with
  the gap and its explanation.
