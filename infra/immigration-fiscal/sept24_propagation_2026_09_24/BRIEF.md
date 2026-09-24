# Lane brief: move the remaining September 23 consumers to the adopted September 24 case

Date: 2026-09-24. The operator adopted the September 24 main case, $200.9–246.3bn
(`../main_case_2026_09_24/RESULT.md`, decision
`../../../decisions/2026-09-24-main-case-audit-and-outside-checks.md`). These consumers already
moved, and are out of scope:

- the figures page;
- the explorer;
- the back-cast;
- the sign break-even;
- the benchmark profiles.

`main_case_2026_09_24/RESULT.md` lists what was not re-run:

- the ten-year and lifetime anchors;
- the uncertainty propagation (`../uncertainty_propagation_2026_09_22/`, ladder 184);
- the real-costs totals (ladder 193/195 and
  `../../../research/immigration-real-fiscal-and-social-costs-2026-09-23.md`).

The debt legacy (`../debt_legacy_2026_09_23/debt_legacy.py`, ladder 207) is also still on
September 23. It re-implements the account in Python and needs a federal/state split of every
correction.

## Tasks

1. **Inventory.** Search `infra/` and `research/` for the September 23 case in any form:
   `203.2`, `249.6`, `203.207`, `249.64`, `adopted_2026_09_23`, `main_case_2026_09_23`,
   `227.9`, `237.48`. Classify each hit:
   - a live computation that reads the old case;
   - a hand-typed number in a script or data file;
   - historical text that is correctly dated.

   Identify what "the ten-year and lifetime anchors" are and which scripts produce them. Write
   the inventory to `derived/inventory.csv`.
2. **Re-run each live computation on the adopted case** by editing its own lane in place, and
   only its computation files. Before switching the input, confirm the script reproduces its
   current tracked outputs byte for byte on the September 23 input, as the regression gate. Then
   switch to the September 24 source: `../main_case_2026_09_24/derived/main_case_bands.csv`,
   `summary.json` (`group_receipts_bn`) and `corrections.json`. Never hand-type the new numbers.
   Read the corrected case from those files.
3. **Debt legacy.** Build the federal/state split of each correction from the line's government
   level in the model (`../assumption_explorer_2026_09_21/derived/model.json` and the
   `full_account_*` builders). Gate that federal plus state equals the total for every
   correction. Keep the lane's September 23 result reproducible behind a flag.
4. **Real-costs totals.** Compute the fiscal-plus-beside totals as the real-costs memo defines
   them, on the adopted case. Report old and new; the parent edits the memo. A sister lane
   (`../winners_losers_2026_09_24/`) builds a registry of the same channels. Use the same channel
   totals and name any disagreement.
5. **Report old → new for every number** in a table in RESULT.md, with the file that holds it.

## Boundaries

- Edit only the computation files of the lanes named in your inventory (for example
  `debt_legacy_2026_09_23/`, `uncertainty_propagation_2026_09_22/`), plus this directory. Do not
  edit memos, the FAQ, INDEX, the ladder, `engine.js`, `package.cjs` or `main_case.cjs`. Do not
  commit; the parent re-runs and commits.
- Consumers of `ledger_absolute_2026_09_17` verify stored source hashes and stop with
  `[BLOCKED] missing or stale source` after any edit to a fingerprinted `.py`. Never edit a hash.
  If a lifetime anchor sits behind that guard, report it and do not force it.
- Stub `RESULT.md` first with `**Verdict:** pending` and keep it current.
- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` and Node with
  `node`. Stop a re-run loop on the first nonzero exit code before comparing any hash.
- Never print keys. Never run `pgrep -f` or `ps` dumps.
- RESULT.md style: lead with the outcome in plain words; short paragraphs; tables with units; a
  model self-report line with the exact model id from your environment.
- Final message: the RESULT.md path and at most ten lines.
