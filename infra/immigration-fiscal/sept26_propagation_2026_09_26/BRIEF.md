# Lane brief: move the consumers of the September 24 case to the adopted September 26 case

Date: 2026-09-26. The operator adopted the September 26 main case, **$200.9180–245.6949bn**
(`../main_case_2026_09_26/RESULT.md`, commit ca619bb; decision
`../../../decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md`). It is the
September 24 package plus two corrections:

- **Finite-removal responses** (ladder 227): general government responds at 0.6000/0.8504 instead
  of 0.59/0.84, schools at 0.6522/0.6813 instead of 0.63/0.66, and audit row 8's constant shrinks
  by 0.949 (−$0.10bn).
- **The consumption key** (ladder 225): receipt edits on general sales tax, selective excise,
  customs and personal current transfers, and zero-weight spending edits on `resources` keys.

Read the RESULT's "For consumers" section first. Every consumer below still runs on September 24.

## What changes for a consumer

1. **The payload.** `../main_case_2026_09_26/derived/corrections.json` has the same format as
   September 24's and goes through `Engine.applyCorrections` the same way.
2. **The responses.** These are engine state, not cell edits. They are in
   `corrections.json` → `meta.responses` (also `summary.json` → `responses`):
   - `general_government.low/high` replace 0.59/0.84 (today read from `scaling_check.json`
     `composite_low/high` or from `main_case_2026_09_23/derived/inputs.json`);
   - `school.growth/decline` replace the hand-typed 0.63/0.66.

   Read them from the file and never hand-type them. The new payload with the old responses gives
   a mixed case ($196.7–242.2bn), which is wrong.
3. **Node consumers** that import `main_case_2026_09_24/package.cjs` can import
   `main_case_2026_09_26/package.cjs` instead. It has the same interface plus `RESPONSES`,
   `specsFor(o)`, `central(o)` (options `finite`, `ck`) and `correctionsPayload()`. Its `MAIN_SPECS`
   already carry the new responses.
4. **Bands and summary names.**
   - `main_case_bands.csv` keeps `adopted` and `adopted_2026_09_23` and adds `adopted_2026_09_24`
     and `uncorrected_at_adopted_responses`.
   - A gate on the uncorrected model uses **`uncorrected_at_adopted_responses`
     ($207.4046–253.1859bn)**. The September 23 case ($203.2070–249.6400bn) is the uncorrected
     model at the old responses.
   - `summary.json` → `group_receipts_bn` gains `adopted_2026_09_24`.

## Protocol for every consumer

a. **Regression gate first.** Rerun the consumer as it stands. Its tracked outputs must reproduce
   byte for byte (sha256) on the September 24 case. Stop on the first nonzero exit code before
   comparing any hash. If a consumer does not reproduce as it stands, report that and leave it.
b. **Switch with the old case kept.**
   - Keep the September 24 run reproducible behind the lane's case flag. Add one where the lane
     already has a flag convention (`--case sept24` → add `sept26`, now the default).
   - A lane with a test that pins an older case (`test_debt_legacy.py`, `test_distribute.py`) keeps
     it passing and adds the September 26 case.
   - Read the new case from the files above.
c. **Gates on the new case.** The corrected model reproduces $200.9180–245.6949bn (1e-4). An
   uncorrected-model gate reproduces $207.4046–253.1859bn.
d. **Determinism.** Run twice; the second run must be byte-identical.
e. **Report old → new** for every number the consumer publishes, in a table in your RESULT file,
   with the file that holds each.

## Workers and their consumers

**W1, `lanes`**, in this order (the debt legacy's control reproduces the back-cast):

1. `../historical_backcast_2026_09_20/backcast.py`. Its "corrected" concepts read
   `main_case_2026_09_24` bands and `group_receipts_bn`. Move them to the September 26 case; da2b107
   shows how the September 24 switch was made.
2. `../distribution_weights_2026_09_23/distribute.py`, with `--case sept26`. The package's change at
   each band end moves A; P and F do not move.
3. `../uncertainty_propagation_2026_09_22/`. `sept24_specs.cjs` sets responses per spec: add the
   September 26 specs, taking the responses from the payload. Then `propagate.py --case sept26`.
4. `../debt_legacy_2026_09_23/debt_legacy.py`, with `--case sept26`.
   - Its engine port must take the adopted responses (its `PROFILES` school (0.63, 0.66) and
     `INPUTS` general-government response) from `meta.responses`.
   - Apply the new payload, and split each new correction into federal and state-local parts. The
     row-8 change splits as the row-8 constant does. Consumption-key edits split by the government
     level of their receipt or spending line, in the model and the lane's shares.
   - The finite responses act on general government (its federal and state-local components, as
     the lane composes them) and on schools.
   - Gate that federal plus state-local equals the total for every correction.

**W2, `generation`**: `../generation_account_2026_09_24/` (`run_generations.cjs`, `run_all.sh`).

- Import the September 26 package. Its `MAIN_SPECS` carry the responses.
- Split the new edits across G1, G2 and G3+:
  - the row-8 change as the lane splits the constants line;
  - the consumption-key edits by generation-specific consumption shares, if
    `../consumption_key_2026_09_24/` (`cps_frame.py`, `consumption_key.py`) can identify generation
    (parents' birthplace in the CPS). Otherwise split each line's edit by the generations' shares of
    the old key, and state it as a limit.
- Gates: the three generations add to the union in every specification, and the union reproduces
  $200.9180–245.6949bn.

**W3, `explorer`**: `../assumption_explorer_2026_09_21/`.

- `build_ui.py` loads the September 26 `corrections.json`.
- The central preset evaluates the new case. Preset response values come from `meta.responses`:
  expose them to `presets.json` as `value_from` keys, as `composite_low` is today. Slider marks show
  the adopted values beside the elasticities.
- Each changed preset note says in one sentence why the response exceeds the elasticity, citing an
  id in `sources.json`; the registry validates at build time.
- `test_engine.js` checks the three September 26 bands both ways, as it did for September 24:
  - $200.9180–245.6949bn (main);
  - $156.5248–210.8433bn (non-school education fixed);
  - $301.2853–334.7516bn (proportional).
- Update the numbers in `context.json` and the README.
- Rebuild `derived/explorer.html`. Verify in a headless browser (`agent-browser`) that the central
  preset shows $200.9–245.7bn and that the corrections switch works. Screenshot the result area; it
  can sit below the fold. Engine semantics do not change.

The figures page, the winners-and-losers ledger (with the compliance and vending rows) and the
real-costs totals depend on W1's and W2's outputs. They follow in a second round.

## Boundaries

- Edit only your listed directories, plus your `RESULT_<worker>.md` in this directory. Do not edit
  `../main_case_2026_09_24/`, `../main_case_2026_09_26/`, the engine's semantics, `research/`,
  `decisions/`, `CLAUDE.md`, INDEX, FAQ or the ladder.
- **Other workers run in the same checkout at the same time, on other directories.** Do not commit,
  and do not run `git add`, `stash`, `checkout` or `reset`. The lanes read ignored data (`sources/`,
  `_cache/`, `node_modules/`), so there is no worktree.
- Consumers of `ledger_absolute_2026_09_17` verify stored source hashes. Never edit a hash; report
  a guard instead of forcing it.
- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` from the repository
  root, and Node with `node`. Never print keys, and never run `pgrep -f` or `ps` dumps.
- Stub `RESULT_<worker>.md` first with `**Verdict:** pending` and keep it current as you go.
- RESULT style: lead with the outcome in plain words; short paragraphs; tables with units; a
  model self-report line with the exact model id.
- Final message: the RESULT path and at most ten lines.

## Round 2 (dispatched after W1 and W2 are committed)

**W4, `ledger`**, in this order:

1. `../sept24_propagation_2026_09_24/band_variants.cjs` and `real_costs_totals.py`. Add a case
   parameter; do not copy the scripts. The September 24 outputs must reproduce byte for byte. Write
   the September 26 outputs to this directory's `derived/`: `band_variants.*` from the September 26
   payload and responses, then `real_costs_totals.*`.
2. `../winners_losers_2026_09_24/` (`specs.cjs`, `winners_losers.py`), then the rows it reads from
   `../compliance_gap_2026_09_24/` and `../vending_restaurants_2026_09_24/`.
   - The lane pins its inputs at commits (`BASE_COMMIT`, `DEBT24_COMMIT`). Add September 26 pins at
     the commits that hold W1's distribution and debt-legacy runs; the parent gives them in the
     dispatch.
   - `specs.cjs` copies the package's grid. Its import race is fixed (e5e23ec), so it may import
     `../main_case_2026_09_26/package.cjs`.
   - The consumption key is now inside the adopted case. Its channel moves from "proposed" to the
     fiscal channel. Keep the September 24 run reproducible.

**Update, 23:15: schools at full cost.** At 22:39 JST the operator adopted schools at full average
cost (`../main_case_schools_full_2026_09_26/`, $258.4885–291.9548bn; decision
`../../../decisions/2026-09-26-main-case-schools-full-cost.md`). The September 26 case above is now
the one-year scenario.
- Every consumer takes a case `sept26_schools` → that lane's `package.cjs`, `corrections.json` and
  `derived/`, as its **default**, and keeps `sept26` and `sept24` reproducible.
- The payload's edits equal September 26's; only `meta.responses.school` changes, to 1/1.
- The uncorrected-model gate is that lane's `uncorrected_at_adopted_responses`
  ($265.5903–298.6797bn).
- The union's range ends move to specifications 48 and 11: the school-share bound flips when schools
  respond at 1. A bridge from an earlier case runs at matched specifications first, then adds one
  "range ends move" term.
- W4 targets `sept26_schools`.
- W5 is dropped: the operator said "we don't have to update all the uis ... we're still
  researching", so the figures page, prototypes and explorer stay on earlier cases.

**W5, `figures`** (dropped 23:15, see above): `../figures_2026_09_22/` (`build_data.cjs`,
`account.cjs`, the Svelte sources, `dist/`).

- `build_data.cjs` reads the September 26 payload and `meta.responses`; no hand-typed 0.59/0.84 or
  0.63/0.66 stays in a computation.
- Labels that print a response ("General administration, 0.59–0.84") show the adopted values.
- The staircase gains the September 26 step in the existing grammar (README "Visual grammar"). The
  number line's corrections range becomes $164–277bn.
- Every gate passes. Rebuild, then screenshot every changed figure at 1400 and 390 px. Scroll each
  section into a tall viewport; the `#id` crop blanks sections below the fold.

## W4 `ledger`, dispatched 2026-09-26 23:35: work order

Target case: **`sept26_schools`** (`../main_case_schools_full_2026_09_26/`: `package.cjs`,
`derived/corrections.json` with school 1/1 in `meta.responses`, `derived/main_case_bands.csv`,
`derived/summary.json`). Keep **`sept26`** (`../main_case_2026_09_26/`, the one-year scenario) and
**`sept24`** runnable. `sept24` must reproduce the committed files byte for byte.

Committed state to build on:
- Sept 26 consumer runs: back-cast f5b4aae, distribution f697514, uncertainty 1d14940, debt legacy
  e62fccb.
- The explorer is on Sept 26 (b84629e).
- Figures pages are pinned at Sept 24 (fef4d12); stay out of `../figures_2026_09_22/`.
- W1 (`lanes`) and W2 (`generation`) are now adding `sept26_schools` as their default. The parent
  commits them and sends you the commit hashes before your step 2 pins them.

**Step 1: now.** In `../sept24_propagation_2026_09_24/`:
- **`band_variants.cjs`.** Add a case parameter; do not copy the script. The case chooses the
  package (`main_case_2026_09_24`, `main_case_2026_09_26` or `main_case_schools_full_2026_09_26`),
  its payload and its responses. Every package already exposes `cost`, `MAIN_SPECS` and `specsFor`.
- **`real_costs_totals.py`.** Add the same parameter. §7 pairs the fiscal band with the social rows;
  §7b carries care and mobility. Under the schools case the fiscal row is $258.4885–291.9548bn.
- **`constant_choices.py`.** Add `--case sept24` so it reproduces its committed outputs. Where it
  zeroes `row8`, it must also zero the finite-removal row-8 piece (`row8_finite`, −$0.10bn) on the
  Sept 26 cases.

Default output paths: `sept24` → `../sept24_propagation_2026_09_24/derived/` (unchanged). The
default `sept26_schools` → this directory's `derived/`. `sept26` → `--out-dir DIR` only.

Gates:
- the `sept24` rerun reproduces every committed file byte for byte;
- the schools-case bands reproduce the lane's `main_case_bands.csv` (1e-4);
- the variants gate against their own case;
- two runs are byte-identical.

**Step 2: after the parent's pin message.** `../winners_losers_2026_09_24/` (`specs.cjs`,
`winners_losers.py`, `test_winners_losers.py`), then the rows it reads from
`../compliance_gap_2026_09_24/` and `../vending_restaurants_2026_09_24/`.

1. **First, fix the unpinned read.** `PATHS["debt_corrections"]` reads
   `debt_legacy_2026_09_23/derived/corrections_federal_by_component_2024.csv` from the working tree.
   Since e62fccb that file holds the Sept 26 case, so `per_correction_check` fails. Read it through
   `git_show` at the pinned commit, as the other debt inputs are read. Then run the regression gate:
   the `sept24` rerun reproduces every committed file.
2. **Add `--case sept26_schools` as the default**, plus `sept24` (reproducible) and `sept26` if it
   costs one row of pins. Add pins in the lane's style (`BASE26S_COMMIT`, `DEBT26S_COMMIT`,
   `GEN26S_COMMIT`) at the hashes the parent sends. `specs.cjs` may import the case's `package.cjs`
   now (import race fixed in e5e23ec); keep its band gates.
3. **The consumption key** (ladder 225) is inside the adopted case from Sept 26 on. The
   `consumption_proposal` registry row applies only to `sept24`; under the later cases the key sits
   in the fiscal channel.
4. **School dilution** (sister row `school_dilution`, $16.1bn beside) prices school cost left
   unfunded at a response below 1. Under `sept26_schools` nothing is unfunded. The row leaves the
   main case's nets and moves to the role table, labelled "applies to the lower-response scenarios
   only" (decision `2026-09-26-main-case-schools-full-cost`, bullet "School dilution").
5. **Compliance and vending rows.** Rerun each lane's row builder if it depends on the case. If it
   doesn't, show that and leave its files alone.
6. **Gates.**
   - Under each case, the generations add to that case's band (1e-3).
   - The fiscal channel's A is taken from the distribution lane's `fiscal_totals(<case>)` at the
     pinned commit.
   - The ledger's regression tests keep passing and gain the new case.
   - Two runs are byte-identical.

Report old → new for every published number (Sept 24 → schools case, and the one-year scenario where
computed), with the file that holds each. Boundaries as in round 1:
- edit only the directories named above plus `RESULT_ledger.md` here;
- no git writes;
- stub the RESULT first with `**Verdict:** pending`;
- final message: the RESULT path and at most ten lines.
