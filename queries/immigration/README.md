# Immigration headline queries

Checked-in SQL that backs claims in the verified-findings and June 2026 fiscal memos.

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

Each file starts with `-- requires:` and `-- backs:` comments.

## Expected build

| Query set | Needs |
|-----------|-------|
| `context_*` | `./reproduce.sh build context` |
| `context_06_*` (federal microsim) | `./reproduce.sh build mvp` |
| `context_07_*` | `./reproduce.sh build context` (stage5 base) |
| `context_08_*` (SAFMR/SNAP) | `./reproduce.sh build context` + `setup-net-negative.sh` (optional query) |
| `union_*` | `./reproduce.sh build all` |
