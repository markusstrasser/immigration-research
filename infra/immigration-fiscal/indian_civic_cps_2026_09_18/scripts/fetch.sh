#!/usr/bin/env bash
# Cached fetcher for this lane. Retries with HTTP/1.1 + resume (census.gov truncates under HTTP/2).
# Usage: fetch.sh <url> <dest> [expected_min_bytes]
set -uo pipefail
url="$1"; dest="$2"; minb="${3:-1024}"
mkdir -p "$(dirname "$dest")"
if [[ -s "$dest" && $(wc -c < "$dest") -ge $minb ]]; then echo "[cached] $dest ($(wc -c < "$dest") B)"; exit 0; fi
for try in 1 2 3 4 5; do
  code=$(curl -s --http1.1 -C - --max-time 300 --retry 2 -o "$dest" -w "%{http_code}" "$url")
  n=$(wc -c < "$dest" 2>/dev/null || echo 0)
  if [[ "$code" == "200" || "$code" == "206" ]] && [[ $n -ge $minb ]]; then echo "[ok try$try] $dest ($n B)"; exit 0; fi
  echo "[retry $try] http=$code bytes=$n" >&2
  [[ "$code" == "404" ]] && { echo "[404] $url" >&2; exit 4; }
done
echo "[FAIL] $url -> $dest (last http=$code bytes=$n)" >&2; exit 1
