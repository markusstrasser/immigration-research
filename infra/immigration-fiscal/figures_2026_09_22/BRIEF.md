# Brief: bring the figures page to the adopted main case

Date: 2026-09-23. The operator adopted three changes to the complete account's main case
([decision](../../../decisions/2026-09-23-main-case-general-government-and-use-keys.md);
[main-case lane](../main_case_2026_09_23/RESULT.md)): general government at 0.59–0.84, public
order and safety keyed by use, uncompensated care keyed to uninsured use. This Svelte page still
shows the September 20 numbers ($165–197bn). Its README says numbers are copied from executed
tables named under each figure; keep that discipline.

## Numbers (copy from these files; cite them under the figure)

- `../main_case_2026_09_23/derived/main_case_bands.csv`, variant `adopted`: headline
  (cbo_category_lag_non_school_full) 203.2–249.6; non-school education fixed 158.9–212.6;
  proportional 307.9–341.0. `published` rows are the September 20 values.
- `../main_case_2026_09_23/derived/sign_reversal.csv`: ordinary services fixed, private capital
  fixed: adopted welfare −87.85 to +80.53 (the page shows cost as positive: lo −80.53, hi 87.85).
- `../historical_backcast_2026_09_20/derived/backcast_annual.csv`: the adopted columns
  `net_cost_cbo_informed_adopted_{low,high}__{flat,ratio,income}`. Rebuild the `backcast` array
  the same way the existing one was built from the six September 20 CBO-informed columns (check
  that rebuilding the existing array from those columns reproduces it exactly before switching).
  The programme-by-programme paths (`rulePaths`) exist only on the September 20 anchor; keep them
  and label them as such, or drop them if the figure cannot say so clearly.

## Text to update

`src/data.js` (responseRows, backcast), `src/lib/Paths.svelte` ("Midpoint of the $165bn and
$197bn anchors"), `src/lib/Places.svelte`, `src/lib/Ranges.svelte`, `src/lib/ResponseLine.svelte`
("general government and subsidies at zero response. That zero is an assumption."),
`src/App.svelte`. Replace the "General public services at 25%" row with the adopted rows. Keep a
September 20 headline row only if it helps a reader see the change. Say in one line under the
response figure what changed and link the decision. Use plain sentences; keep the page's existing
style (no new colours, boxes or badges).

## Gates

```sh
cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/figures_2026_09_22
bun run build        # must succeed
```

Then a headless look: `bun run preview` (or `dev`) in the background, `agent-browser --session
<s> open http://localhost:<port>`, `errors`, and screenshots of the response figure, the back-cast
figure and any section whose text you changed. LOOK at them. Stop the server afterwards.
`rg -n "165|197" src` must return only lines deliberately labelled September 20.

## Limits

Write only in `figures_2026_09_22/`. Do not commit, stash or checkout. Report files changed, gate
output and anything you could not do, in at most 10 lines.
