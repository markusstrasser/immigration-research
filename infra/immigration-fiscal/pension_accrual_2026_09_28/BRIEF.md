# Lane brief: the September 27 case with earned entitlements on an accrual basis

Date 2026-09-28, 07:50 JST. Parent session immigration-research-1c. The operator asked what we haven't thought about.
The adopted case ($321.82–387.37bn at specifications 48 / 11) is long-run on public capital: it charges an imputed
2–3% return because the stock scales with population. It is still cash on pensions, though.
- It credits the group's Social Security and Medicare hospital-insurance taxes in full, and charges only the
  benefits paid in 2024.
- The group is young (7.7% aged 65+, against about 18% nationally), so its 2024 work earns far more future benefit
  than it collects now.
- The 09-18 timing lane computed this for the union, but reported it only as a gap against whites
  (`lifetime_longevity_sstiming_2026_09_18/derived/ss_timing_group.csv`, row `mexican_observed_total`). There:
  - taxes are $2,998 per person ($122.6bn);
  - accrued benefits are 1.53 per tax dollar ($188.1bn), from SSA money's-worth ratios;
  - current benefits are $51.3bn;
  - a consistent cash-to-accrual switch therefore adds $136.9bn of cost.

  It was never carried to the absolute account. Price it on the adopted case, beside it, never in it. Adoption is
  the operator's call.

## Read first

- `lifetime_longevity_sstiming_2026_09_18/` (`ss_timing.py`, `derived/mwr_table.csv`, RESULT §2). Reuse its
  money's-worth machinery; reproduce the union's 1.53 and −$136.9bn as a gate before changing anything.
- `main_case_long_run_2026_09_27/` (`package.cjs`, `derived/corrections.json`). Do not edit it. The engine lines
  are `social_security`, `railroad_retirement` and `medicare` (spending), and the OASDI, HI and self-employment
  receipt lines.
- `research/immigration-objections-faq-2026-09-21.md` entries 3 and 10. Entry 10's aging composition exercise is
  a second route to the same question.

## Items

1. **OASDI on the adopted case.** The accrual charge is the present value of the benefits the group's 2024 covered
   work earns. It replaces 2024 benefit payments, which were accrued in earlier years. Arms:
   - scheduled benefits against payable benefits, using the 2025 Trustees' depletion date and payable ratio;
   - the discount rate: the Trustees' real rate, and 3%;
   - unauthorized workers (the repo's status imputation) accruing nothing, against a legalization probability you
     source;
   - SSA coverage scaling, as in the 09-18 lane.
2. **Medicare hospital insurance (Part A).** Part A is earned by 40 quarters of covered work, not in proportion to
   tax. Derive a per-worker-year accrual from a published present value of Part A benefits at 65 (Trustees or CBO)
   and the group's probability of qualifying. Parts B and D are financed from general revenue and premiums, so they
   stay cash. Say so.
3. **A cross-check without money's-worth ratios.** Reweight the group's 2024 cash balance to a steady-state age
   structure: its own stationary population from the Hispanic or Mexican-specific life table the 09-18 lane used,
   and the white age mix as FAQ entry 10 did. Report how close each comes to the accrual result, and why they
   differ.
4. **The case beside.** Report the adopted case at 48 and 11 with each arm. Give the decomposition (OASDI taxes,
   accrual, 2024 benefits removed, HI) and the central arm you would defend, with the reason.

## Rules

- Work only in this directory. Import upstream code; don't copy it. Gates:
  - reproduce the 09-18 union row;
  - reproduce `evaluateFull` at 48 and 11;
  - the package stays unchanged.
- Scripts write to `derived/`. Write `RESULT.md` first with `**Verdict:** pending` and append as you go. Two runs
  through `scripts/rerun_lane.py` must be byte-identical.
- Tag every number, and source every Trustees or CBO figure from the primary document, saved in `reads/`. No
  commits, staging or stash.
- Final message: the RESULT path and at most ten lines, giving the case at 48 / 11 under the central arm and the
  range across arms.
