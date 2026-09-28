# Brief: net the pension accrual of income tax on benefits (2026-09-28, parent)

## Why

The cross-lab review of this lane (GPT-6 Astra, xhigh) flagged that the accrual values benefits before income tax on
them. The parent confirmed it at the source. SSA Note 2025.7, footnote 2: "money's worth ratios that ignore these
transfers may arguably be overstated. Due to the difficulty of determining the level of income tax on benefits, this
factor is not addressed in this note." The lane's own national check already has the national path. Nationally the
tax returns 10.1% of the future OASDI benefits of today's 15–61: 5.85% to OASDI, and HI gets 0.722 times OASDI's
share (`derived/national_score.json` `stock_check.tob_share_15_61`; `derived/national_prediction.json`
`kappa_hi_over_oasdi_tob`). The RESULT section "Corrections after the cross-lab review" (commit 8062db1) estimates
−$4.5bn to −$9bn at spec 48 without measuring anything. Measure it.

## What to build (in this lane; the parent owns commits)

1. **Current tax on the group's 2024 benefits.** The case's income-tax receipts come from the Census tax model's
   `FEDTAX_BC` (`full_account_receipts_2026_09_20/builder.py` line 95), which taxes Social Security benefits under
   the usual rules. Measure the part attributable to benefits: federal income tax with and without the tax unit's
   Social Security benefits, for the group's tax units and for all tax units. Reuse the existing Tax-Calculator
   pipeline (`tax_rerun_acs_2026_09_17/`, `taxcalc==6.8.2`, `taxcalc_io.py` and `cps_tax.py`). Alternatively use the
   simplified difference operator `cps_imputation_keys_2026_09_23/taxcalc.py`, but only if it models taxable Social
   Security; it may not. Report:
   - the group's and the nation's benefit tax in $bn;
   - each as a share of their benefits;
   - the group's rate relative to the nation's.

   State taxes on benefits are out of scope unless a state line in the case plainly carries them; say which.
2. **Future tax on the benefits the group's 2024 work earns.** Apply the national year-by-year tax-on-benefits
   share (OASDI plus HI; `national_check.py` builds `paths.tob_share` from TR Tables IV.B1/IV.B2, and HI takes
   `kappa`) to the timing of the group's accrued benefits. Scale it by the group's relative rate from step 1, held
   constant over time, and weight it by benefit present value, as `window_grid` does. Report the PV share for the
   group and by generation.
3. **Net switch.**
   - Net OASDI accrual = gross accrual × (1 − that share).
   - Under the switch, drop the current benefit tax from receipts, since cash benefits leave the account.
   - Report the case on accrual at 48 / 11 for the central and every arm. Keep the gross central as a named arm,
     `gross_of_benefit_tax`.
   - Part A benefits are not taxed, so leave Part A alone.

   In `derived/summary.json`, keep every existing key. Add:
   - `benefit_tax.future_share_group`;
   - `benefit_tax.current_receipt_bn` (by spec end);
   - `ratio_net`;
   - `case_on_accrual_net_bn`.

   Decide with the parent (SendMessage) before changing what the existing `ratio` key means. Candidate v3 reads
   `ratio` and `part_a_accrual_bn` through `git show` at a pinned commit.
4. **Time-boxed (≤ 45 min of work, skip if it does not fit): spouses' own records.** The central prices a worker
   whose spouse has no 2024 covered earnings as a one-earner couple. The bounds are the central's 1.298 per tax
   dollar and 1.186 with every such couple priced as two-earner. Find the share of those spouses who have their own
   work history, using ACS 2024 PUMS `WKL` (when last worked) by age and sex, or CPS ASEC if it carries a usable
   field. Say whether that share supports a point between the bounds. Report it as an arm; do not move the central.

## Gates and validation (exact)

- The existing gates in `pension_accrual.py` and `national_check.py` still pass. `derived/national_prediction.csv`
  keeps its frozen sha256; `national_check.py` checks this.
- With the share set to 0, the net central reproduces today's central ($437.828882bn / $497.775764bn at 48 / 11) to
  1e-6.
- The benefit-tax computation reproduces the Census `FEDTAX_BC` total for the tested units, with benefits in, within
  the tolerance the tax-rerun lane documents. Report the gap.
- The national benefit tax from step 1, as a share of national benefits, should sit near 2024's national
  tax-on-benefits income over OASDI cost. That is about 6.4%: OASDI $55.1bn plus HI $39.8bn, over cost. Read the
  exact figures from TR 2025 in `_cache/tr2025.txt`. A miss over 25% is a finding to report, not a failure to hide.
- Reproduce from the repository root:
  `uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/pension_accrual_2026_09_28 "node {lane}/case_lines.cjs" "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/pension_accrual.py" "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/national_check.py" --allow-unrun infra/immigration-fiscal/pension_accrual_2026_09_28/lifetime_model.py --allow-unrun infra/immigration-fiscal/pension_accrual_2026_09_28/sources.py`
  - Add any new script to that command.
  - Two consecutive passes must print IDENTICAL.
  - Quote `"pandas>=2"` in any `--with`, because commands run under /bin/sh.

## Rules

- Files you own:
  - this lane's scripts, `derived/`, and RESULT.md, but only in a new section "Net of income tax on benefits"
    plus Progress lines;
  - a new script if you want one.
- Do not edit other lanes. Read them only.
- Never print the Census API key. Do not read `acquire/config.local.env` unless a Census call is unavoidable. If
  one is, pipe the output through a redaction filter.
- Tag every number: [SOURCE], [DATA], [CALCULATION] or [INFERENCE]. Times in the Progress log come from `date`.
- Do not commit, stage or stash. When done, update the RESULT verdict paragraph with the net figures. SendMessage
  the parent a ≤10-line summary: the net central at 48 / 11, the current and future shares, and the gate results.
