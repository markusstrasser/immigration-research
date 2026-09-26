# Figures

A Svelte 5 page of the account’s figures, set as a Tufte handout: one light theme, colour on data
marks only, sources in the margin. Each figure stays inside one account and names it above its title.

Figures: the tally-to-bill staircase; every combination of service responses and general
administration; age weights; generations; schooling and birthplace; places; who pays by income
fifth; net per person by income percentile; offending against two reference groups. The
September 20 programme paths, the back-cast chart, the arrival-schooling panel, the India
decomposition and the ledger-convention chart were retired to sentences with inline sparklines
(last section).

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

- `build_data.cjs` writes `src/generated/figures.json`. The staircase and the matrix run the
  explorer’s evaluator (`../assumption_explorer_2026_09_21/engine.js`, gated by its
  `test_engine.js`) on its executed model and on that model with the data corrections adopted on
  2026-09-24 (`../main_case_2026_09_24/package.cjs`), one evaluation per step or cell. The
  staircase adds the corrections as its last two main-case rows (taxes, then benefits and
  services); the matrix runs on the corrected model, with the tax corrections carried to each
  incidence rule as the same proportional change. Who pays, crime, birthplace and the back-cast
  series and windows (the corrected concept) are read from the lanes’ CSVs. Who pays and the
  back-cast are read as they stood on the September 24 case, pinned by commit in `account.cjs`
  (`PINS`: distribution 6e554a3, back-cast da2b107; the prototypes’ explorer presets d710a74). The
  lanes move with each main case, and the pages stay on September 24 until the operator asks. The gates reproduce
  `main_case_2026_09_24/derived/main_case_bands.csv` (the case before the corrections, the adopted
  case and its non-school-fixed and proportional bands) and its receipts-side change, the
  explorer’s taxes-minus-benefits card, the $6–21bn production grid, ladder 194’s −$80.7bn /
  +$46.0bn, the percentile table summing to its quintile table, the NIBRS murder and robbery
  ratios, the origin screen’s Mexico and India rows and the back-cast’s 2024 anchor. Nothing is written if a gate fails. Re-run it after any upstream lane
  changes.
- `src/data.js` holds numbers copied from the executed tables named beside each export; move an
  array into `build_data.cjs` whenever its figure is touched.

## Run

```sh
cd infra/immigration-fiscal/figures_2026_09_22
node build_data.cjs   # every gate must pass
bun install
bun run dev           # http://localhost:5199
```
