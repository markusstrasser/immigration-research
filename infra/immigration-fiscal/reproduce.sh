#!/usr/bin/env bash
# End-to-end reproducibility for immigration-fiscal (+ optional causal stack).
#
#   ./reproduce.sh init              # config + dirs + data symlink
#   ./reproduce.sh doctor            # deps + resolved paths
#   ./reproduce.sh download [tier]    # minimal | standard (default) | full
#   ./reproduce.sh verify [tier]      # required | optional | all | derived
#   ./reproduce.sh build [target]     # context | mvp | lifetime | unified | all
#   ./reproduce.sh all [tier]         # download + verify required + build all
#   ./reproduce.sh query [filter]    # headline SQL (all | context | union | life)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$ROOT/../.." && pwd)"
# shellcheck source=acquire/lib.sh
source "$ROOT/acquire/lib.sh"

_usage() {
    cat <<'EOF'
Usage: reproduce.sh <command> [tier|target]

Commands:
  init                 Create config.local.env, data dirs, optional sources/ symlink
  doctor               Check tools and print resolved paths
  download [tier]      minimal (~2GB) | standard (~50GB attempts) | full (+tier-a, causal)
  verify [tier]        required (default) | optional | all | derived
  build [target]       context | mvp | lifetime | unified | all (default)
  query [filter]         Run headline SQL (all | context | union | life)
  all [tier]           download + verify required + build all
  smoke                minimal pipeline smoke test

Tiers:
  minimal    ACS 2023 PUMS + CPS ASEC only (warehouse minimum)
  standard   Public fiscal stack + stage2/3/5 attempts + lifetime PDFs
  full       standard + tier-a labor panels + immigration-causal setup

Manual / WAF-blocked list (after download):
  $PNY_DATA_ROOT/external/stage5_net_negative/kff_refs/MANUAL_ACQUIRE.md
  $PNY_DATA_ROOT/external/lifetime/applications/MANUAL_ACQUIRE.md
EOF
}

_cmd_init() {
    local cfg="$ROOT/acquire/config.local.env"
    if [[ ! -f "$cfg" ]]; then
        cp "$ROOT/acquire/config.env.example" "$cfg"
        echo "created $cfg (edit paths if needed)"
    else
        echo "exists $cfg"
    fi
    # shellcheck source=acquire/config.local.env
    source "$cfg"
    immigration_fiscal_load_config
    mkdir -p "$PNY_DATA_ROOT" "$DERIVED_ROOT" "$CORPUS_ROOT" "$(dirname "$DUCKDB_PATH")"
    bash "$ROOT/scripts/link-data-layout.sh"
}

_cmd_doctor() {
    immigration_fiscal_load_config
    local ok=0
    for bin in bash curl unzip; do
        if command -v "$bin" >/dev/null 2>&1; then echo "ok  $bin"; else echo "MISSING $bin"; ok=1; fi
    done
    if command -v uv >/dev/null 2>&1; then echo "ok  uv"; else echo "WARN uv not found (needed for build)"; fi
    [[ -f "$ROOT/acquire/config.local.env" ]] || { echo "WARN no config.local.env — run: ./reproduce.sh init"; }
    cat <<EOF

Paths:
  REPO_ROOT              $REPO_ROOT
  PNY_DATA_ROOT          $PNY_DATA_ROOT
  DERIVED_ROOT           $DERIVED_ROOT
  CORPUS_ROOT            $CORPUS_ROOT
  DUCKDB_PATH            $DUCKDB_PATH
  LIFETIME_DUCKDB_PATH   $LIFETIME_DUCKDB_PATH
  FISCAL_UNION_DUCKDB_PATH $FISCAL_UNION_DUCKDB_PATH
  IMMIGRATION_CAUSAL_DATA $IMMIGRATION_CAUSAL_DATA
EOF
    return "$ok"
}

_cmd_download() {
    local tier="${1:-standard}"
    immigration_fiscal_load_config
    export REPRODUCE_TIER="$tier"
    bash "$ROOT/acquire/setup.sh"
    if [[ "$tier" == "full" ]]; then
        bash "$ROOT/acquire/setup-tier-a-labor-demography.sh" || true
        bash "$ROOT/acquire/setup-restrictionist-panels.sh" || true
        local causal_setup="$REPO_ROOT/sources/immigration-causal/setup.sh"
        [[ -f "$causal_setup" ]] || causal_setup="$(dirname "$IMMIGRATION_CAUSAL_DATA")/setup.sh"
        if [[ -f "$causal_setup" ]]; then
            bash "$causal_setup" || true
        else
            echo "WARN immigration-causal/setup.sh not found — skip causal downloads"
        fi
    fi
}

_cmd_verify() {
    local tier="${1:-required}"
    immigration_fiscal_load_config
    bash "$ROOT/scripts/verify-downloads.sh" --tier "$tier"
}

_cmd_build() {
    local target="${1:-all}"
    immigration_fiscal_load_config
    export PNY_DATA_ROOT DERIVED_ROOT DUCKDB_PATH CORPUS_ROOT
    export LIFETIME_DUCKDB_PATH FISCAL_UNION_DUCKDB_PATH IMMIGRATION_CAUSAL_DATA UNIFIED_DUCKDB_PATH
    case "$target" in
        context) bash "$ROOT/rebuild.sh" ;;
        mvp) bash "$ROOT/rebuild_mvp.sh" ;;
        lifetime) bash "$ROOT/rebuild_lifetime_warehouse.sh" ;;
        unified) uv run --with duckdb python "$ROOT/build/build_unified_warehouse.py" ;;
        all)
            bash "$ROOT/rebuild.sh"
            bash "$ROOT/rebuild_mvp.sh"
            bash "$ROOT/rebuild_lifetime_warehouse.sh"
            uv run --with duckdb python "$ROOT/build/build_unified_warehouse.py"
            ;;
        *) echo "unknown build target: $target" >&2; exit 2 ;;
    esac
}

_cmd_smoke() {
    immigration_fiscal_load_config
    export PNY_DATA_ROOT DERIVED_ROOT DUCKDB_PATH
    _cmd_download minimal
    _cmd_verify required
    _cmd_build context
    uv run --with duckdb python - <<PY
import duckdb
p = "${DUCKDB_PATH}"
c = duckdb.connect(p, read_only=True)
n = c.execute("SELECT COUNT(*) FROM information_schema.tables").fetchone()[0]
print(f"smoke ok: {p} tables={n}")
assert n > 0
PY
}

_cmd_query() {
    local filter="${1:-all}"
    bash "$REPO_ROOT/queries/immigration/run-queries.sh" "$filter"
}

_cmd_all() {
    local tier="${1:-standard}"
    _cmd_download "$tier"
    _cmd_verify required
    _cmd_build all
}

main() {
    immigration_fiscal_load_config
    local cmd="${1:-}"
    shift || true
    case "$cmd" in
        init) _cmd_init ;;
        doctor) _cmd_doctor ;;
        download) _cmd_download "${1:-standard}" ;;
        verify) _cmd_verify "${1:-required}" ;;
        build) _cmd_build "${1:-all}" ;;
        query) _cmd_query "${1:-all}" ;;
        all) _cmd_all "${1:-standard}" ;;
        smoke) _cmd_smoke ;;
        ""|-h|--help) _usage ;;
        *) echo "unknown command: $cmd" >&2; _usage; exit 2 ;;
    esac
}

main "$@"
