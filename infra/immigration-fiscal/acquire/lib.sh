#!/usr/bin/env bash
# Shared config loader for immigration-fiscal acquire/build scripts.
immigration_fiscal_load_config() {
    local acquire_dir
    acquire_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    IMMIGRATION_FISCAL_ROOT="$(cd "$acquire_dir/.." && pwd)"
    if [[ -f "$acquire_dir/config.local.env" ]]; then
        # shellcheck source=config.local.env
        source "$acquire_dir/config.local.env"
    elif [[ -f "$acquire_dir/config.env" ]]; then
        # shellcheck source=config.env
        source "$acquire_dir/config.env"
    else
        # shellcheck source=config.env.example
        source "$acquire_dir/config.env.example"
    fi
    export IMMIGRATION_FISCAL_ROOT
    export REPO_ROOT="${REPO_ROOT:-$(cd "$IMMIGRATION_FISCAL_ROOT/../.." && pwd)}"
    export PNY_DATA_ROOT="${PNY_DATA_ROOT:-$HOME/research-data/immigration-fiscal/data}"
    export CORPUS_ROOT="${CORPUS_ROOT:-$HOME/research-data/corpus}"
    export DERIVED_ROOT="${DERIVED_ROOT:-$PNY_DATA_ROOT/derived}"
    export DUCKDB_PATH="${DUCKDB_PATH:-$REPO_ROOT/warehouse/immigration_context.duckdb}"
    export LIFETIME_DUCKDB_PATH="${LIFETIME_DUCKDB_PATH:-$REPO_ROOT/warehouse/immigration_lifetime_evidence.duckdb}"
    export FISCAL_UNION_DUCKDB_PATH="${FISCAL_UNION_DUCKDB_PATH:-$REPO_ROOT/warehouse/immigration_fiscal_union.duckdb}"
    export IMMIGRATION_CAUSAL_DATA="${IMMIGRATION_CAUSAL_DATA:-$REPO_ROOT/sources/immigration-causal/data}"
}
