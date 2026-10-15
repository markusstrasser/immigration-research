# World ledger: matched cash

Run from the repository root. The single selector is the case key (currently `oct15`, v8):

```sh
sh infra/immigration-fiscal/world_ledger_2026_09_27/run_all.sh oct15
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/world_ledger_2026_09_27 "sh {lane}/run_all.sh oct15"
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 infra/immigration-fiscal/world_ledger_2026_09_27/check_tests.py
```

`run_oct15.py --case <key>` threads that selector through the producers. Each registered case needs its own principal/generation/winners/distribution pins, native central coverage export/cache, and exact package cash artifact. No v7 cash or prior-case financing fallback is permitted. A future v9 run is unverified until its upstream exports exist and pass these same contracts; no v9 numbers are claimed here.

Completed-frame economic filenames use the selected case key even when the population schema remains `oct15`. The cash loader takes generation lines directly from that case's exact artifact. Native recipient routing requires `inputs/<key>_final_routing/manifest.json` and its frozen coverage-source receipt (`coverage_routing_dir` / `coverage_source_receipt` may declare other paths in the case pins). The native household producer must support that case; an unknown case stops instead of being relabelled. The historical oct15 receipt name is retained only for oct15.

The route verifies source bytes, runs the set/cash generation core for oct15, exports canonical coverage donors, recomputes compensation and weights, verifies exact package cash cells, transports zero-response recipient values, and executes `cash_readings.py`. The report reads those executed CSVs. Producer failures retain nonzero exit codes in `derived/route_oct15.json`. Timings and physical-memory receipts are in `_cache`; each numerical Python producer enforces the 2.5GB physical-footprint limit.

`derived/readings_cash_oct15.csv` contains R1/R2/R3 × personal low/high ends × G3+ zero/upper × eight weightings. A has all completed members, with s=1 centrally and s=.5/0 beside. P032's all-public s=1 proxy is explicitly `[DEGRADED]`; changing funding never changes recipient payments. R3 retains the MMP same-person parameter interpretation and is not a causal low bound. The recipe table states each reading's fixed prices and assumptions.

Scope B reports counted members' group position beside complete-lineage effects on others. It excludes missed people's group pay, recipient values and weights, discloses their sender debit, enters no A total, and has no complete-world total or break-even. It is not a coverage-off fiscal account.

`reading_rows_cash_oct15.csv`, `reading_cells_cash_oct15.csv` and `private_gains_cash_oct15.csv` share the cash basis and explicit scope/end/bound identities. Cells retain scalar class/source receipts; nested component JSON stays once in the exact artifact and residual-mix contract. `residual_convention_cash_oct15.csv` compares the proportional mix against zero recipient value at the same fiscal cost. The approximately $0.19–0.21bn signed residual fiscal slice is distinct from that priced recipient-value gap.

`readings_status_oct15.csv` retains full accrual as `[BLOCKED]`: Mexico's contribution histories and public service-cost bridge are missing. The separate debt recipes remain `[BLOCKED: no oct15 federal split]` and enter no reading total. Current debt flows may close the case without identifying that split.

`readings_table_cash_oct15.md` contains every reading and its holdings; `readings_v7_bridge_oct15.csv` compares frozen published v7 readings with current cash. That bridge includes pension timing and implemented compensation/G3/capital/price rules as well as v8 items; it is not a v8-only effect. Frozen comparison rows and source receipts are pinned under `inputs/readings_v7_frozen.*`; old live-case files are never regenerated.

The coverage JSON omitted donor IDs/weights. The donor adapter exports the unchanged canonical coverage calculation against its validated native cache, then gates every generation's count and fiscal amount against `sets.cash.scenarios.central`. All economic components use those exact signed weights. G3 calibration uses counted donors before transporting their per-person projections. Zero-response public-good recipient values come from the same native household key routing. These are modelling assumptions, not observations of missing people.

`performance.md` and `failure-catalog.md` preserve the first serializer's failed memory gate and its repair. The main result log is append-only. Every changed path is in `changed-paths.txt`. No git writes belong to this worker.
