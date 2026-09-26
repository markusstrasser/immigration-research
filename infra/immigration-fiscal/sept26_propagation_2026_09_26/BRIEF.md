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
