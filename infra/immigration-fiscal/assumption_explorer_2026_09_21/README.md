# Fiscal assumption explorer

**Verdict:** One self-contained page (`derived/explorer.html`) evaluates the complete annual
account of `full_account_2026_09_20` under any set of assumptions, live. Its evaluator
(`engine.js`) is the account's own formula, `welfare = P + weight * (direct + F)`, over executed
allocations and the 3,888 executed production scenarios. `test_engine.js` gates it against
2,629 rows of the 497,664-row grid (every level of every dimension), all 60 category
service-response cases, all 32 complete accounting cases and the four published headline
bounds (165.1-197.4 and 269.8-288.7 bn); worst gap 4e-9 bn. [CALCULATION: test_engine.js]

The page shows presets, the result with its unresolved-convention span, an exact Shapley split of
the distance from the central case, a bridge with uncounted-but-assigned amounts, a sensitivity
ranking, the full receipt and spending ledger with per-line allocation rule and response, and
context cards for executed results outside the account.

## Reproduce

```sh
cd infra/immigration-fiscal/assumption_explorer_2026_09_21
uv run --no-project --with duckdb --with pandas --with numpy python3 build_model.py   # hash-guards upstream
node test_engine.js
uv run --no-project python3 build_ui.py && open derived/explorer.html
```

`context.json` is rebuilt with `build_context.py <inventory.json>`; it keeps a value only when every
number in it equals, at its printed precision, a number within two lines of the cited file:line
(49 of 50 items and all 255 values on 2026-09-21; the dropped item is a caveat with no number).
Fabricated numbers at real locations are rejected in memo and CSV files alike.

## Limits [FRAMING-SENSITIVE]

- Author presets (`presets.json`) are reconstructions from the truth-conditions of claims recorded
  in this repo's audits, not quoted positions; each setting carries stated / implied /
  not_addressed and a memo reference. The authors write about all immigrants; the account is the
  Mexican-origin resident stock, all generations. A preset transports assumptions; it does not
  test the author's number.
- Settings off the executed grid are exact evaluations of the same linear formula, and are
  labelled as the reader's own assumptions.
- One income year of a resident stock. No generation split, lifetime value, crime-specific cost
  or policy effect; the context cards say which outside results overlap and none may be added.
- The production block is CES; increasing-returns arguments are outside it.
