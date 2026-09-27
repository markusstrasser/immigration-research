# Brief: the return on public capital, priced consistently across the account's services

Date 2026-09-27. Parent session immigration-research-1c. The operator delegated the open ladder-231
decision ("ok do what you think is well reasoned and makes sense", 13:22 JST).

## Why

The main case (`main_case_schools_full_2026_09_26`, $258.4885–291.9548bn) charges government
services at BEA consumption, which includes depreciation but "assumes a zero net return" on public
capital (NIPA 3.10.5 note 2). The school-capital lane (`school_capital_return_2026_09_26/`, ladder
231, proposed) priced the omitted return for K-12 alone: $9.52bn at 2% and $14.28bn at 3%. With it,
the account's school capital charge lands on the cash-basis charge (outlay + interest) that the
ledger uses; without it the account sits below (that lane's §7). Adding K-12 alone would be
inconsistent: every tax-financed service the main case lets respond uses public capital too. This
lane prices the return for all of them, at the main case's own responses and allocation keys, so the
parent can decide adoption on a consistent number.

## Scope

1. **Inventory.** List every service line of the account (engine: `assumption_explorer_2026_09_21/engine.js`;
   case: `main_case_schools_full_2026_09_26/package.cjs` `MAIN_SPECS`, `cost()`, and
   `derived/corrections.json` → `meta.responses`). For each line give its response in the main case and
   its allocation key. Lines at response 0 (defense, existing interest, business subsidies) and lines
   held fixed (economic affairs, highways included) get no capital charge; say so per line.
2. **Capital per responsive line.** Map each responsive, tax-financed line to the public capital that
   serves it, from BEA's Fixed Assets tables (state and local, and federal nondefense where the line is
   federal). Reuse the school lane's `_cache/` downloads and functions read-only; do not edit any file
   in `school_capital_return_2026_09_26/` or `main_case_schools_full_2026_09_26/` (the figures
   session owns both). At least:
   - K-12: reproduce the school lane's $9.52bn / $14.28bn exactly (gate).
   - Higher education: the non-K-12 part of educational structures (the school lane's key gives the
     K-12 share), charged only in proportion to the account's college line and net of the
     tuition-financed share.
   - Public order and safety (the main case keys it by use).
   - Health, net of fee recovery in the same proportion the account nets hospital sales (the school
     lane notes gross $491.4bn against net $126.8bn).
   - General government: office structures (and any other type that serves it), at its response
     (0.6000/0.8504 at the band ends).
   - Anything else that responds. Fee-financed utilities and public housing stay out: the account's
     lines are net of sales, so fees recover their capital. Name every exclusion.
   - Equipment and intellectual property: include where BEA gives a usable split, else report as a gap.
3. **Rates.** 2% (A-4 2023; 2024 real Treasury yields) and 3% (A-4 2003, in force since M-25-15) as the
   band's low and high ends; 7% (A-4 2003's private-capital rate) reported only. Real rate on the
   current-cost net stock (2024 average of year-end stocks), as in the school lane.
4. **Per specification.** For each of the 64 specifications, the group's return = Σ lines stock ×
   rate × the line's key at that specification × its response. Add it to the case's cost at the same
   specification (from `package.cjs`) and report the candidate band (min and max over specifications)
   with the end specifications. Report the move at fixed specifications as well: never difference
   two bands' ends (they can come from different specifications).
5. **Double-count gates.** The interest row stays at 0 in the main case; `debt_legacy_2026_09_23` is
   federal only; the production term carries private capital only; the new-seats upside and land
   are not priced (land: report the school lane's per-10% conversion for each line, as a
   sensitivity, marked [GAP]).

## Outputs (all inside this directory)

- `capital_return.py` (or `.cjs` if the engine is needed), deterministic, stops with `[BLOCKED] …` on
  any failed gate and writes nothing then.
- `derived/`: per-line table (stock, key, response, return at 2/3/7%), group totals, per-spec costs
  with and without the return, the candidate band, and `gates.json`.
- `RESULT.md` opening with `**Verdict:**`: the consistent total at 2% and 3% (and 7%), the candidate
  main case, what each line contributes, every exclusion with its reason, every gap, and the files
  covered and skipped.

## Validation (run from the repository root; report each result)

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/capital_return_services_2026_09_27/capital_return.py
# run it twice: derived/ must be byte-identical
node infra/immigration-fiscal/main_case_schools_full_2026_09_26/main_case.cjs | tail -1   # still "all gates passed"
```

## Rules

- Do not commit, stage or stash. The checkout is shared with another session: touch nothing
  outside this directory.
- Primary sources only for every number used in a calculation (BEA tables, OMB texts, Census, NCES);
  tag claims `[SOURCE]`, `[DATA]`, `[CALCULATION]`, `[INFERENCE]`, `[GAP]`.
- `csv.writer(..., lineterminator="\n")`. Never print the Census API key.
- Report token use is not required; report wall time of the final run.
