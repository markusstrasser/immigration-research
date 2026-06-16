# Immigration prototype progress

Date: 2026-04-10

## Scope

This pass builds two real prototypes against the weakest parts of the immigration incidence stack:

1. `Federal prototype`
Texas-targeted ACS origin-household cells joined to a CPS ASEC donor-cell library for foreign-born low-skill households.

2. `Local prototype`
Texas tract-to-PUMA-to-unified-school-district context using ACS tract metrics and district finance.

## What the federal prototype does

1. Replaces the unusable staged SIPP slice with CPS ASEC 2024 March.
Reason: the staged SIPP file turned out to be child-only for this purpose and could not support adult household microsimulation.
2. Builds donor cells from actual foreign-born low-skill households in CPS ASEC.
3. Estimates:
   - household earnings
   - payroll tax from person-level `FICA`
   - federal income tax from person-level `FEDTAX_AC`
   - pre-Medicaid net after household SNAP and person SSI amounts
   - SNAP / SSI / Medicaid / EITC participation rates

## What the federal prototype does not do

1. It is not a full federal microsimulation.
2. Medicaid remains a flag, not an annual dollar amount.
3. It is a donor-cell library, not a causal federal estimate for Texas.
4. Donor coverage is sparse outside a subset of low-income household cells.

## What the local prototype does

1. Replaces area-weighted county overlays with tract-based weights.
2. Uses ACS tract renter counts and school-age population as weights.
3. Uses Texas unified school district boundaries and district finance.
4. Produces a PUMA-level stage-3 context table for Texas.

## What the local prototype does not do

1. It is Texas-only.
2. It uses unified school districts only.
3. It is still a capacity-context table, not a causal marginal-burden estimate.

## Why this matters

These prototypes directly attack the two weakest assumptions identified in the confidence ladder:

1. `federal-side proxy ledger`
2. `coarse local burden bridge`

## What actually materialized

1. `Federal donor library`
   - `sipp_household_donor_cells_2023`: `24` donor cells
   - built from CPS ASEC 2024 March:
     - `89,473` household rows
     - `144,265` person rows
     - `2,356` qualified foreign-born low-skill households
2. `Local stage-3 context`
   - `tx_tract_stage3_context_2023`: `6,896` tracts
   - `tx_puma_stage3_context_2023`: `217` PUMAs
3. `Integrated federal target layer`
   - `tx_origin_household_target_cells_2023`: `845` Texas target cells
   - `tx_origin_household_federal_proto_2023`: `845` joined rows
   - `tx_origin_puma_household_stage3_context_2023`: `845` Texas local+federal joined rows

## Verified attachment rates

1. `Federal donor match coverage`
   - `238 / 845` Texas target cells matched a donor cell
   - row coverage: `28.17%`
   - household-weight coverage: `26.34%`
2. `Texas local stage-3 coverage`
   - school-finance attachment at PUMA layer: `217 / 217` PUMAs
   - school-finance attachment at final Texas joined layer: `845 / 845` rows
   - housing-stress attachment at final Texas joined layer: `845 / 845` rows

## Corrections made during execution

1. The staged SIPP slice was rejected after verification.
   - it exposed only child-age values for this use case and was not fit for adult household donor construction
2. The federal donor builder was replaced with a disk-backed CPS ASEC pipeline.
3. Texas ACS person extraction was corrected.
   - local corpus only had `csv_pus.csv`, the `A` half of the national person file
   - Texas required the official state-specific ACS person file `psam_p48.csv`
4. Texas district finance was corrected.
   - the stable Texas filter is `NCESID LIKE '48%'`, not `STATE='48'`
5. Final Texas PUMA attachment required normalized `puma_code` matching.

## Current epistemic status

1. The prototypes are real and materially better than the earlier proxy stack.
2. The federal side is still sparse because donor cells only cover about a quarter of Texas target-cell household weight.
3. The local side is now attached on both school-finance and housing-stress dimensions for Texas.
4. These are usable for method development, scenario building, and identifying where incidence claims are data-supported versus donor-sparse.
5. They are still not strong enough for high-confidence statewide fiscal point estimates.
