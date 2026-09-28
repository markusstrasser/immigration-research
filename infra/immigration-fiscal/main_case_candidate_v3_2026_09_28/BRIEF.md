# Lane brief: candidate v3, the bundled next-case revision

Date 2026-09-28, 09:15 JST. Parent session immigration-research-1c. At 07:39 the operator agreed to take the queued
corrections in one revision, built once and then put to him with a decision record. This lane builds that
candidate, `sept28_candidate_v3`, on candidate v2 (`main_case_candidate_v2_2026_09_28`, 08d9a86,
$318.57–383.69bn). Nothing here is adopted. Adoption is the operator's call, and he takes each item on its own.

## Read first

- `main_case_candidate_v2_2026_09_28/` (`package.cjs`, `main_case.cjs`, RESULT.md). Build on it; do not edit it.
- The adopted case `main_case_long_run_2026_09_27/` (`package.cjs`, `derived/corrections.json`). Do not edit it.
- Each item's lane, listed below. Import its code or read its committed outputs; do not copy numbers by hand.

## Items: each alone at specifications 48 and 11, then together

1–3. **v2's three items, unchanged:** public housing's operating deficit at the tenant key (−$1.69bn), production
   on the account's weights (+$1.64 / +$1.11bn) and the IRS-matched income-tax key (−$3.20 / −$3.10bn).
4. **Public housing's capital at the tenant key.** This is v2's own companion (the capital lane's variant
   `public_housing_at_rental_assistance_key`), −$0.3529 / −$0.5293bn. With it, the enterprise's current account
   and its capital sit at one key.
5. **Long-run property taxes** (ladder 253; `receipt_side_long_run_2026_09_28`, 8d1840a): owner-occupied at 0.763,
   tenant-occupied at 0.708 on the $83.84bn split, and personal property re-keyed to vehicles at 1, giving
   −$27.19bn at both ends. Carry the lane's ranges (owner 0.672–1; tenant national $83.84–123.13bn) into the
   range components.
6. **Payroll compliance** (ladder 254; `payroll_compliance_2026_09_28`, 89ee79d), in two parts:
   - 6a, the `all` central items on the calibrated within-group rule: −$0.37 / −$0.16bn;
   - 6b, row 2 carried through CBO's re-key by the within-group rule instead of in proportion to raw shares:
     −$0.81bn at both ends.
   Apply the lane's per-line ratios exactly as its `price.cjs` does (`applyCorrections` on the right model per
   method), carrying the proportional rule as a sensitivity.
7. **Workers' compensation pooled over income years 2019–2024** (ladder 251;
   `backcast_pandemic_measured_2026_09_28`, cbaddcf, `derived/ratio_vs_2024.csv`,
   `account_2024_change_if_pooled_bn`). The lane reports −$2.03bn / −$1.54bn at its "low" / "high" ends. Check
   which specifications those are before gating on them: in some lanes "low/high" means the shared/personal
   allocation.
8. **Transit at a riders' key.** The lines `fed_transit_and_railroad` and `sl_transit_and_railroad` are keyed by
   population. My chat estimate: ACS 2024 S0201 transit commuting 2.8% (Mexican) against 3.7% (all), so a riders'
   key of about 0.084 against 0.117, about −$2.2bn. That estimate is a proxy.
   - Build the key from the best source you can pin: ACS 2024 PUMS commute mode for the group against everyone,
     with NHTS 2022 transit trips by Hispanic origin as an all-trip check.
   - Split transit from railroad where the national source allows, and key only the transit part.
   - State the key's limits (commuters against riders, and NYC's weight in ridership).
9. **Pension accrual, a switch that is OFF by default** (`pension_accrual_2026_09_28`; not yet validated).
   - Accrual on: the social_security line's group amount becomes the OASDI accrual ratio times this candidate's
     own group OASDI receipts at each specification (employee plus employer OASDI, plus the OASDI share of
     self-employment tax). The medicare line swaps its Part A share (HI 416.3 / 1,109.8 of 2024 benefits) for the
     lane's Part A accrual.
   - Read the ratio and the Part A accrual from the lane's committed `derived/summary.json` (central) at build
     time, and record its hash. The lane is adding a national-aggregate validation, which may revise them. Until
     the parent commits the lane, build items 1–8.
   - Gate: switched on over the September 27 base alone, it reproduces the lane's +$121.9 / +$116.3bn at 48 / 11.
   - Report the candidate with the switch off (cash) and on (accrual), at all specifications. Name the unpriced
     interest on the group's existing pension liability beside it.

## Report

- Old → new at 48 / 11 for every item alone, and together. Report the items' interactions: the sum of the items
  alone against the joint total, and a sequential attribution in the listed order and in reverse.
- The band's ends and runner-up specifications across the 32 distinct specifications (48 ≡ 52, 11 ≡ 15), with
  the switch off and on.
- Carry forward v2's companions beside the range: public pay, the road arms, the outer range under the
  dependent-pieces rule, and the sign break-even. Keep defense at 0 with FAQ 2's GDP-share bound
  (+$47.5–72.0bn) beside.
- For each item, your recommendation: in the case or beside, with the one-sentence reason.

## Gates

- With every item off, the candidate reproduces September 27 exactly at all 64 specifications. With items 1–3 on,
  it reproduces v2 exactly.
- Each new item alone reproduces its lane's own figure at 48 / 11, or the RESULT explains the difference.
- Each item moves only its named lines, and national totals hold.
- Two runs through `scripts/rerun_lane.py` are byte-identical.

## Adoption path (specify, do not implement)

Write out the payload extension that `derived/corrections.json` would need for the items, with the engine.js
receipt-line and national-scale edits v2 named. List every lane that reads the payload
(`rg -l corrections.json infra/`) and say which would change.

## Rules

- A new lane in this directory. Do not edit the adopted case, either candidate or any other lane.
- Scripts write to `derived/`. Write `RESULT.md` first with `**Verdict:** pending` and append as you go.
- No commits, staging or stash.
- Final message: the RESULT path and at most ten lines, giving old → new at 48 / 11 for every item, the joint
  total with the switch off and on, and your in/beside recommendation per item.
