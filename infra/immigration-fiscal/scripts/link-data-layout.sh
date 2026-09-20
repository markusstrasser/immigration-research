#!/usr/bin/env bash
# Accept the physical project-local layout; link only deliberate external overrides.
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
if [[ "$link" -ef "$PNY_DATA_ROOT" ]]; then
    echo "data root ready: $link"
elif [[ -e "$link" || -L "$link" ]]; then
    echo "ERROR: $link differs from PNY_DATA_ROOT=$PNY_DATA_ROOT; refusing to replace existing data." >&2
    exit 1
else
    ln -s "$PNY_DATA_ROOT" "$link"
    echo "linked $link -> $PNY_DATA_ROOT"
fi

derived_link="$sources_root/immigration-fiscal/data/derived"
if [[ "$derived_link" -ef "$DERIVED_ROOT" ]]; then
    echo "derived root ready: $derived_link"
elif [[ -e "$derived_link" || -L "$derived_link" ]]; then
    echo "ERROR: $derived_link differs from DERIVED_ROOT=$DERIVED_ROOT; refusing to replace it." >&2
    exit 1
else
    if [[ "$PNY_DATA_ROOT" -ef "$sources_root/immigration-fiscal/data" &&
          "$DERIVED_ROOT" -ef "$sources_root/immigration-fiscal/derived" && ! -L "$link" ]]; then
        ln -s ../derived "$derived_link"
    else
        ln -s "$DERIVED_ROOT" "$derived_link"
    fi
    echo "linked $derived_link -> $DERIVED_ROOT"
fi
