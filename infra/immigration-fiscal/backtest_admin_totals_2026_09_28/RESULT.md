claude-opus-5-5

**Verdict:** pending

# Back-test: do the account's keys predict where administrative dollars land?

Lane opened 2026-09-28 from `BRIEF.md` (commit 78ca741). Pre-registered: phase 1 writes the predictions,
baselines and tolerances (`PREDICTIONS.md`, `derived/predictions.csv`) before any external figure is
opened; the parent commits them; phase 2 scores. Nothing outside this directory is edited. Nothing is
committed, staged or stashed.

## Log

- Phase 1 started. Blindness screen of the repo by file name and match counts only (no values read):
  - IRS SOI county files for tax years 2011–2022 sit in
    `causal_evidence_2026_09_20/raw/county_outcomes/raw/irs_soi/county/` and carry county EITC and ACTC;
    state sums for those years are therefore in the repo, unopened. California FTB CalEITC reports sit in
    `california_program_costs_2026_09_23/_cache/`, unopened.
  - No SSA state file is in the repo by name; `admin_transfer_checks_2026_09_19` holds national totals.
  - Several memos and lanes mention births to Mexican(-born) mothers and Medicaid-paid births
    (`demo_momentum_2026_09_16`, `ir5_fraud_and_cohorts_2026_09_27`, `external_benchmarks_2026_09_24`,
    the confidence ladder); unopened.
- Definitions read, numbers not: the SOI 2023 state data guide (AGI_STUB 0 = state total; A59660 is the whole
  EIC, A59720 its refundable part, A11070 the ACTC), the WONDER natality expanded help (mother's residence,
  Mexican origin, mother's birth country, five payer categories, 1–9 births suppressed) and SSA's table of
  contents. SSA's site refused scripted fetches; its contents page was read through a browser session.
- The prediction was first built on the builder's published keys with the audit's paper rule at 0.60. The
  adopted case keys these lines with the CPS lane's stack instead (audit row 4's weights, the state-aware flag,
  the on-books lane's origin shares; `main_case_2026_09_24/package.cjs`), so the prediction now rebuilds that
  stack before its fill-in step with the lane's own functions. The earlier reading stays as the "published"
  secondary. The change matters: the state-aware flag moves California's predicted credit share from 11.30% to
  10.12%, and the no-rule baseline now sits 0.185 in δ from the prediction instead of 0.074
  [DATA: derived/predictions.csv, derived/power.csv].
- Gates: builder keys 9.7e-17, paper rule 1.4e-15, stored stack cells of the four lines reproduced with a
  0.0 bn gap [DATA: derived/prediction_audit.json].
- Scoring frozen in `estimators.py` before any administrative figure: δ's standard error is the larger of the
  replicate and HC3 terms (the first draft added a HC1 term to the replicate term, which counts sampling error
  twice). A synthetic check on the frame's own replicates finds the estimator unbiased, 96–98% coverage and a
  3–4% false-miss rate [DATA: derived/estimator_check.csv].
- Power before looking: credits powered by sampling only just (sampling SE 0.103 / 0.106 against τ 0.113 /
  0.122); SSI powered (0.331 / 0.335 against 0.414 / 0.415) but coarse; Social Security declared no power;
  births of Mexican-origin mothers powered for the national share and the six-cell distribution of children
  0–2; Mexico-born mothers declared no power; the Medicaid group share powered (relative SE 3.4% against 10%)
  [DATA: derived/power.csv].
- Predictions, baselines, tolerances and the phase 2 procedure: `PREDICTIONS.md`. Frozen for the parent's commit.
