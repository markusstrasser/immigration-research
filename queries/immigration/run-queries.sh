#!/usr/bin/env bash
# Run checked-in immigration SQL against local DuckDB warehouses.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
INFRA="$REPO/infra/immigration-fiscal"
CFG="$INFRA/acquire/config.local.env"

if [[ -f "$CFG" ]]; then
  # shellcheck source=/dev/null
  source "$CFG"
fi
# shellcheck source=/dev/null
source "$INFRA/acquire/lib.sh" 2>/dev/null || true
immigration_fiscal_load_config 2>/dev/null || true

CTX="${DUCKDB_PATH:-$REPO/warehouse/immigration_context.duckdb}"
UNION="${FISCAL_UNION_DUCKDB_PATH:-$REPO/warehouse/immigration_fiscal_union.duckdb}"
LIFE="${LIFETIME_DUCKDB_PATH:-$REPO/warehouse/immigration_lifetime_evidence.duckdb}"

FILTER="${1:-all}"

_run_sql_file() {
  local db="$1" sql_path="$2" mode="$3"
  shift 3
  uv run --with duckdb python - "$db" "$sql_path" "$mode" "$@" <<'PY'
import sys
import duckdb
from pathlib import Path

db, path, mode = sys.argv[1], sys.argv[2], sys.argv[3]
extra = sys.argv[4:]
raw = open(path).read()
optional = "optional:" in raw.lower()
body = "\n".join(line for line in raw.splitlines() if not line.strip().startswith("--"))
parts = [p.strip() for p in body.split(";") if p.strip()]
con = duckdb.connect(db, read_only=True)
if mode == "union":
    ctx, life = extra[0], extra[1]
    if Path(ctx).exists():
        con.execute(f"ATTACH '{ctx}' AS ctx (READ_ONLY)")
    if Path(life).exists():
        con.execute(f"ATTACH '{life}' AS life (READ_ONLY)")
try:
    for i, stmt in enumerate(parts):
        if len(parts) > 1:
            print(f"-- statement {i + 1}/{len(parts)}")
        res = con.execute(stmt)
        if res.description:
            cols = [d[0] for d in res.description]
            rows = res.fetchall()
            print(" | ".join(cols))
            print("-" * 72)
            for row in rows[:40]:
                print(" | ".join(str(x) for x in row))
            if len(rows) > 40:
                print(f"... ({len(rows) - 40} more rows)")
except Exception as e:
    if optional:
        print(f"SKIP (optional): {e}")
    else:
        print(f"ERROR: {e}", file=sys.stderr)
        raise
PY
}

_run_context() {
  local sql="$1"
  local name
  name="$(basename "$sql")"
  [[ -f "$CTX" ]] || { echo "MISSING $CTX — run: ./scripts/reproduce-immigration-data.sh build context"; return 1; }
  echo ""
  echo "=== $name (context) ==="
  _run_sql_file "$CTX" "$sql" context
}

_run_union() {
  local sql="$1"
  local name
  name="$(basename "$sql")"
  [[ -f "$UNION" ]] || { echo "MISSING $UNION — run: ./scripts/reproduce-immigration-data.sh build all"; return 1; }
  echo ""
  echo "=== $name (union) ==="
  _run_sql_file "$UNION" "$sql" union "$CTX" "$LIFE"
}

for sql in "$HERE"/context_*.sql; do
  [[ -f "$sql" ]] || continue
  [[ "$FILTER" == all || "$FILTER" == context ]] || continue
  _run_context "$sql"
done

for sql in "$HERE"/union_*.sql; do
  [[ -f "$sql" ]] || continue
  [[ "$FILTER" == all || "$FILTER" == union ]] || continue
  _run_union "$sql"
done

echo ""
echo "done."
