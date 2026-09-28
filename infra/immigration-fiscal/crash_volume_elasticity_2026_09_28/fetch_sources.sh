#!/bin/bash
# Fetch primary sources into _cache/ (ignored). Usage: fetch_sources.sh name=url ...
cd "$(dirname "$0")/_cache" || exit 1
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
fetch_one() {
  curl -sL -A "$UA" --max-time 150 -o "$1" "$2"; rc=$?
  echo "$1 rc=$rc size=$(stat -f %z "$1" 2>/dev/null || echo 0)"
  case "$1" in *.pdf) [ -s "$1" ] && pdftotext -layout "$1" "${1%.pdf}.txt" 2>/dev/null ;; esac
}
for kv in "$@"; do fetch_one "${kv%%=*}" "${kv#*=}" & done
wait
