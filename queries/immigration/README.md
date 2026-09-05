# Immigration headline queries

Checked-in SQL for the current warehouses. September 2026 repairs replace the invalid household-donor fiscal schema; see the [repair report](../../research/immigration-material-repair-report-2026-09-05.md). Successful queries reproduce descriptive/model quantities, not causal certification of historical memo claims.

The annual projection tables are `acs_origin_person_payroll_transfer_microsim_2023` and `acs_nh_white_person_payroll_transfer_microsim_2023`, using `sipp_person_donor_cells_2024` and `sipp_person_donor_cells_usborn_2024`. The historical `usborn` key now means the ACS native definition, including citizenship at birth abroad. `payroll_less_allocated_benefits_proxy_annual` is employee OASDI/HI minus allocated SNAP/TANF/SSI; it is not a full federal balance. Rollups retain `scenario_id` and `unit` so alternative assumptions and price years cannot be summed.

Validated 2026-09-05: all 17 headline files (19 statements) pass with no skips against the repaired canonical warehouses. The separate historical sweep generator's nine SQL diagnostics also pass; its output now goes to `DERIVED_ROOT/sweeps/` and does not revise the research memo automatically.

## Run

From repo root (after `reproduce.sh all standard` or equivalent):

```bash
./scripts/reproduce-immigration-data.sh query
./scripts/reproduce-immigration-data.sh query context   # immigration_context.duckdb only
./scripts/reproduce-immigration-data.sh query union     # fiscal union (+ attaches context + lifetime)
```

Or directly:

```bash
queries/immigration/run-queries.sh
queries/immigration/run-queries.sh union
```

## File naming

| Prefix | Database |
|--------|----------|
| `context_*` | `warehouse/immigration_context.duckdb` |
| `union_*` | `warehouse/immigration_fiscal_union.duckdb` (attaches `ctx` + `life`) |
| `life_*` | `warehouse/immigration_lifetime_evidence.duckdb` |

Each file starts with `-- requires:` and `-- backs:` comments.

## Expected build

| Query set | Needs |
|-----------|-------|
| `context_*` | `./reproduce.sh build context` |
| `context_06_*` (federal microsim) | `./reproduce.sh build mvp` |
| `context_07_*` | `./reproduce.sh build context` (stage5 base) |
| `context_08_*` (SAFMR/SNAP) | `./reproduce.sh build context` + `setup-net-negative.sh` (optional query) |
| `union_*` | `./reproduce.sh build all` |
