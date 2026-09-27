# Lane brief: the next main-case candidate, revised after its attack

Date 2026-09-28, 05:00 JST. Parent session immigration-research-1c. The first candidate
(`main_case_candidate_2026_09_28`, c313b53, $323.68–388.70bn) was attacked in
`candidate_attack_2026_09_28` (f0e262e). Its arithmetic holds, but three of its explanations do not. The held-out
IRS test of the income-tax key (`tax_key_heldout_2026_09_28`, aec08a4, ladder 249) adds a third item. Build
`sept28_candidate_v2` so that the operator can accept or reject each item on its own. Adoption is his call.

## Read first

- `candidate_attack_2026_09_28/RESULT.md`, all of it. Every correction below comes from it.
- `main_case_candidate_2026_09_28/RESULT.md` and `package.cjs`. Build on that package in this lane; do not edit it.
- `tax_key_heldout_2026_09_28/RESULT.md` §3, `ends.cjs` and `derived/translation_inputs.json`.
- The adopted case: `main_case_long_run_2026_09_27/` (`package.cjs`, `derived/corrections.json`). Do not edit it.

## Items (each reported alone at specifications 48 and 11, then together)

1. **Public housing's enterprise deficit keyed by its tenants.** Split NIPA 3.8 line 13 (housing and urban
   renewal, current surplus −$40.30bn in 2024) out of the enterprise line and key it by the rental-assistance key
   (kh), not the population key (ke). Keep the consolidation of the $5.258bn operating subsidy; under this key it
   moves nothing.
   - The attack's §1 [E] expects −$1.69bn at both ends on the September 27 case.
   - Report the first candidate's population-key reading (+$0.22bn) beside, and name the choice in one sentence.
2. **Production on the account's weights.** The first candidate's item 2, unchanged: +$1.64 / +$1.11bn on
   September 27.
3. **The federal income-tax key matched to IRS 2023, raked with CBO's groups.** Take
   `share_change.irs_2023_raked_with_cbo_groups` from the tax lane's `translation_inputs.json`. Apply it through
   the stack factor exactly as that lane's `ends.cjs` does. It expects −$3.20 / −$3.10bn on September 27.

## Beside the range

- **Public pay** on the account's own shrinking public workforce (attack §4d). The attack gives
  $12.05–12.39 / $7.85–8.09bn on the first candidate. Recompute it on v2, and state the approximation (a uniform
  removal share across skill groups).
- **Road arm, three cases.**
  - Replacement adjustment.
  - A fixed stock. State that the across-state scaling of highway construction (0.79, CI 0.68–0.91; attack §3a)
    excludes it.
  - The upward case: a stock scaled like construction, +$0.44–0.90bn at spec 48 on September 27.

## Corrections to carry

- **Outer range.** Apply the dependent-pieces placement rule to every component, including the range's own
  long-run response read jointly with congestion. The attack gets $260.61–434.22bn on the first candidate.
- **The consolidation's "after" gate is an identity.** Keep it as a unit test of the two helpers and describe it
  that way. List the internal transfers that still cross differently keyed legs after item 1, with −$m per $1bn.
- **Specifications.** The 64 hold 32 distinct ones (48 ≡ 52, 11 ≡ 15). Every statistic across specifications uses
  the 32.
- **Sign break-even.** Re-derive it for v2 (the attack did not check `sign_reversal.cjs`).

## Gates

- With every item off, v2 reproduces September 27 exactly at all specifications.
- Each item moves only its named lines. The items add exactly.
- Report the ends and runner-up specifications.
- Two runs through `scripts/rerun_lane.py` are byte-identical.

## Adoption path (specify, do not implement)

Consumer lanes apply `main_case_long_run_2026_09_27/derived/corrections.json`. Write out the payload extension v2
would need: the split enterprise line and its key, the production grid, and the tax-key share change. List every
lane that reads the payload (`rg -l corrections.json infra/`) and say which of them would need a change.

## Rules

- A new lane in this directory. Do not edit the adopted case, the first candidate or any other lane.
- Scripts write to `derived/`. Write `RESULT.md` first with `**Verdict:** pending`, and append as you go.
- No commits, staging or stash.
- Final message: the RESULT path and at most ten lines, with old → new at 48 / 11 for every item.
