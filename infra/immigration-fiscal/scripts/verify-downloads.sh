#!/usr/bin/env bash
# Verify files from DOWNLOAD_MANIFEST.tsv exist under PNY_DATA_ROOT.
# Usage: verify-downloads.sh [--tier required|optional|all|derived]
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=../acquire/lib.sh
source "$ROOT/acquire/lib.sh"
# shellcheck source=../acquire/validation.sh
source "$ROOT/acquire/validation.sh"
immigration_fiscal_load_config

TIER="required"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --tier) TIER="${2:?}"; shift 2 ;;
        -h|--help)
            echo "Usage: $0 [--tier required|optional|all|derived]"
            exit 0 ;;
        *) echo "unknown arg: $1" >&2; exit 2 ;;
    esac
done
case "$TIER" in
    required|optional|all|derived) ;;
    *) echo "bad tier: $TIER" >&2; exit 2 ;;
esac

MANIFEST="$ROOT/DOWNLOAD_MANIFEST.tsv"
DATA="$PNY_DATA_ROOT"
missing=0
checked=0
skipped=0

_should_check() {
    local req="$1" script="$2"
    if [[ "$TIER" == derived ]]; then
        [[ "$script" == build || "$script" == compose ]]
        return
    fi
    case "$script" in build|compose) return 1 ;; esac
    case "$TIER" in
        required) [[ "$req" == required ]] ;;
        optional) [[ "$req" == required || "$req" == optional ]] ;;
        all) [[ "$req" == required || "$req" == optional || "$req" == blocked ]] ;;
    esac
}

while IFS=$'\t' read -r stage req relpath min_bytes script notes; do
    [[ "$stage" == stage ]] && continue
    [[ -z "$relpath" ]] && continue
    if ! _should_check "$req" "$script"; then
        skipped=$((skipped + 1))
        continue
    fi
    dest="$DATA/$relpath"
    if [[ "$script" == build || "$script" == compose ]]; then
        dest="$DERIVED_ROOT/${relpath#derived/}"
        [[ "$relpath" == derived/* ]] || dest="$DERIVED_ROOT/$relpath"
    fi
    checked=$((checked + 1))
    if [[ ! -s "$dest" ]]; then
        echo "MISSING [$req/$script] $dest"
        missing=$((missing + 1))
        continue
    fi
    sz=$(wc -c < "$dest" | tr -d ' ')
    if [[ "$sz" -lt "${min_bytes:-1}" ]]; then
        echo "TOO_SMALL [$req] $dest (${sz}B < ${min_bytes}B)"
        missing=$((missing + 1))
    elif ! immigration_fiscal_validate_file "$dest" "${min_bytes:-1}" "$dest" directory; then
        echo "INVALID [$req/$script] $dest"
        missing=$((missing + 1))
    fi
done < "$MANIFEST"

echo "---"
echo "tier=$TIER data=$DATA derived=$DERIVED_ROOT"
echo "ZIP validation: central directory only; acquisition checks member CRCs"
echo "checked $checked skipped $skipped — missing/invalid: $missing"
if [[ "$checked" -eq 0 ]]; then
    echo "No manifest entries selected for tier=$TIER; verification is incomplete" >&2
    exit 1
fi
exit $([[ $missing -eq 0 ]] && echo 0 || echo 1)
