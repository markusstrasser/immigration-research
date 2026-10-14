**Verdict:** Use M1 as a **conditional arm**, not an observed measurement correction. The ordinary federal survivor correction is **+$6.723962bn**, SE **$3.570733bn**, at both central ends and in set/cash. Recomputing the separate `federal_gap_high_agi` arm gives **+$5.169874bn**, SE **$2.689663bn**; scalar transport would overstate it by **$1.051190bn** (difference SE **$1.511804bn**). Adopt the lane-local EITC formula repair as a code correction; the survivor TAXSIM kernel already passes the corrected formula's primary-source regression. [CALCULATION: `tax_corrections.py --run`; `derived/tax_corrections_results.csv`]

Covered: survivor own factors and IRS cells, federal high-AGI recomputation, EITC primary validation and local callable repair, validation of existing M2. Skipped: member-child membership, M4/M5, added-people transport, pension accrual and unified accounting, owned by peers. No upstream source or git metadata was changed.

## Tax results

| Net-cost correction against central union, $bn | G1 | G2 | G3+ | All | All replicate SE |
|---|---:|---:|---:|---:|---:|
| M1, ordinary IRS benchmark | −0.233367 | +1.317403 | +5.639926 | +6.723962 | 3.570733 |
| M3, refundable credits | +0.379708 | −0.585569 | −0.594603 | −0.800464 | 0.186546 |
| M1, high-AGI residual arm | −0.157966 | +1.998403 | +3.329438 | +5.169874 | 2.689663 |
| Recomputed high-AGI minus scalar approximation | +0.057946 | +0.779531 | −1.888667 | −1.051190 | 1.511804 |

The main-case evaluated endpoints, specification 16/11 in both set and cash, use `federal_liability`, response 1. Thus the high-AGI result is an arm beside central, not a reason to scale either central end by 0.925208. All 161 columns are written in `derived/tax_corrections_replicates.csv`; use the vectors, not SE quadrature, when constructing a stack. Numbers here use the original round-1 membership. A driver changing membership must call the hook again on its canonical survivor registry. [DATA: `derived/case_inputs.json`, `evaluated`; CALCULATION: `run`, `federal_high_agi`]

## Exact high-AGI rule

The authoritative receipts builder's arm is observed national CPS liability **$1,977.915739bn** plus the positive residual to the **$2,403.242bn** national line, **$425.326261bn**. Its liability part uses the on-books-adjusted liability share; its residual part retains the adopted unadjusted `FEDTAX_BC * (AGI >= 500000)` share. The original national pools are held; the numerator and denominator of each key use the same row-4 replicate. [DATA: `full_account_receipts_2026_09_20/builder.py`, `conditional_rows`; `cps_imputation_keys_2026_09_23/combine_onbooks_lane.py`, `row3_partition`, `row3_deltas`; CALCULATION: `derived/tax_corrections_audit.json`]

Both before and after survivor flows are recomputed on the same canonical return as M1. The low-level arm adds **$6.665637bn** from liability and **$0.146476bn** from high-AGI residual, then subtracts the already-booked item-5b receipt adjustment **$1.642238bn** exactly once. Only that ledger subtraction uses the frozen item's recorded scenario scale 0.925207989647569. It is never used to approximate the survivor response. Generation closure is below **$6.4e−12bn**. [CALCULATION: `high_agi_delta`; `derived/tax_corrections_audit.json`]

Continuing unchanged claimants retain their reported AGI residual, just as their Census liability residual is retained. Mixed spouses filing anew and newly created claimant returns use their own kernel AGI. Applying raw kernel AGI to all continuing claimants spuriously moves unaffected returns across $500,000; the generation-closure gate caught an **$11.144785bn** unowned difference. The hook fixes this class by preserving original AGI on all anchored continuing returns. [CALCULATION: `federal_high_agi`]

The current ordinary M1 code already uses `flag[own]`, `onbooks[own]`, survivor own weights, their own IRS AGI bin and the remaining household's CBO cell. Its surviving-tax and IRS-cell head/spouse-swap checks pass at 1e−9. The IRS multipliers remain benchmark weights, not marginal tax rates; statutory tax response, unobserved deductions and earnings classifications remain conditional. [DATA: `removal.py`, `federal_removal`, `survivor_irs_cells`]

## EITC

`cps_imputation_keys_2026_09_23/taxcalc.py` has the confirmed defect: it subtracts phase-out from phase-in. The legal amount is the smaller of phase-in and **maximum credit less phase-out**, floored at zero. `corrected_eitc` implements this; `install_eitc_fix(module)` repairs the frozen module in memory for any lane-local caller, preserving its tax and ACTC results and source bytes. The control lane's `credits.eitc` already has the correct formula. The actual survivor code uses pinned local NBER TAXSIM, whose EITC also passes. [DATA: cited Python functions; SOURCE: [IRS Publication 596 (2024)](https://www.irs.gov/pub/irs-prior/p596--2024.pdf)]

The pinned primary PDF was converted with `pdftotext -layout`. The parser retains PDF page and source row for **10,688** numeric filing-status/child-count/income cells, including one-sided final table rows. Eight starred terminal cells refer to within-interval footnotes; their complete rows and footnotes remain in the pinned PDF/text, and they are excluded explicitly from the constant-cell regression. The formula constants are inherited from the frozen tax code, then independently checked against this parsed primary table. Continuous-schedule values match numeric table midpoints within $0.51 except intervals straddling a statutory kink, separately bounded at $5.50 and tested. The low-earnings/high-AGI fixture gives **$1,708.50** in TAXSIM versus the IRS table's **$1,709**; the defective formula is more than $300 too low. `assert_eitc_used(tax_module)` makes that actual-kernel check callable and fail-loud. [DATA: `inputs/tax_corrections_pins.json`, `tax_corrections_eitc_table_2024.csv`; CALCULATION: `test_tax_corrections.py`]

## State M2 and recommendations

The existing shared canonical state result is **+$0.850817bn**, SE **$0.580743bn**; its mixed-couple-only standalone result is **+$0.722380bn**, SE **$0.579778bn**. The former also recalculates continuing returns' changed dependents and child-care interactions. Both exceed the rough +$0.3–0.5bn guess but remain below $1bn. This follows state-specific statutory refiling, own survivor factors/weights and state/replicate calibration, rather than flat-scaling the $536.167bn line's 5% key. Recommend **arm**: transporting calibration across refiling and unobserved state deductions remains assumed. The existing eleven state tests passed, including survivor symmetry, own weights/status factors, source-derived California brackets, and shared-care forwarding. [DATA: `derived/results.csv`, `state_sensitivity.json`; CALCULATION: `test_state_tax.py`; SOURCE: pinned local NBER TAXSIM documentation]

- **Adopt as measurement/code correction:** survivor own flags and IRS cells; fixed EITC formula when the simplified operator is used; exact subtraction of booked item; keeping unchanged claimant AGI fixed.
- **Arm:** M1/M3 statutory survivor liability/credits; high-AGI residual recomputation; M2 state response. Report both ends and both sets using their actual receipt scenario.
- **Reject:** scalar multiplication of the survivor tax correction to obtain high-AGI residual; original-head factors or joint IRS cells applied to the survivor; kernel-only AGI drift on unchanged continuing claimants.

## Integration and checks

```python
taxfix = load_module(LANE / 'tax_corrections.py', 'removal_tax_corrections')
eitc_gate = taxfix.assert_eitc_used(tax)
high = taxfix.federal_high_agi(c, x, d, federal, removal_module=current_removal_module)
# high['M1_high_agi']: 3 x 161 vector; beside central M1
# high['after_agi']: shared survivor AGI with anchored residual preserved
```

`after_output=` can reuse the already-computed canonical TAXSIM output and avoid one subprocess. The hook consumes the driver's `after_input`, `after_federal`, `afterR`, `own`, `owner`; it does not rebuild membership or care inputs. `install_eitc_fix` is available only for a caller of frozen simplified `taxcalc.compute`; it is unnecessary for the correct NBER survivor kernel. [DATA: function contracts]

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 tax_corrections.py --run
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest test_tax_corrections.py test_state_tax.py -q
```

Run from the lane for these commands or use full lane-relative paths. The tax run preserves original positive controls byte-for-byte, including all 83 original gates. Nine owned tests and eleven state tests pass. The final complete helper run took **64.25s**, peak self RSS **0.961GB**, child RSS **9.62MB** using `time.perf_counter` and `resource.getrusage`; its numerical results match the prior successful run. Reproduction validation and integration of peers' output remain the parent's responsibility.
