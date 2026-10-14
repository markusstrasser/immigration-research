**Verdict:** M2 is a **+$0.722bn** conditional sensitivity (160-replicate SE **$0.580bn**) on the identified union, below the $5bn review bar at either v7 end. Do **not** adopt it as an exact correction. The local NBER 2024 state-rule kernel is source-backed, but the CPS does not identify all deductions and pension/business classifications; state calibration is an assumed transport rule. [CALCULATION: `state_tax.py --run` → `derived/state_sensitivity.json`]

Covered: M2 state income tax. Skipped: M1, M3–M6 and shared driver, owned by peers.

## Source discovery

No source-complete state-tax engine found in repository Python/CJS or sibling tool files. Existing `cps_imputation_keys_2026_09_23/taxcalc.py` is federal only. Census's primary tax-parameter workbook is the candidate source; all parsed constants will retain cell provenance and source hashes.

The subsequently located NBER local TAXSIM test executable runs locally on this Mac and documents state law through 2024. Every source and the programmatically parsed Census 2024 parameter column is hashed in `inputs/state_pins.json`; parsed entries retain the workbook cell and source label. No records leave the computer. The kernel's `siitax` is state tax after credits; `fiitax + v25 + actc` recovers federal tax before EITC and ACTC for the parent's M1/M3 computation. [SOURCE: https://taxsim.nber.org/taxsimtest/; https://taxsim.nber.org/taxsimtest/low-level-local.html; https://www.census.gov/topics/income-poverty/income/guidance/tax-model.html]

## M2 results

All changes are net cost against v7 personal allocation; item 5b is federal only and supplies no state component. Both end specifications use the same state-liability key, so this conditional union sensitivity has the same effect at each end and in both set/cash accounts. This component covers 1,323 mixed civilian joint returns. [DATA: `state_sensitivity.json` `returns`, `scope`; frozen receipts builder `state_liability`]

| Identified union, $bn | Change | Replicate SE |
|---|---:|---:|
| G1 | −0.303526 | 0.194067 |
| G2 | +0.406291 | 0.390414 |
| G3+ | +0.619616 | 0.384617 |
| Total | +0.722380 | 0.579778 |
| Original carrier is non-member | −2.842121 | 0.371534 |
| Original carrier is member | +3.564502 | 0.405805 |
| Uncalibrated TAXSIM arm | +0.861861 | 0.589403 |

[CALCULATION: `state_tax.py` → `derived/state_terms.csv`, `derived/state_replicates.csv`, `derived/state_sensitivity.json`]

No added-descendant observations are reconstructed here. Any extension to the 42.75M lineage must be computed by the shared driver under a stated extrapolation; the union result must not be described as a measured full-lineage correction. The added people priced as whites cannot be inferred from this identified-group state calculation. [ASSUMPTION / SCOPE]

## Rule and sign

1. Build all original returns from the reused CPS return registry. Each state-law calculation uses person income components, Social Security, age, state and qualifying-dependent counts. A surviving non-member files single or head of household using their own components, without an unexplained share of the joint AGI. TAXSIM automatically assigns head of household to an unmarried taxpayer with dependents; the maintenance/qualifying-relative assumptions are inherited from the CPS registry. [DATA: `taxsim_frame`; SOURCE: NBER TAXSIM input documentation]
2. Calibrate positive original TAXSIM state liabilities to the CPS positive `STATETAX_A` total, separately by state and by all 161 weight columns. Transport that state factor to the survivor. This reproduces the original benchmark, but does not validate the response to income or filing-status changes. Indiana and Maryland need factors 1.6103 and 1.5764, consistent with a material local-tax/deduction mismatch; those factors are not legal marginal tax rates. [CALCULATION: `state_sensitivity.json` `state_calibration`; INFERENCE: possible source of mismatch]
3. Apply the original carrier's own on-books/status factor to the original non-member baseline and the surviving person's own factor to their new tax. Keep the original carrier's weights on the old tax and the survivor's weights on the new tax. [DATA: `compute`]
4. Additional cost = surviving non-members' calibrated positive tax minus original non-member-carrier positive tax. A member-carrier return contributes its surviving tax; a non-member-carrier return contributes the change in its surviving tax. This restores the remaining receipt against the personal baseline exactly once. Generation follows the departing member spouse. [CALCULATION: `difference`, `member_gen`; INFERENCE: removal-account sign]

Held explicitly: unobserved itemized deductions, rents, property taxes and childcare are zero; all dividends are qualified and capital gains long-term; pensions are treated as taxable; self-employment is non-QBI. Negative state refunds are outside the case's positive receipt key and are not turned into spending. `other_personal_tax` is held: sharing the source proxy does not establish the same behavioral response. The standalone result above prices mixed joint returns only. [ASSUMPTION / DEGRADED]

The shared driver may supply `refiling={own, dep_counts, R, owner}` aligned to the original return rows, optionally with canonical `before_input` and `after_input` TAXSIM frames. The latter use exactly the shared M1/M3 childcare attribution, so their state deduction/credit interactions enter consistently. This extends the modeled change to continuing non-member returns when member dependents leave or staying dependents are transferred in: the new signed liability is original Census `STATETAX_A` plus state-calibrated TAXSIM(after)−TAXSIM(before), then floored at zero. The original residual is retained only for the same continuing claimant, not a newly re-filed spouse. A recipient's generation owner comes from the shared transfer registry; an unowned nonzero change blocks. Newly created recipient filers are outside this original-row extension. This optional result is not the joint-only numeric table above. [DATA: `compute` `refiling`; ASSUMPTION: transported statutory delta]

`compute` returns `remaining_state_liability`, `remaining_state_own`, and `remaining_state_live` for the shared consumption interaction. Liabilities are full-weight calibrated CPS dollars after the surviving person's own status rule; continuing unchanged returns retain their original Census amount. These arrays are original-return-aligned, not a new population frame. [DATA: `compute` return schema]

## Validation and reproduction

- Eleven tests pass: independent California bracket-tax integration from the primary Census workbook; head-of-household deduction parsed from the workbook; survivor head/spouse symmetry; zero-income survivor; own survivor weights; departing unauthorized flag does not reduce a legal survivor; arbitrary new-filer input builder; transferred-dependent continuing return retains its residual and changes tax; canonical shared care inputs forwarded; malformed output and nonzero executable exits fail loudly. [CALCULATION: `test_state_tax.py`]
- State calibration closure across all replicates: **7.6294e−15bn**; generation closure: **1.3323e−15bn**. Head/spouse-swapped survivor inputs differ by **0**. Equal survivor inputs deterministically give equal kernel liabilities; the v7 personal correction remains dependent on which original record carried the joint tax. [CALCULATION: `state_sensitivity.json` `gates`]
- The kernel checks source hashes, process exit, required columns, finite inputs/results, row counts and IDs/order. A state with CPS positive taxes but no simulated positive base blocks. A zero/zero stratum is declared structural and recorded. [DATA: `run_taxsim`, `compute`]

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/mixed_unit_removal_2026_10_14/state_tax.py --run
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/mixed_unit_removal_2026_10_14/test_state_tax.py -q
```

Source acquisition is explicit (`state_tax.py --acquire`) only when pins do not exist; runtime verifies pins and never downloads/replaces them. The pinned local executable is an x86_64 Mac binary in `_cache/`; other operating systems require a separately pinned matching NBER build. The shared lane rerun must cover the parent's driver and peers; the component run does not claim their coverage.

## Log

- 2026-10-14: discovered and probed pinned NBER local 2024 kernel; no external record submission.
- First full component run: **23.704s**, peak self RSS **918,192,128 bytes**, child RSS **9,601,024 bytes**.
- Final component run after adding uncalibrated sensitivity and parsed-source pin: **9.530s**, peak self RSS **1,442,955,264 bytes**, child RSS **9,617,408 bytes**; all below 2.5GB. Timing uses Python `time.perf_counter` and `resource.getrusage`, not sandbox-denied system tools.
- 2026-10-14 20:43 JST: eleven tests passed, exit 0; both owned Python files compile. Shared positive controls for item 5b and prior D are the parent's responsibility and live in the shared driver.
- 2026-10-14 20:44 JST: final component output hash replay **IDENTICAL: 3/3**, exit 0; run **13.618s**, peak self RSS **1,144,438,784 bytes**, child RSS **9,617,408 bytes**. The shared lane's required `rerun_lane.py` pass remains the parent's integration check.
