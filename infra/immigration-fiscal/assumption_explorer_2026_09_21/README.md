# Fiscal assumption explorer

**Verdict:** One self-contained page (`derived/explorer.html`) evaluates the complete annual
account of `full_account_2026_09_20` under any set of assumptions, live. Its evaluator
(`engine.js`) is the account's own formula, `welfare = P + weight * (direct + F)`, over executed
allocations and the 3,888 executed production scenarios. `test_engine.js` gates it against
2,629 rows of the 497,664-row grid (every level of every dimension), all 60 category
service-response cases, all 32 complete accounting cases and the four published headline
bounds (165.1-197.4 and 269.8-288.7 bn); worst gap 4e-9 bn. [CALCULATION: test_engine.js]

The page has a pinned result bar (the live number, its unresolved-convention span, the distance
from the central case, and the last-touched setting beside its central value and its effect
alone), convention cards, an exact Shapley split of the distance from the central case, a bridge
with uncounted-but-assigned amounts, a sensitivity ranking, and the full receipt and spending
ledger with per-line allocation rule and response. Below the ledger: whose welfare the ledger
counts, what four commentators argue (text, no number under any name), the 49 FAQ-routed
objection cards, and the whole confidence ladder, searchable and linked to ledger lines.

## Reproduce

```sh
cd infra/immigration-fiscal/assumption_explorer_2026_09_21
uv run --no-project --with duckdb --with pandas --with numpy python3 build_model.py   # hash-guards upstream
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl --with numpy python3 scaling_check.py
node test_engine.js
uv run --no-project python3 build_ui.py && open derived/explorer.html
```

`context.json` is rebuilt with `build_context.py <inventory.json>`; it keeps a value only when every
number in it equals, at its printed precision, a number within two lines of the cited file:line
(49 of 50 items and all 255 values on 2026-09-21; the dropped item is a caveat with no number).
Fabricated numbers at real locations are rejected in memo and CSV files alike.

`ladder.py` parses `research/immigration-confidence-ladder.md` at build time, so the page carries
the ladder's own sentences (171 entries on 2026-09-21: 89 current, 31 qualified, 51 historical).
Status is mechanical: entries 1-51 are the dated earlier layers; an entry is `qualified` when it
opens with a bracketed correction, is named in the file's opening correction notes, or is named by
a later entry as replaced, superseded, qualified or narrowed. Topics and ledger links are keyword
rules and the page says so. Only current entries show by default.

## General government: a proposal, not the published account

The published account holds defense **and** general government at zero response. The engine now
separates the two (`general_government_response`; the executed grid moves them together, and the
gate sets both from the grid's one column). `scaling_check.py` gives the evidence for treating
them differently [CALCULATION: scaling_check.py -> derived/scaling_check.json]:

- BEA Table 3.16, 2024: general public service outside interest is 475.8 bn, 63% of it state and
  local. Federal tax collection and financial management is 36.6 bn; federal executive and
  legislative 137.9 bn. [DATA: bea_nipa/Section3All_xls.xlsx, T31600-A lines 3, 4, 6, 44, 45, 47]
- Across the 50 states (FY2022), log spending on log population: governmental administration
  0.842 (se 0.039), financial administration 0.789, judicial 0.951; for comparison police 1.041,
  correction 0.975, K-12 0.983. [DATA: _cache/slf2022.xlsx, Census State and Local Government
  Finance Table 1, sha256 4dd123c5...643b9b; census_popest_2024/NST-EST2024-ALLDATA.csv]
- Implied response 0.59 (federal executive and legislative fixed, federal tax collection at 0.789,
  state and local at 0.842) to 0.84 (everything at 0.842). On the 48.3 bn assigned to the group
  that is 28.5-40.6 bn a year: the central span moves from 165-197 to 194-226 (low) or 206-238
  (high). [INFERENCE: a cross-section shows long-run scale, not a measured response to this group]
- Federal police, courts and prisons (82.8 bn, FBI included) are already charged per head inside
  `public_order_safety`; this is not an added cost. Defense and interest on debt already issued
  stay at zero.

Adopting this in the published account is a change of analysis protocol and needs the operator.

## Limits [FRAMING-SENSITIVE]

- Number cards (`presets.json`) are accounting conventions, never people: no commentator
  produced a number for this population. The authors section is text with audit references, the
  object each claim is about, and the closest convention where one exists. Caplan has none: his
  gains accrue mainly to migrants and his keyhole remedy applies to future entrants, so switching
  benefits off here would only stop counting 364 bn of costs.
- The ledger counts other US residents only. Gains to the group's own members (the place premium,
  where most of any world-GDP gain sits) and origin-country effects are not computed in this repo;
  the page says so rather than netting them.
- Settings off the executed grid are exact evaluations of the same linear formula, and are
  labelled as the reader's own assumptions.
- One income year of a resident stock. No generation split, lifetime value, crime-specific cost
  or policy effect; the cards say which outside results overlap and none may be added.
- The production block is CES; increasing-returns arguments are outside it.
- Compiled through an LLM (notes/llm-bias-caveat.md): the ledger numbers are gated, the readings
  of authors and the ladder's keyword links are not.
- Built for a desktop window and checked there in both themes (no overflow at 1400 px; the
  blue/orange pair passes the colour-vision validator in light and dark). At 390 px the page still
  scrolls sideways by 7 px; the cause was not found.
