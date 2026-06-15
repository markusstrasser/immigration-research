#!/usr/bin/env bash
# Verify files from DOWNLOAD_MANIFEST.tsv exist under PNY_DATA_ROOT.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ACQUIRE="$ROOT/acquire"
if [[ -f "$ACQUIRE/config.local.env" ]]; then
    source "$ACQUIRE/config.local.env"
elif [[ -f "$ACQUIRE/config.env" ]]; then
    source "$ACQUIRE/config.env"
else
    source "$ACQUIRE/config.env.example"
fi
MANIFEST="$ROOT/DOWNLOAD_MANIFEST.tsv"
DATA="$PNY_DATA_ROOT"
missing=0
checked=0
while IFS=$'\t' read -r stage req relpath min_bytes script notes; do
    [[ "$stage" == stage ]] && continue  # header
    [[ -z "$relpath" ]] && continue
    dest="$DATA/$relpath"
    checked=$((checked + 1))
    if [[ ! -s "$dest" ]]; then
        echo "MISSING [$req] $relpath"
        missing=$((missing + 1))
        continue
    fi
    sz=$(wc -c < "$dest" | tr -d ' ')
    if [[ "$sz" -lt "${min_bytes:-1}" ]]; then
        echo "TOO_SMALL [$req] $relpath (${sz}B < ${min_bytes}B)"
        missing=$((missing + 1))
    fi
done < "$MANIFEST"
echo "---"
echo "checked $checked paths under $DATA — missing/invalid: $missing"
exit $([[ $missing -eq 0 ]] && echo 0 || echo 1)
