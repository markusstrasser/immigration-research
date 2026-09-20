#!/usr/bin/env bash
# Read-only checks. Staged payloads use their intended filename for format selection.
# full tests ZIP member CRCs; directory checks metadata only (fast manifest audit).
immigration_fiscal_validate_file() {
    local file="$1" min_bytes="${2:-512}" intended="${3:-$1}" mode="${4:-full}"
    local size
    [[ -f "$file" ]] || { echo "INVALID missing file: $file" >&2; return 1; }
    size=$(wc -c < "$file" | tr -d ' ')
    [[ "$size" -ge "$min_bytes" ]] || {
        echo "TOO_SMALL $file (${size}B < ${min_bytes}B)" >&2; return 1;
    }
    # Also protect callers that have not supplied the final name explicitly.
    intended="${intended%.part}"
    case "$intended" in
        *.zip|*.xlsx)
            case "$mode" in
                full) unzip -tqq "$file" >/dev/null 2>&1 && return 0 ;;
                directory) unzip -Z -t "$file" >/dev/null 2>&1 && return 0 ;;
                *) echo "INVALID validation mode: $mode" >&2; return 1 ;;
            esac
            ;;
        *.pdf) [[ "$(head -c 5 "$file")" == '%PDF-' ]] && return 0 ;;
        *.json)
            python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$file" \
                >/dev/null 2>&1 && return 0
            ;;
        *) return 0 ;;
    esac
    echo "INVALID $file (expected ${intended##*.}, mode=$mode)" >&2
    return 1
}
