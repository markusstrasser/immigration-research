#!/usr/bin/env bash
# Shared config loader for immigration-fiscal acquire/build scripts.
immigration_fiscal_load_config() {
    local acquire_dir
    # Fail loud instead of resolving to the cwd: under zsh/sh BASH_SOURCE is unset, which
    # silently pointed every data root at $HOME (2026-09-16 recovery probe).
    if [[ -z "${BASH_SOURCE[0]:-}" ]]; then
        echo "immigration_fiscal_load_config: BASH_SOURCE is unset; run entry points with bash (bash ./reproduce.sh ...), not zsh or sh" >&2
        return 1
    fi
    acquire_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [[ ! -f "$acquire_dir/config.env.example" ]]; then
        echo "immigration_fiscal_load_config: resolved acquire dir $acquire_dir has no config.env.example; refusing to guess data roots" >&2
        return 1
    fi
    IMMIGRATION_FISCAL_ROOT="$(cd "$acquire_dir/.." && pwd)"
    if [[ -f "$acquire_dir/config.local.env" ]]; then
        # shellcheck source=config.local.env
        source "$acquire_dir/config.local.env"
    elif [[ -f "$acquire_dir/config.env" ]]; then
        # shellcheck source=config.env
        source "$acquire_dir/config.env"
    fi
    # Apply shared defaults after optional overrides; preserve caller-provided values.
    # shellcheck source=config.env.example
    source "$acquire_dir/config.env.example"
    export IMMIGRATION_FISCAL_ROOT
    export REPO_ROOT="${REPO_ROOT:-$(cd "$IMMIGRATION_FISCAL_ROOT/../.." && pwd)}"
    export DUCKDB_PATH="${DUCKDB_PATH:-$REPO_ROOT/warehouse/immigration_context.duckdb}"
    export LIFETIME_DUCKDB_PATH="${LIFETIME_DUCKDB_PATH:-$REPO_ROOT/warehouse/immigration_lifetime_evidence.duckdb}"
    export FISCAL_UNION_DUCKDB_PATH="${FISCAL_UNION_DUCKDB_PATH:-$REPO_ROOT/warehouse/immigration_fiscal_union.duckdb}"
    export IMMIGRATION_CAUSAL_DATA="${IMMIGRATION_CAUSAL_DATA:-$REPO_ROOT/sources/immigration-causal/data}"
}
