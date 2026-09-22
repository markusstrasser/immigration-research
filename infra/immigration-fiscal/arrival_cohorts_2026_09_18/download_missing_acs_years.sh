#!/usr/bin/env bash
# Download missing ACS 1-year person PUMS zips into acs_pums_years/.
# HTTP/1.1, no resume of unverified parts (2013 .part was a prefixed corrupt body).
set -euo pipefail
# lane → immigration-fiscal → infra → repo root
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
OUT="$ROOT/sources/immigration-fiscal/data/external/acs_pums_years"
mkdir -p "$OUT"
LOG="$OUT/download.log"

url_for() {
  local y="$1"
  case "$y" in
    2005|2006) echo "https://www2.census.gov/programs-surveys/acs/data/pums/${y}/csv_pus.zip" ;;
    *) echo "https://www2.census.gov/programs-surveys/acs/data/pums/${y}/1-Year/csv_pus.zip" ;;
  esac
}

fetch_one() {
  local y="$1"
  local dest="$OUT/csv_pus_${y}.zip"
  local tmp="$dest.part"
  local url expected sz
  if [[ -f "$dest" ]] && unzip -tqq "$dest"; then
    echo "[skip] $y already verified" | tee -a "$LOG"
    return 0
  fi
  url="$(url_for "$y")"
  expected="$(curl -sS --http1.1 -I "$url" | awk 'tolower($1)=="content-length:"{print $2}' | tr -d '\r')"
  if [[ -z "$expected" || "$expected" -lt 1000000 ]]; then
    echo "[fail] $y no Content-Length from $url" | tee -a "$LOG"
    return 1
  fi
  echo "[get] $y expected=$expected" | tee -a "$LOG"
  rm -f "$tmp"
  curl --http1.1 --fail --location --retry 3 --retry-delay 5 \
    --output "$tmp" "$url"
  sz="$(stat -f %z "$tmp")"
  if [[ "$sz" != "$expected" ]]; then
    echo "[fail] $y size $sz != $expected" | tee -a "$LOG"
    rm -f "$tmp"
    return 1
  fi
  if ! unzip -tqq "$tmp"; then
    echo "[fail] $y zip CRC" | tee -a "$LOG"
    rm -f "$tmp"
    return 1
  fi
  mv "$tmp" "$dest"
  echo "[ok] $y $sz sha=$(shasum -a 256 "$dest" | awk '{print $1}')" | tee -a "$LOG"
}

# Missing 1-year person files. Skip 2013/2019/2023/2024 (held) and 2020 (no 1-year).
YEARS=(2005 2006 2007 2008 2009 2010 2011 2012 2014 2015 2016 2017 2018 2021 2022)
fail=0
for y in "${YEARS[@]}"; do
  if ! fetch_one "$y"; then
    fail=$((fail + 1))
  fi
done
echo "[done] failures=$fail" | tee -a "$LOG"
exit "$fail"
