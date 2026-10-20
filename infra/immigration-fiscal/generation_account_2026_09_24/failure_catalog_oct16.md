# Oct16 regression receipts

- Source item19 declares `added_G3plus` separately from the three observed
  generations. Dropping the fourth part lost 0.202460136354415bn at the low
  end. `v9_split.cjs` now folds that declared part into G3plus, and every
  specification and both conventions stop unless their costs close at 1e-9bn.
- Full old-output reproduction stops if upstream producers change. The first
  full `run_all.sh` rerun correctly blocked at `union_credit_age_v8.py` on the
  changed `world_ledger_2026_09_27/population_basis.py` pin. Its earlier
  provenance-only rewrite of `credit_replicates_oct15.json` was restored from
  the exact pre-run backup; no source pin was edited. The parent must reconcile
  the peer-owned producer before claiming an identical full historical rerun.
- Item16 and item17 counts must follow the same conditional difference as
  their costs. The own-price coverage writer gives item17 `joint minus item16`
  generation counts and zero observed change, rather than copying the joint
  calibration's counts twice. `coverage_check.cjs` verifies count and generation
  cost closure and rejects missing sets, nonfinite totals and generation gaps.
- Completion-marker quotations are not completion receipts. The coverage
  snapshot accepts only an exact standalone `L1 STEP 3 DONE` line once step3
  has been requested. A quoted future marker leaves the build STUB13.
- A post-engine arm's cost selector and typed-part selector must move together.
  `count_transfer` now selects `joint_count_transfer minus item16`, and its
  absolute coverage counts follow the source's selected count changes. G2
  integrates the actual CSV rows by generation/end in both sets and both arms;
  a negative control refuses the otherwise plausible central `joint` selector.
- A source response arm does not identify a new omitted-person price kernel.
  Nondefault items13/14/15/18 now expose a structured central-price carry,
  including its item12 source exposure and central item16/17 scope. In
  particular, item13 `unchanged` is not labeled whole-case unchanged while
  those channels are carried. `V9_ARM_TRANSPORT=require_own` blocks unsupported
  own kernels; G2 probes both labeling and the fail-loud switch. Default cases
  gain no empty carry metadata.

- The source-algorithm regression depended on a machine-local ignored cache and
  the current upstream pins. A peer's legitimate upstream change made its
  positive control fail before the intended algorithm mutation. The regression
  now builds an isolated declared contract and checks both source-pin drift and
  algorithm mutation; it never refreshes frozen historical scientific outputs.
