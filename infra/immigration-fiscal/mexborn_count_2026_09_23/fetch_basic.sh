#!/usr/bin/env bash
# Fetch CPS basic monthly public-use zips, Jan 2024 to the latest posted month, into _cache/basic/.
# October 2025 was never collected (federal shutdown) and is not posted.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/_cache/basic"
mkdir -p "$OUT"
BASE=https://www2.census.gov/programs-surveys/cps/datasets
for y in 24 25 26; do
  for m in jan feb mar apr may jun jul aug sep oct nov dec; do
    f="${m}${y}pub.zip"
    url="$BASE/20$y/basic/$f"
    if [ -s "$OUT/$f" ] && unzip -tq "$OUT/$f" >/dev/null 2>&1; then echo "have $f"; continue; fi
    code=$(curl -s -o /dev/null -w '%{http_code}' -I -m 30 "$url")
    if [ "$code" != "200" ]; then echo "skip $f http=$code"; continue; fi
    curl -s --retry 4 --retry-delay 5 -m 600 -o "$OUT/$f.part" "$url" && mv "$OUT/$f.part" "$OUT/$f"
    if unzip -tq "$OUT/$f" >/dev/null 2>&1; then echo "ok $f $(stat -f %z "$OUT/$f")"; else echo "BAD $f"; fi
  done
done
echo DONE
