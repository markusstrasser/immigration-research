**Verdict:** Round 2 supplies a bounded unified removal arm, replacing item 5b and D once. Adopt the weight, survivor-record and EITC corrections; retain the tax-input, own-resource, health-takeup, added-person and pension assumptions as arms. [CALCULATION: `round2.py` → `derived/round2_summary.json`]

| Unified removal, $bn | Low v7 end | High v7 end |
|---|---:|---:|
| set, bounded_low | 350.292 (Δ+10.740, SE 4.417) | 434.389 (Δ+10.740, SE 4.417) |
| set, bounded_high | 354.084 (Δ+14.532, SE 4.405) | 438.181 (Δ+14.532, SE 4.405) |
| cash, bounded_low | 275.166 (Δ+10.740, SE 4.417) | 359.263 (Δ+10.740, SE 4.417) |
| cash, bounded_high | 278.957 (Δ+14.532, SE 4.405) | 363.055 (Δ+14.532, SE 4.405) |

The low/high model rows vary takeup and shelter within each fixed v7 end specification 16 / 11. They are conditional model envelopes, not sampling confidence intervals. Set and cash have the same current tax/transfer/key adjustments; the pension model upper arm is beside the set only. [ASSUMPTION] [FRAMING-SENSITIVE]

| One change from v7, $bn | Set low / high | Cash low / high | SE low / high | Recommendation |
|---|---:|---:|---:|---|
| M1_federal | +6.723962 / +6.723962 | +6.723962 / +6.723962 | 3.570733 / 3.570733 | arm: own-survivor flags/cell and filing status are measurement corrections; unobserved deductions remain conditional |
| M2_state | +0.850817 / +0.850817 | +0.850817 / +0.850817 | 0.580743 / 0.580743 | arm: state-calibrated own-return recomputation; income/deduction transport conditional |
| M3_refunds | -0.800464 / -0.800464 | -0.800464 / -0.800464 | 0.186546 / 0.186546 | arm: solved with M1; EITC operator repair is a measurement correction |
| M6_biological_children | +1.847528 / +1.847528 | +1.847528 / +1.847528 | 0.265029 / 0.265029 | arm: biological link correction adopted in arm; priced universe stays fixed and roster projection removed once |
| D_added_residual | +0.545411 / +0.545411 | +0.545411 / +0.545411 | 0.259237 / 0.259237 | arm: G3 transport on unlocated added people; white amount held at zero |
| M5_consumption | +4.372536 / +4.372536 | +4.372536 / +4.372536 | 0.346487 / 0.346487 | arm: own disposable resources are an explicit allocation rule |
| M5_owner_property | +1.133426 / +1.133426 | +1.133426 / +1.133426 | 0.114867 / 0.114867 | arm: applies same resource rule to owner unit |
| M5_SNAP_key | -0.171835 / -0.171835 | -0.171835 / -0.171835 | 0.205792 / 0.205792 | arm separately; exact baseline interaction removes it from solved SNAP removal |
| M4_SNAP_baseline_interaction | +0.171835 / +0.171835 | +0.171835 / +0.171835 | 0.205792 / 0.205792 | adopt accounting identity in solved removal; cancels M5 SNAP key arm |
| M5_housing_key | -0.025789 / -0.025789 | -0.025789 / -0.025789 | 0.131858 / 0.131858 | arm: reported housing pool reallocated, rent and eligibility responses held |
| Medicaid_low | -1.436357 / -1.436357 | -1.436357 / -1.436357 | 0.180987 / 0.180987 | arm: statutory household/eligibility plus empirical takeup and primary-source cost bridge |
| Medicaid_high | -0.322352 / -0.322352 | -0.322352 / -0.322352 | 0.133141 / 0.133141 | arm: statutory household/eligibility plus empirical takeup and primary-source cost bridge |
| ACA_low | -0.483317 / -0.483317 | -0.483317 / -0.483317 | 0.095348 / 0.095348 | arm: enhanced schedule, enrollment and premium proxy; rule-based bounded estimate |
| ACA_high | +0.464593 / +0.464593 | +0.464593 / +0.464593 | 0.040479 / 0.040479 | arm: enhanced schedule, enrollment and premium proxy; rule-based bounded estimate |
| tax_replacement_item5b_and_D | +13.884538 / +13.884538 | +13.884538 / +13.884538 | 4.275700 / 4.275700 | replacement item, not an additional change from v7; subtract old item5b first |
| SNAP_cap_observed_high_takeup | -0.707893 / -0.707893 | -0.707893 / -0.707893 | 0.159310 / 0.159310 | arm: statutory SNAP with observed-cell takeup and shelter band |
| SNAP_cap_observed_low_takeup | -0.527782 / -0.527782 | -0.527782 / -0.527782 | 0.150981 / 0.150981 | arm: statutory SNAP with observed-cell takeup and shelter band |
| SNAP_cap_observed_newly_eligible_high | -0.639091 / -0.639091 | -0.639091 / -0.639091 | 0.079099 / 0.079099 | diagnostic component only; newly eligible/ineligible separately, never a complete SNAP arm |
| SNAP_cap_observed_newly_eligible_low | -0.458980 / -0.458980 | -0.458980 / -0.458980 | 0.060316 / 0.060316 | diagnostic component only; newly eligible/ineligible separately, never a complete SNAP arm |
| SNAP_cap_observed_newly_ineligible | +0.251742 / +0.251742 | +0.251742 / +0.251742 | 0.079687 / 0.079687 | diagnostic component only; newly eligible/ineligible separately, never a complete SNAP arm |
| SNAP_zero_observed_high_takeup | -2.631240 / -2.631240 | -2.631240 / -2.631240 | 0.245841 / 0.245841 | arm: statutory SNAP with observed-cell takeup and shelter band |
| SNAP_zero_observed_low_takeup | -2.195441 / -2.195441 | -2.195441 / -2.195441 | 0.218580 / 0.218580 | arm: statutory SNAP with observed-cell takeup and shelter band |
| SNAP_zero_observed_newly_eligible_high | -1.586365 / -1.586365 | -1.586365 / -1.586365 | 0.159509 / 0.159509 | diagnostic component only; newly eligible/ineligible separately, never a complete SNAP arm |
| SNAP_zero_observed_newly_eligible_low | -1.150566 / -1.150566 | -1.150566 / -1.150566 | 0.118875 / 0.118875 | diagnostic component only; newly eligible/ineligible separately, never a complete SNAP arm |
| SNAP_zero_observed_newly_ineligible | +0.206317 / +0.206317 | +0.206317 / +0.206317 | 0.063417 / 0.063417 | diagnostic component only; newly eligible/ineligible separately, never a complete SNAP arm |
| bounded_low_membership_benefit_interaction | +0.643503 / +0.643503 | +0.643503 / +0.643503 | 0.123358 / 0.123358 | adopt interaction accounting inside chosen arm; latent-child departures change survivors benefits |
| bounded_high_membership_benefit_interaction | +0.269805 / +0.269805 | +0.269805 / +0.269805 | 0.067834 / 0.067834 | adopt interaction accounting inside chosen arm; latent-child departures change survivors benefits |
| M6_all_biological_federal_tax_arm | +2.488160 / +2.488160 | +2.488160 / +2.488160 | 0.291603 / 0.291603 | arm beside fixed lineage: all biological departures, including source-definition conflicts; own costs of outside-definition children held, not newly booked |

The tax replacement row is the new item amount, not an additional v7 delta. All other standalone rows are one change from v7. Health and SNAP standalone rows use the identified-union departures; the unified rows additionally include their explicit membership-benefit interaction. SEs sample all 160 signed CPS SDR replicates, conditional on policy/cost/calibration assumptions, not an uncertainty estimate for those assumptions. [CALCULATION / ASSUMPTION]

SNAP key allocation is shown as a one-change arm. Its negative baseline interaction is included in every unified row; adding it without that interaction would double count attribution. `round2_replicates.csv` stores generation vectors and the exact covariance-preserving stack. [CALCULATION]

The original item-5b and D controls remain byte-identical under `derived/positive_control/`; old D is a control and is not added to any unified row. The original conditional first-pass result is preserved in [round1-result.md](round1-result.md). All original diagnostic arms remain in `derived/results.csv` and `derived/replicates.csv`. [DATA]

## Membership and credit carriers

The own-parent biological rule identifies 0.853468M children outside the union; 0.074754M step-only children stay. 0.517863M fit the frozen latent universe. They replace its modeled crossing-credit projection once (not their own costs). The remaining outside-definition children are priced as an all-biological federal-tax arm beside the fixed-lineage result; inserting their own costs into the 42.75M headline would silently change its population. [CALCULATION / ASSUMPTION]

Every counted child is assigned to exactly one partition: identified union, located latent subset, or unlocated residual of the fixed addition. This is an explicit reconciliation rule, not an individual crosswalk observed in the aggregate loss estimate. `derived/membership.json` includes count closure, raw parent-field conflicts, generation/class assignment and nonmember claimants. The literal all-biological rule stays visible beside it. [DATA / ASSUMPTION]

The blanket −$1.033bn subtraction is rejected: a claimant credit for a child is not that child’s own refundable-credit record. The located latent children have no own-record CTC/ACTC/EITC; the nonzero crossing-credit projection that is replaced is explicitly traced by receipt/spending side. The reverse-credit diagnostic is not added a second time to the jointly solved returns. [CALCULATION: `membership.py`; `derived/membership.json`]

## Primary-source health arm and costs

See [health-result.md](health-result.md), `inputs/health*`, and `derived/health_results.json`. Health is priced as an arm; the primary expenditure/enrollment bridge and its vintage are explicit. Each state/category transition and newly eligible/ineligible count is in that output. [SOURCE / CALCULATION]

## Keys and weight conservation

Own-resource splitting is an arm; all-zero own resources retain equal shares. The original civilian weighted key total stays fixed in every unit and all 161 columns. The worst closure discrepancy is 2.62e-15bn. The old within-member unweighted sharing artifact is +1.443594bn; v7's personal allocation excludes it, so no extra +$1.44bn is booked. The four affected person-key metrics each pass the within-member identity in all 161 columns. [CALCULATION: `resource_keys.py`; `derived/round2_summary.json` `resource_keys`]

## Pension and federal-tax alternatives

See [pensions-result.md](pensions-result.md) and [tax-corrections-result.md](tax-corrections-result.md). The high-AGI federal scenario is recomputed directly, not the former scalar; both headline ends use the ordinary key. The pension inputs support a conditional one-earner family-model envelope, not a measured lifetime-spouse entitlement correction or new cash payment. [CALCULATION / ASSUMPTION]

The pension zero-current-earnings proxy is +2.746940bn at both set ends (SE 0.217975); the historical-model upper is +13.946102bn (SE 0.465090). Both are arms, with primary pension costs held in set/cash. Their hypothetical benefit timing cannot be inserted as this year's cash. [CALCULATION / ASSUMPTION]

The remaining white-priced added people take zero crossing credits and D under the existing case rule, explicitly an assumption. Located biological children receive their observed linked-return treatment regardless of their aggregate G3/white price blend. The reviewer’s ≤$0.25bn white-credit amount is a sensitivity claim, not a verified hard bound on D; adding $0.25bn beside the reported arm moves each endpoint by that amount. [ASSUMPTION / INFERENCE]

## Reproduction and scope

Run `removal.py` then the full lane pytest command with `-p no:cacheprovider`; `RUN_LOG.md` records actual return codes and `rerun_lane.py` IDENTICAL receipts. Every computation is deterministic, retains 160 signed SDR replicates, and fails on source, weight or closure drift. No frozen-case or other-lane source is edited. No Git metadata is written. [CALCULATION]

This LLM-based political research can inherit framing bias; recommendations above separate numerical corrections from counterfactual assumptions. [INFERENCE]
