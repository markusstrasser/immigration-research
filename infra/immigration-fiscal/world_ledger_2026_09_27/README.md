# World ledger: oct16 matched cash

The live selector is `oct16` (main case v9). Historical case outputs remain frozen.

The matched-cash source account is **$284.397043 / 352.928831bn** at its fiscal low/high ends, over **44,903,074.086245 people**. At equal weights, complete scope A, the G3+ zero-premium bound and public pension funding share s=1, the modeled annual world gains are:

| Reading | Fiscal low end, $bn | Fiscal high end, $bn |
|---|---:|---:|
| R1 | 327.691732 | 272.950365 |
| R2 | 141.387185 | 112.942631 |
| R3 | 213.678751 | 166.803133 |

These hold the named reading and bound fixed; they are not a confidence interval. s=1 retains the declared P032 funding proxy. [CALCULATION: `inputs/pension_cash_cells_oct16.json.gz` results.cash.oracle_bn; `derived/g2_meta_oct16.json` population.complete_total; `derived/readings_cash_oct16.csv` world_total_bn, scope=A_completed, public_pension_share=1, weighting=equal, g3_bound=zero]

Run from the repository root:

```sh
sh infra/immigration-fiscal/world_ledger_2026_09_27/run_all.sh oct16
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 infra/immigration-fiscal/world_ledger_2026_09_27/check_tests.py
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/world_ledger_2026_09_27 "sh {lane}/run_all.sh oct16" "uv run --no-project python3 -m pytest {lane}/test_v9_contract.py {lane}/test_live_contract.py {lane}/test_case_selection.py {lane}/test_snapshot_scope.py -q"
```

Before the first run after an upstream change, explicitly capture the reviewed source epoch, the native routing declaration and exact source cells. These are setup actions, excluded from a reproducibility replay:

The normal producer route and fresh source/artifact capture require the live
declaration and consumed package to agree on oct16 adoption. Frozen validation
continues to check the original captured bytes independently of the live key.

```sh
uv run --no-project python3 infra/immigration-fiscal/world_ledger_2026_09_27/v9_snapshot.py --capture
uv run --no-project python3 infra/immigration-fiscal/world_ledger_2026_09_27/v9_routing.py --capture
uv run --no-project python3 infra/immigration-fiscal/world_ledger_2026_09_27/v9_artifact.py --capture
```

The concurrent upstream inputs are explicitly `[WORKTREE INPUT]`, identified by SHA256 in `inputs/oct16_source_hashes.json` and verified before and after execution. The parent owns commits. Missing source files, undeclared bytes or changed source hashes stop the route. Committed historical pins keep their original contract.

Donor-source admission also pins the actual joint-tenure call chain, parsed source tables, person/factor inputs, preserved pricing kernels and their complete manifest dependencies. Normal donor export verifies this reviewed epoch before source import and again before publication; it cannot enroll changed builder code by regenerating its receipt. `failure-catalog.md` records the caller trace and negative controls.

`v9_cells.cjs` uses the source generation evaluator and its typed new post parts, including military13, administration14, college15, joint16/17, basket18, rate20 and health21. Count atoms split observed and constructed changes; item17 subtracts item16 from the joint source. Military and health keep their original service parents. Capital changes use the actual selected rate and stay resource costs, outside debt flows. Item19/W09 remain beside. Each generation and fiscal end closes to the principal case at 1e-9bn, in set and cash. The count/tenure production parts of items 16/17 have no measured split between private gains (P) and induced receipts (F); as in the winners lane they stay in A as one unlocated carrier, and the set-basis A, P and F at both end specifications equal winners' `fiscal_specs.csv` at 1e-9bn (until 2026-10-20 an unpinned oct14 union_completion cache split them, moving about $0.03bn from A to F). `inputs/pension_cash_cells_oct16.json.gz` retains the exact cells as deterministic gzip (57 MB of JSON); its pin hashes the JSON content, and every route byte-verifies its replay.

Source IDs use declared nonnumeric semantics and recipient scope. Where the count producer supplies identical declarations for distinct rows, a within-declaration source-record occurrence preserves every row before zero filtering. The occurrence denotes source order, not an identified person or program. Unrelated zero/pension rows cannot relabel a shared capped-program source, and the original strict set/cash source-key and dollar gates remain.

`population_v9` supplies current denominators. The source distribution frame declares its already calibrated ranking weights; the world adapter verifies and restores its raw production weights before row4, then applies the selected calibration exactly once. Observed completion records follow their own factors; synthetic G3+ proxy mass remains fixed. `v9_transport.py` calls the canonical joint tenure builder on calibrated source weights and checks every generation against the final count contract. Its donors carry economic weights; fiscal dollars come from the independent typed source atoms, with no invented average person-price reconstruction.

Zero-response public-good values use the v9 native export's explicitly declared original-key scaffold, with immutable source receipts. Current constructed donor mass and observed calibration changes travel separately; this does not substitute a v8 fiscal account. The economic filename schema remains `oct15`, while filenames and source identities are keyed `oct16`.

The operator's price rule remains in force: cost-valued US services convert their category prices to the US general price level; Mexico's source budgets use Mexico's general GDP-money PPP. Fiscal G/net-cost dollars and source pesos remain unchanged by recipient service pricing. WTP and separately priced service arms retain their explicit exemptions. `test_service_prices.py`, `test_mexico_prices.py` and the live oct16 source-dollar test enforce these distinctions. Mexican budget dollar equivalents use PPP, not a market-exchange-rate conversion.

The existing recipient-value convention also remains: cash, health and social services follow their fiscal effects; education has no separate direct value because its return is in the earnings premium; public goods retain their attributed average-cost value. Thus item13's zero-response military parts contribute zero recipient value under this convention, while zero-response defense retains recipient value. This is a modeling convention, not a measurement of military recipients' willingness to pay. `test_v9_contract.py` distinguishes these cases.

`derived/readings_cash_oct16.csv` contains R1/R2/R3 × personal low/high ends × G3+ zero/upper × eight weightings. A contains all completed members; s=1 is the explicitly `[DEGRADED]` all-public P032 funding proxy, with s=.5/0 beside. R3 retains the MMP same-person parameter interpretation, not a causal low bound. Scope B retains counted members and their observed calibration corrections, excludes constructed recipient/pay/weight components, and keeps complete-lineage effects on others. It has no world total or break-even and enters no A total.

Expanded source components carry their declared proportional-mix convention separately from recipient scope. Employer compensation keeps direct receipts equal across fiscal ends within each generation; only the marked source-mix subtotal follows its selected end. Scope B therefore retains legitimate observed end-specific components without exempting unrelated direct receipts from their gate.

`reading_rows_cash_oct16.csv`, `reading_cells_cash_oct16.csv.gz` and `private_gains_cash_oct16.csv` retain source/scope/end/bound identities. The cells file has 562,428 rows (7.1 times oct15's, 259.5 MB as text, 11.5 MB gzipped): the 72 scenarios and 449 lines are oct15's, but v9's count and tenure items add counted and constructed coverage components, each carried across every recipient line. Source component JSON is stored once; scalar output cells retain the source class. `residual_convention_cash_oct16.csv` compares the signed proportional residual mix against zero recipient value at the same fiscal cost. `readings_v7_bridge_oct16.csv` compares frozen v7 readings with current matched cash; it includes pension timing and all implemented case/compensation/price changes, not a v9-only effect.

Full accrual remains `[BLOCKED]` for missing Mexico contribution histories and the public service-cost bridge. Debt recipes remain `[BLOCKED: no oct16 federal split]` and enter no reading total. The source health program/exposure bridge remains provisional. These modeled world readings inherit the case's static-removal and donor-counterfactual assumptions; they are not measured historical effects.

Producer exit codes stay in `derived/route_oct16.json`; `performance.md` and `failure-catalog.md` retain timing, memory and repair evidence. The historical path inventory is preserved byte for byte in `changed-paths.md`; no Git write belongs to this worker.
