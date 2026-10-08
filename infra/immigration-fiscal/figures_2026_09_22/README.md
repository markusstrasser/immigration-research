# Figures

A Svelte 5 page of the account’s figures, set as a Tufte handout: one light theme, colour on data
marks only, sources in the margin. Each figure stays inside one account and names it above its title.

Figures: the tally-to-bill staircase; every combination of service responses and general
administration; age weights; generations; schooling and birthplace; places; who pays by income
fifth, with capped aid beside the fiscal cost; net per person by income percentile; offending against
two reference groups. The September 20 programme paths, the back-cast chart, the arrival-schooling
panel, the India decomposition and the ledger-convention chart were retired to sentences with inline
sparklines (last section).

## Visual grammar

One rule for every figure here and on the prototypes page (operator, 2026-09-25: "a consistent
visual grammar ... what's negative / positive").

- **Whose side.** A figure reports what the group's presence does to everyone else: US residents
  outside the Mexican-origin population. The title or axis says "everyone else".
- **Colour is the sign, and only the sign.** Orange (fill `#f2cabc`, line `#ca7a5e`): everyone
  else worse off. Blue (`#bbd4ee`, `#5c97d2`; text `#2f5f8f`): everyone else better off. Ochre
  (`#ecdcae`, `#b8913a`): break-even, or a range whose sign depends on the account's open choices.
  Grey (`#e4e1d6`, `#57544c`): about zero, or a neutral reference.
- **People are not coloured.** Where a figure compares groups (the group against whites, natives or
  other origins) or draws plain series, the group is a filled ink mark (`#111`) and the comparison a
  grey open mark (`#8d897e`), told apart by label. Orange and blue stay free for the sign.
- **No signed numbers.** Every number carries its direction in words: "$201–246bn worse off",
  "$1,147 better off", "a gain of $56–67bn". Axes name their ends in words ("worse off →",
  "better off ↑"); the zero line is ink.
- **Direction.** A horizontal axis of cost runs worse off to the right; a vertical axis runs better
  off up. The words at the ends decide, never a minus sign.

## Data

- `build_data.cjs` writes `src/generated/figures.json`, and only when every gate passes. The page shows the
  live main case only: v6, adopted 2026-10-07 (`../../../decisions/2026-10-07-main-case-v6.md`).
- The staircase and the matrix run v6 through its package (`account.cjs` loads
  `../main_case_2026_10_07/package.cjs` on the case's payload model): one `evaluateFull` per step or cell and
  specification, on a copy of the case's specification with that step's or cell's responses, so the
  engine, the case's added lines and its return on public capital run as the case runs them. The payload
  (`main_case_2026_10_07/derived/corrections.json`, `corrections_cash.json`, `summary.json`) is pinned by
  sha256 in `account.cjs` (`PAYLOAD`); the case's choices must reproduce the case at every specification.
- The other figures read lane files: who pays and the percentiles (`distribution_weights_2026_09_23`,
  `derived/oct07/`) and the back-cast (`historical_backcast_2026_09_20`, `derived/oct07/`) as they stood
  on v6, pinned by commit in `account.cjs` (`PINS`: distribution 498a6a71, back-cast 55a8fff7); the
  white-reference ledger with item T, the income tax the survey misses (`ledger_absolute_2026_09_17`,
  with its lifetime values and the case's own generation split from `generation_account_2026_09_24`);
  places with item T (`ledger_stress_2026_09_17`, `metro_match_2026_09_17`, the `*_T.csv` files); crime,
  custody and victims' harm; the origin screen and the schooling comparisons with item T; and the
  sentences' inputs. Several of these are ignored files: `figures.json` lists every input with its commit
  or `worktree`, whether git tracks it, and the sha256 of the text read (CRLF read as LF).
- The gates reproduce the case's files (the band, the cash set, the case without its capital return,
  the colleges-fixed, roads-fixed, general-administration-fixed and proportional bands, the C2 tally on
  accrual and on cash, `sign_reversal.csv`'s oct07 columns) and every published figure the page prints
  (ladder 194's −$80.3bn / +$45.4bn, the percentiles summing to the quintiles, NIBRS murder and robbery
  ratios, the custody ratios, the origin screen's Mexico and India rows, the item T places, the FAQ 5
  generation gaps and lifetime values, the back-cast's 2024 anchor and per-member figures). A last block
  checks each claim the text makes in words, so a rebuild that would leave a sentence false stops.
- No figure types its numbers in: `src/data.js` is gone.
- The research lanes move with each main case; the page moves when the operator asks. Re-run
  `node build_data.cjs` after an upstream lane changes on the live case.

## Prototypes

`prototypes.html` and `proto/` stay on the September 24 case until the operator asks to move them.
`proto_data.cjs` runs them on `account_sept24.cjs`, the account this page ran on until 2026-10-08. Their
gates against the figures page read `build_data.cjs` and `figures.json` as they stood on that case
(`account_sept24.cjs` `PINS.page`, fef4d12b; its figures.json is 57b48186's), and the prototypes page opens
with that page's staircase (`proto/staircase.cjs`, `src/proto/Staircase.svelte`).

## Run

```sh
cd infra/immigration-fiscal/figures_2026_09_22
node build_data.cjs   # every gate must pass
bun install
bun run dev           # http://localhost:5199
```
