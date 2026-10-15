**Verdict:** Conditional source-tax measurement and an item19 component; no
identified central correction. Parent chooses adoption and any arm. This lane
does not build a v9 case or change v8. [DATA: `derived/item.json`]

Reproduce from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project --with xlrd python3 infra/immigration-fiscal/passthrough_source_tax_r5_2026_10_15/run.py
uv run --no-project --with xlrd python3 -m pytest infra/immigration-fiscal/passthrough_source_tax_r5_2026_10_15/ -q
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/passthrough_source_tax_r5_2026_10_15 "uv run --no-project --with xlrd python3 {lane}/run.py" "uv run --no-project --with xlrd python3 -m pytest {lane}/test_item.py -q"
```

`xlrd` is needed for the pinned legacy IRS workbooks; no repository dependency
file is changed. Downloads require the extractors' explicit `--acquire`; ordinary
runs verify the pins and are offline. Acquired bytes remain in ignored `_cache/`.
The source catalogs and definitions are pinned alongside the tables. See
`income-evidence.md` and `owner-evidence.md`. [DATA: `inputs/*_pins.json`]

`run.py` executes the income and owner extractors, a fresh frozen job-key replay
redirected entirely into this lane's ignored cache, v8 endpoint evaluation,
measurement and item toggles. It records UTC dates from `date`, Python wall time,
exit codes and child peak RSS in `_cache/run_log.json` and `_cache/runtime.json`.
The frozen replay independently verifies every old output byte and source gate.
No git mutation, upstream lane mutation or secret read occurs. [CALCULATION:
`run.py`, `job_keys.py`]

The item's registry interface is `item.cjs.build(ctx, arm, which)`. The parent
registers ID `passthrough_source_tax`, kind `post_engine`, and lists the returned
`arms()`; `build` returns `edits:[]` and
`meta.passthrough_source_tax.by_end[low|high]`, with `total_bn`, signed
`parts_by_line`, and generation parts. **An omitted arm throws**: `central:null`
is not a measured zero. The parent must add this amount once to its full
post-engine evaluator; the existing v8 evaluator has no knowledge of item19.
`evaluate.cjs` evaluates live v8 with/without this component at specifications16/11
in both methods and both sets and prints all changes to1e-9bn. This verifies the
component arithmetic, not the future parent's v9 registry integration.
[CALCULATION: `item.cjs`, `evaluate.cjs`]

`derived/arms.csv` contains every arm at both endpoints, set and cash, including
per-member changes on the full45,230,062.30075857-person v8 denominator. This
does not imply the numerator has measured missing-person taxes: item12's new
pass-through increment is explicitly withheld. Item10's231 observed completion
records are included on their own wages, industries and enterprise sizes; its
uncertainty is not added to the existing CPS replicate SE. [DATA:
`derived/job_keys.json`, `derived/item.json`, `derived/v8.json`]

W09 is separately reported in `derived/w09.json`. It changes only corporate
receipts; property and production taxes keep off-books wages. The frozen union
plus v6-descendant calculation is exact on the published conditional K1 model;
the v8 completion/coverage extension is explicitly a generation-profile proxy.
It is not stacked automatically into item19. [CALCULATION: `measure.py`]

Sources for parent registration: IRS2022 S Tables6.1/7, partnership Tables1/3/5,
nonfarm Tables1/2; IRS2022/2023 individual Tables1.2/1.4; Census2022 SUSB legal form
by sector and enterprise size (reused K1 pin); Federal Reserve H.15 annual10-year
Treasury yields. Full URLs, hashes, units, industry joins and limitations are in
the source input JSON and the two evidence files. No central geography,
ultimate-owner rate, state-source rate or replacement split is identified.
[DATA: `inputs/income_pins.json`, `inputs/owner_source_pins.json`]
