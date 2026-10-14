**Verdict:** Withhold new adoption. The conditional tax-only correction is **+6.774bn** (SE 4.075bn), beyond item 5b, and the conditional fixed-pool stack is **+10.077bn** (SE 4.164bn). These cross the $5bn point-estimate review bar. They are not an identified complete removal effect: deductions, person consumption, benefit units/takeup and added-child membership remain unmeasured. M6 is unpriced, not zero. [CALCULATION: `removal.py` → `derived/summary.json`, `derived/results.csv`, `derived/replicates.csv`] [INFERENCE]

## One change from the current central

Income year 2024, personal allocation, specifications 16 / 11, row-4 identified union 39,712,493, against v7 plus item 5b. A plus sign raises net cost to other residents. Every row holds other case lines fixed and is a modeled mechanical adjustment, not a causal forecast. SEs use all 160 SDR replicates; the stack SE comes from the summed replicate vector. [DATA: frozen v7 `package.cjs`, `derived/corrections.json`; CPS ASEC 2025 pinned archive] [FRAMING-SENSITIVE]

| Component, change from frozen v7 | Union, low / high $bn | SE $bn | G1 | G2 | G3+ | Review bar |
|---|---:|---:|---:|---:|---:|---|
| M1 | +6.723962 / +6.723962 | 3.570733 | -0.233367 | +1.317403 | +5.639926 | Above $5bn |
| M2 | +0.850817 / +0.850817 | 0.580743 | -0.304246 | +0.444106 | +0.710956 | Below $5bn |
| M3 | -0.800464 / -0.800464 | 0.186546 | +0.379708 | -0.585569 | -0.594603 | Below $5bn |
| M4_conditional_SNAP | -1.069501 / -1.069501 | 0.167594 | -0.222760 | -0.312886 | -0.533855 | Below $5bn |
| M5_fixed_pool | +4.372536 / +4.372536 | 0.346487 | -0.810791 | +0.132132 | +5.051196 | Below $5bn |
| tax_only_stack | +6.774315 / +6.774315 | 4.075207 | -0.157905 | +1.175940 | +5.756279 | Above $5bn |
| conditional_fixed_pool_stack | +10.077351 / +10.077351 | 4.163753 | -1.191456 | +0.995186 | +10.273620 | Above $5bn |

The primary whole-lineage reading uses the **same adjustment at both ends**, holding the case's existing added-person costs fixed; it does not observe their mixed units. `results.csv` separately shows the case-style G3 transport: each union G3+ adjustment per identified G3+ member times the case's 1.957M G3+-priced added people, white-priced people held. That assumed transport gives +11.479bn for the stack; its SE conditions on the transport coefficient. This is not a measured 42.75M correction. [ASSUMPTION] [CALCULATION: `result_rows`, `derived/case_inputs.json`]

## Positive controls and account sign

The original credits code runs unchanged with only its output directory redirected here. All six files reproduce byte for byte; all 83 original gates pass. Item 5b is +4.298545385bn and the old D is +2.279133775bn. D is a control, **never an added component**. [CALCULATION: `derived/positive_control/`, `positive_control()`]

The new correction is remaining nonmembers' tax after removal minus their tax on the original personal ledger, and original nonmember refunds minus their post-removal refunds. The already-booked A/B/C/Cr item-5b receipt and spending vectors are subtracted once. M1 includes federal liability before EITC/ACTC; M3 includes those refunds, not the same child credit a second time. Item 5b's own full-sample IRS normalization is retained for every replicate, so the subtraction uses one calibration convention. [CALCULATION: `federal_removal`, `original_item_parts`, `federal_denominator`]

## M1, M2 and M3: the surviving return

The local pinned NBER 2024 TAXSIM kernel evaluates surviving incomes, Social Security taxability, dependent counts, filing status, capital-gain preferences and state laws. A staying spouse files alone; nonmember parents receive staying dependents from vanished returns, including a new return if necessary. The current data transfer 20 dependents to existing returns and create 0 nonfiler returns. Children with no staying parent receive no invented claimant. Two nonmembers' joint return remains joint. The statutory survivor calculation and own IRS cell pass the head/spouse swap check at 1e-9 (measured discrepancy 0). The frozen personal baseline is held: relabeling which original person carried its tax changes that baseline by definition. [CALCULATION: `survivor_registry`, `federal_removal`; `test_removal.py`, `test_state_tax.py`] [ASSUMPTION: staying claimant rule and qualifying dependents]

The surviving return uses its own state-aware status flag and on-books share, its own weight, its own AGI bin and the remaining household's CBO income group at fixed original national rank thresholds. The benchmark cell multipliers are fixed; unsupported positive-tax cells block. A continuing claimant keeps the Census residual plus the statutory schedule difference; a new return gets its own statutory result, without unexplained joint-income residuals. M2 is state/replicate calibrated to original CPS positive state liability and uses the same canonical before/after kernel inputs as M1/M3, including the conditional care-spending attribution. State negative refunds are outside the positive receipt key and are held outside M2. [CALCULATION: `survivor_irs_cells`, `state_tax.compute`]

Baseline TAXSIM federal liability is 2010.375bn versus CPS 1984.587bn; EITC is 42.897 versus 42.624; ACTC is 26.449 versus 21.589. Retaining residuals is calibration, not validation of new returns. Keeping the original head's IRS cell instead of the survivor's gives M1 +4.998bn, showing material cell sensitivity. [CALCULATION: `derived/summary.json`, `derived/results.csv`] [INFERENCE]

Unobserved itemized deductions, qualified dividends, short/long gains, taxable pension shares, QBI, qualifying-household maintenance and actual child-care attribution remain assumptions. March 2025 ages are held as in the CPS model. Other refundable credits, including education credits and ACA PTC, are not identified as a return-level CPS value; their spending is held, not declared zero. The original non-PTC line convention prices EITC and ACTC together, as the control lane does. The M1/M3 result is therefore a conditional kernel simulation, not an exact reconstructed legal return. [ASSUMPTION / DEGRADED]

## M4: benefits

SNAP uses primary USDA FY2024/FY2025 schedules in calendar-year 9/3-month proportions, income tests, unit size, standard/earned/medical/care/support deductions, the benefit formula and the statutory maximum. It keeps reported CPS level residuals, varies missing shelter deductions, and compares reported participation held with full-takeup proxies. SPM is a proxy assistance unit, annual incomes proxy monthly incomes, and deductions are prorated: assets, state BBCE/ABAWD/student/status rules are unmeasured. Existing participation with zero shelter is -1.070bn; maximum shelter is -0.069; full-takeup/zero-shelter is -5.606, crossing $5bn only under that unverified takeup construction. [CALCULATION: `benefits.py`, `derived/benefit_results.json`] [ASSUMPTION]

Medicaid/CHIP uses parsed state age/parent/expansion thresholds and the 2024 FPL to show income-proxy transitions for surviving children/adults. The fixed MEPS expected-payment key remains held: eligibility is not observed enrollment or spending. ACA premiums, SLCSP, APTC, monthly enrollment and complete MAGI/employer-affordability inputs are absent, so PTC is unpriced. The health changes are unidentified. See `benefits-result.md` for proxy fit failures, excluded units, signed weights, threshold-vintage limits and the conditional SNAP envelope. [DATA: `derived/benefit_results.json` `Medicaid_CHIP`, `ACA`] [SOURCE: primary files and URLs in `inputs/benefit_pins.json`]

## M5: consumption allocation

Only mixed SPM units change: the adopted saving/remittance-adjusted resource pool is split in proportion to positive own disposable cash income, with joint tax bills split by positive AGI components. Each full/replicate weighted pool and the civilian national key is conserved at 1e-6bn or tighter; signed weights are retained, and noncivilian strata stay fixed. All-zero own-income units explicitly keep equal shares. The original consumption key and saving/remittance shares are positive controls. Sales, excise, customs and personal-transfer receipts use the live **union-only** targets; added people's targets are isolated and fixed. Federal excise keeps CBO income-group shares; the resulting raw union exposure is calibrated to the current case line. [CALCULATION: `weight_preserving_split`, `consumption_removal`, `case_inputs.cjs`]

Own disposable income is an attribution assumption, not measured individual consumption: children can consume resources supplied by parents. Half equal sharing / half own income reduces M5 to +2.186bn. Do not adopt the own-income split as a literal spending measurement. Resource-keyed service/subsidy lines and the corporate/business-property key remain held; M5 prices the requested consumption receipts only. [ASSUMPTION / SCOPE]

## M6: identity-loss reconciliation

The roster locates 0.970877M native children under 18 outside the identified union with a member parent (SE 0.083805M). The population concept includes such lost-identity descendants, but v5's 3.04M aggregate addition has no `PH_SEQ`/`PPPOS` crosswalk. No individual child's numerical inclusion or pool overlap is verified. The prior claim that a particular such child is already counted and would leave is therefore not established by these files. [CALCULATION: `identity_loss_children`, `derived/summary.json` `M6`] [INFERENCE]

No new child, cost or credit is added; the aggregate addition and its item-5b extrapolation stay fixed. If these children are added members, letting them stay can overstate continuing credits; replacing an aggregate child with a roster child requires subtracting its existing modeled costs first. The direction of the full fiscal correction cannot be determined without that membership/substitution map. M6's cost is **null/unidentified**, not an assumed measured zero. [ASSUMPTION / DEGRADED]

## Stack, adoption and limits

M1/M2/M3 are solved on one shared post-removal return, including nonlinear tax/credit interactions. The displayed stack adds that solved tax correction, the named conditional SNAP scenario and the fixed-pool M5 allocation. Its extra cross-module interaction is 0 **by construction**: SNAP uses pre-tax gross income and the pre-removal consumption pool is held. This does not estimate consumption responses to survivor taxes/refunds/SNAP, benefit takeup/health changes or M6. It is explicitly a partial conditional stack. [CALCULATION: `derived/replicates.csv`, `derived/summary.json` `stack`] [ASSUMPTION]

Recommend adopting no new headline edit from this lane yet. Retain the material tax finding for further validation; do not infer reliability from national residual calibration or from a confidence interval containing/excluding zero. Missing deductibles/new-return fit can move M1, and the tax-only sampling SE is large. Individual consumption observations or an explicit normative allocation rule would settle M5; actual program units/monthly resources would settle M4; a roster-to-added-person crosswalk with aggregate-cost replacement would settle M6. The politically sensitive analysis is LLM-assisted; independent source/gate checks reduce implementation errors without identifying the modeled counterfactual. [INFERENCE]

## Sources, checks and reproduction

Input URLs, primary-file SHA256 and reused read-only input hashes are in `inputs/pins.json`, `inputs/state_pins.json`, and `inputs/benefit_pins.json`. Downloaded constants are parsed, or evaluated by the pinned statutory kernel; no model-extracted numbers are used as statutory tables. NBER documents the local beta's 2024 coverage and input omissions: https://taxsim.nber.org/taxsimtest/. Census's workbook preserves its 2024 source cells in `inputs/state_parameters_2024.json`. [SOURCE]

Run from repository root:
```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/mixed_unit_removal_2026_10_14/removal.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/mixed_unit_removal_2026_10_14/ -q
```

The code review is `review-result.md`; its calibration issue was repaired and cancellation has a regression test. All implemented gates are in `derived/summary.json`; no existing gate or tolerance was relaxed. `RUN_LOG.md` records actual check commands, return codes, wall time, Python RSS and full-lane reproduction. The frozen case and all other lanes are read-only. No Git metadata was changed by this worker. Every changed path is enumerated in `changed-paths.txt`.
