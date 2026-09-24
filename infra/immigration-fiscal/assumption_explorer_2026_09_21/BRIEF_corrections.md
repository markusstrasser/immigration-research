# Brief: put the September 24 data corrections into the explorer

Date: 2026-09-24. The operator adopted a package of data corrections to the complete account's
main case ([decision](../../../decisions/2026-09-24-main-case-audit-and-outside-checks.md);
[lane](../main_case_2026_09_24/RESULT.md)). The main case moves from $203.2–249.6bn to
$200.9–246.3bn a year: the group's taxes were overstated (+$48.7 / +$50.3bn of cost) and so was
its keyed spending (−$51.0 / −$53.6bn). The explorer still shows the September 23 case.

## Already done by the parent (commit 9e1dd44; do not edit these files)

- `engine.js`: `applyCorrections(model, payload)` returns a corrected copy of the model; a state
  with `data_corrections: true` evaluates `model.corrected` (throws if it is not attached).
  `defaultState()` has `data_corrections: false`, so every existing consumer is unchanged. Three
  new response classes serve the correction lines: `education_school_part`,
  `education_other_part`, `correction_constant`.
- `../main_case_2026_09_24/derived/corrections.json`: the payload (270 cell edits, three
  correction lines with `label`s, `meta`). Written by `main_case.cjs` only when its gates pass.
- `test_engine.js` attaches `model.corrected` and checks, with explicit `{data_corrections: false}`,
  the September 20 and September 23 bands, and, with `{data_corrections: true}`, the three
  September 24 bands from `../main_case_2026_09_24/derived/main_case_bands.csv` (central
  200.8752–246.3184, non-school education fixed 157.1268–210.8300, proportional
  302.9720–336.4219), plus attribution closure over the switch. It passes now.

If you find that `engine.js`, `corrections.json` or the main-case lane needs a change, stop and
report it in your result file; do not edit them.

## Do

1. **Load the payload.** `build_ui.py` inlines `../main_case_2026_09_24/derived/corrections.json`
   as `window.CORRECTIONS`, the same way it inlines the model; refuse to build if it is missing.
   `ui.js` attaches `M.corrected = E.applyCorrections(M, window.CORRECTIONS)` once, before any
   evaluation.
2. **One control for the switch.** Add `data_corrections` to the controls, styled like the
   existing native controls (checkbox or two radios). Its note says what the corrections are, in
   plain words: a dataset audit and four outside checks, adopted 2026-09-24. Tax records by legal
   status and survey fill-ins, and CBO’s income shares, lower the taxes assigned to the group.
   Treasury’s credit shares, program records for benefits, and medical care charged by use lower
   the spending keyed to it. Do not type the dollar effects into the note. The result bar’s
   “effect alone” and the attribution show them live. Give it a `sources.json` place, citing the
   decision record and the lane RESULT. `build_ui.py` refuses unknown or uncited places.
3. **Controls everywhere.** The switch must be a control path in every place that lists
   controls: the Shapley split of the distance from the central case, the sensitivity ranking,
   the "last touched" effect, undo and reset. Check `executedStatus()`, which decides whether
   settings are the account's own. The corrected central case must not read as “your own
   assumptions”.
4. **Presets.** In `presets.json`, every preset except `repo_central` (“as published on September
   20”) gets a settings entry `{"path": "data_corrections", "value": true, "label": "Data
   corrections", "basis": "stated", "note": …, "ref": "decisions/2026-09-24-main-case-audit-and-outside-checks.md"}`.
   `repo_central` gets the same path with `false` and a note saying the published figure predates
   the corrections. Add a test in `test_engine.js`: the central preset as loaded, with no extra
   overrides, reproduces the September 24 central band; `repo_central` as loaded has the switch
   off.
5. **Ledger.** The three correction lines appear in the spending ledger with their payload
   `label`s when the switch is on. Where the ledger shows a line’s amount, it shows the corrected
   amount. If it fits the design, mark each line’s correction (corrected minus uncorrected
   target at the current allocation, rule and key) as a small signed figure. If not, add one
   sentence above the ledger that names the switch. Keep it minimal.
6. **Objection cards.** Several `context.json` cards quote the September 23 case: $203–250bn, the
   5.5–16.4% break-even, −$87.8bn to +$80.5bn frozen, the back-cast $1.7–2.5tn, and "adopted
   September 23". The FAQ (`research/immigration-objections-faq-2026-09-21.md`), the INDEX, ladder
   entries 162 and 219 and the back-cast memo now carry the September 24 text:
   - $201–246bn;
   - break-even 4.8–16.0%;
   - frozen services with capital fixed −$25.3bn to +$77.8bn on CBO rules;
   - $157–211bn with non-school education fixed, $303–336bn proportional;
   - back-cast $1.7–2.4tn, $2.5–3.6tn and $3.0–4.5tn.

   Follow `BRIEF_context.md`'s procedure. Write `_cache/inventory_2026_09_24b.json` from the
   current items, rewrite each stale card from the current FAQ text with the September 24 figure
   first, and re-anchor every citation that no longer verifies. Run `build_context.py` on it. No
   card may be dropped silently. Check that each value's source still stands (memory trap 10:
   the numeric gate passes STALE values).
7. **Hand-typed numbers.** Search `presets.json`, `context.json`, `template.html`, `ui.js` and
   `README.md` for 203, 249.6, 250, 5.5–16.4 and "adopted September 23". Each number shown on the
   page must be computed live or verified by `build_context.py`.
8. **README.** Update the verdict: the central case is now $200.9–246.3bn with the corrections,
   and the September 23 bands reproduce with the switch off. Add a section “Adopted 2026-09-24:
   data corrections” describing the switch, the payload and the gates, and update Reproduce:
   `node ../main_case_2026_09_24/main_case.cjs` writes the payload before `node test_engine.js`.

## Design

This is the operator's page. Keep the Tufte handout style: one light theme, paper #fffff8, a
Palatino-family serif, booktabs tables, no boxes, pills or left-border callouts, native controls,
and colour on data marks only. Read the memory file
`~/.claude/projects/-Users-alien-Projects-immigration-research/memory/immigration-assumption-explorer.md`
for the traps: the off-screen result, quirks mode, the `.pos/.neg` background, the grid column
set to `auto`, and number-token comparison when editing verified prose.

## Validate (all must pass; paste the output tails into your result file)

```sh
cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/assumption_explorer_2026_09_21
node test_engine.js                                   # PASS, including your new preset gates
uv run --no-project python3 build_context.py _cache/inventory_2026_09_24b.json   # report kept/dropped
uv run --no-project python3 build_ui.py               # no unknown or uncited places
```

Then do a headless check with agent-browser on `file://…/derived/explorer.html`, with
`agent-browser errors` empty. Take screenshots, look at each one, and list their paths:
- the result bar at the central preset ($201–246bn as cost, or the page's sign convention);
- the same with the switch off ($203–250bn), with the attribution naming the switch;
- the new control and its note;
- the ledger rows for the three correction lines;
- the preset cards;
- two refreshed objection cards.

## Boundaries

- Edit only files under `assumption_explorer_2026_09_21/` (except `engine.js`), plus
  `_cache/` there. Read anything.
- Do not commit. The parent reviews and commits.
- Use `uv run --no-project python3`. Never print API keys. Do not edit the essay.
- Write your result to
  `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/f5e074c6-6b7b-4605-a1d5-4fae37fcfc81/scratchpad/explorer_worker_result.md`,
  opening with `**Verdict:**`. Then give the files changed, the gates with their output tails, the
  screenshot paths, the cards changed or dropped with reasons, and anything left undone and why.
  Return that path and at most ten lines.
