# Main-case engine (the former assumption explorer)

**Verdict:** This directory holds the formula the main case runs on. `engine.js` is the complete annual
account's own formula, `welfare = P + weight * (direct + F)`, over executed allocations and the 3,888
executed production scenarios. It carries the data switch (`applyCorrections`), which applies a case's
payload edits, and an exact Shapley split (`attribute`). The 13 main-case lanes and 36 other lanes import
the engine or its compiled model (`derived/model.json`) by this path, so the directory keeps the name of
the interactive page it once served. The operator retired that page on 2026-10-15 (tombstones below).
`test_engine.js` gates the engine against 2,629 rows of the 497,664-row grid, all 60 service-response
cases, all 32 accounting cases, the four published September 20 headline bounds and the bands of the
main-case lanes of September 23, 24 and 26. Worst gap 4.3e-9 bn. [CALCULATION: test_engine.js]

## Files

- `engine.js`: the formula, the data switch and the attribution.
- `build_model.py`: compiles `derived/model.json` and `derived/test_vectors.json` from the `derived/`
  outputs of `full_account_*_2026_09_20`, and refuses to build when an upstream hash moved.
- `scaling_check.py`: the evidence for general government's response (below); writes
  `derived/scaling_check.json`.
- `test_engine.js`: the engine's regression gate.

`derived/` is ignored and rebuilt by the commands below. `REPRODUCTION_INPUTS.md` lists the two files
other lanes read from it.

## Reproduce

```sh
cd infra/immigration-fiscal/assumption_explorer_2026_09_21
uv run --no-project --with duckdb --with pandas --with numpy python3 build_model.py   # hash-guards upstream
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl --with numpy python3 scaling_check.py
node test_engine.js
```

`test_engine.js` also reads the September 23, 24 and 26 main-case lanes' bands and payloads, which stay
in git as the engine's regression record. The live case's own gates are in its lane
(`infra/immigration-fiscal/live_case.json` names it).

## Gates

`test_engine.js` ends `PASS: 2629 grid rows, 60 service cases, 32 accounting cases, 4 headline bounds,
12 lane bands (central: September 23 203.2070 to 249.6400 bn, September 24 200.8752 to 246.3184 bn,
September 26 200.9180 to 245.6949 bn), attribution closure, 532 corrected shares on their base; worst
gap 4.28e-9 bn`. The share-base check holds that `applyCorrections` moves an edited cell's target only
with its line's national total, and that a cell with a national amount of zero stays zero.

## Evidence for general government

The published account held defense **and** general government at zero response. The engine separates
the two (`general_government_response`). `scaling_check.py` gives the evidence for treating them
differently [CALCULATION: scaling_check.py -> derived/scaling_check.json]:

- BEA Table 3.16, 2024: general public service outside interest is 475.8 bn, 63% of it state and
  local. Federal tax collection and financial management is 36.6 bn; federal executive and
  legislative 137.9 bn. [DATA: bea_nipa/Section3All_xls.xlsx, T31600-A lines 3, 4, 6, 44, 45, 47]
- Across the 50 states (FY2022), log spending on log population: governmental administration
  0.842 (se 0.039), financial administration 0.789, judicial 0.951; for comparison police 1.041,
  correction 0.975, K-12 0.983. [DATA: _cache/slf2022.xlsx, Census State and Local Government
  Finance Table 1, sha256 4dd123c5...643b9b; census_popest_2024/NST-EST2024-ALLDATA.csv]
- Marginal rates 0.59 (federal executive and legislative fixed, federal tax collection at 0.789,
  state and local at 0.842) to 0.84 (everything at 0.842). The case reads them over a removal of the
  group's size, 12.9% of residents, under a power-law cost: 0.6005 to 0.8511 of average cost
  ([decision](../../../decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md)).
  [INFERENCE: a cross-section shows long-run scale, not a measured response to this group]
- Federal police, courts and prisons (82.8 bn, FBI included) are charged inside
  `public_order_safety`, by use; this is not an added cost. Defense and interest on debt already
  issued stay at zero.

## Limits

- The production block is CES; increasing-returns arguments are outside it.
- One income year of the account (2024). No generation split, lifetime value or policy effect: those
  are other lanes' work.

## Deleted 2026-10-15 (tombstones)

The operator retired the explorer page on 2026-10-15 ("you can delete map and explorer ... unneeded";
the map stays). The page was last on main case v6, adopted 2026-10-07, and its central preset gave
389.0826–461.4797 bn as loaded. Its case loader, presets, citation registry, cards, ladder section and
build briefs went with it. The checks of `case.js` and `presets.json` against v6 left `test_engine.js`
in the same change. Recover a file with `git show <last commit>:<path>`. Every one is also on GitHub
at origin/main ed8fc58b, as is this README's last version for the page (116ed758).

| Path | Last commit |
|---|---|
| `BRIEF.md` | `e9b03235` (2026-09-23) |
| `BRIEF_context.md` | `b741e4f5` (2026-09-23) |
| `BRIEF_corrections.md` | `2ca1a15e` (2026-09-24) |
| `build_context.py` | `9daa64b4` (2026-10-08) |
| `build_ui.py` | `116ed758` (2026-10-08) |
| `cards/build_inventory.py` | `ca86dde8` (2026-10-08) |
| `cards/reanchor.py` | `a072a06d` (2026-09-27) |
| `case.js` | `116ed758` (2026-10-08) |
| `check_sources.py` | `e9b03235` (2026-09-23) |
| `context.json` | `ca86dde8` (2026-10-08) |
| `ladder.py` | `ccf10617` (2026-09-21) |
| `presets.json` | `116ed758` (2026-10-08) |
| `sources.json` | `116ed758` (2026-10-08) |
| `sources_check.json` | `116ed758` (2026-10-08) |
| `template.html` | `116ed758` (2026-10-08) |
| `ui.js` | `116ed758` (2026-10-08) |

The ignored build of the page (`derived/explorer.html`) and its screenshots were removed from this
machine. The figures page's frozen prototypes read `presets.json` at its pin through git
(`figures_2026_09_22/account_sept24.cjs`), so they still build.
