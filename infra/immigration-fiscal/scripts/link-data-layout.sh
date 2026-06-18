#!/usr/bin/env bash
# Symlink sources/immigration-fiscal/data -> PNY_DATA_ROOT when sources/ is in-repo.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=../acquire/lib.sh
source "$ROOT/acquire/lib.sh"
immigration_fiscal_load_config

mkdir -p "$PNY_DATA_ROOT" "$DERIVED_ROOT" "$(dirname "$DUCKDB_PATH")"

sources_root="$REPO_ROOT/sources"
if [[ -L "$sources_root" ]]; then
    echo "sources is external symlink ($sources_root)"
    echo "Set PNY_DATA_ROOT in acquire/config.local.env — no in-repo data link."
    echo "  PNY_DATA_ROOT=$PNY_DATA_ROOT"
    exit 0
fi

link="$sources_root/immigration-fiscal/data"
mkdir -p "$(dirname "$link")"
if [[ -e "$link" && ! -L "$link" ]]; then
    echo "ERROR: $link exists and is not a symlink — move aside or set PNY_DATA_ROOT only." >&2
    exit 1
fi
ln -sfn "$PNY_DATA_ROOT" "$link"
echo "linked $link -> $PNY_DATA_ROOT"

derived_link="$sources_root/immigration-fiscal/data/derived"
if [[ ! -e "$derived_link" ]]; then
    mkdir -p "$DERIVED_ROOT"
    ln -sfn "$DERIVED_ROOT" "$derived_link"
    echo "linked $derived_link -> $DERIVED_ROOT"
fi
