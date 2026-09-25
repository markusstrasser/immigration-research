# Figures

A Svelte 5 page of the account’s figures, set as a Tufte handout: one light theme, colour on data
marks only, sources in the margin. Each figure stays inside one account and names it above its title.

Figures: the tally-to-bill staircase; every combination of service responses and general
administration; age weights; generations; schooling and birthplace; places; who pays by income
fifth; net per person by income percentile; offending against two reference groups. The
September 20 programme paths, the back-cast chart, the arrival-schooling panel, the India
decomposition and the ledger-convention chart were retired to sentences with inline sparklines
(last section).

## Data

- `build_data.cjs` writes `src/generated/figures.json`. The staircase and the matrix run the
  explorer’s evaluator (`../assumption_explorer_2026_09_21/engine.js`, gated by its
  `test_engine.js`) on its executed model and on that model with the data corrections adopted on
  2026-09-24 (`../main_case_2026_09_24/package.cjs`), one evaluation per step or cell. The
  staircase adds the corrections as its last two main-case rows (taxes, then benefits and
  services); the matrix runs on the corrected model, with the tax corrections carried to each
  incidence rule as the same proportional change. Who pays, crime, birthplace and the back-cast
  series and windows (the corrected concept) are read from the lanes’ CSVs. The gates reproduce
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
