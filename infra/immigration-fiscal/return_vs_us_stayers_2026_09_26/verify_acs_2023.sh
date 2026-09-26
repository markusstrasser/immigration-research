#!/usr/bin/env bash
# Verify the repository's held ACS 2023 1-year person PUMS zip against the file Census serves
# today, without a second 597 MB download.
#
# The brief assumed the 2023 person file was not local and asked for a fetch into
# acs_pums_years/csv_pus_2023.zip. It is held at census/acs_pums_2023_person.zip, acquired by
# acquire/setup.sh from the same URL, and a direct fetch ran at about 27 kB/s on 2026-09-26
# (six hours), so this script checks the held copy instead:
#   1. its size equals the served Content-Length;
#   2. the last 4 KiB (the zip central directory: every member's CRC-32 and sizes) and sixteen
#      16 KiB ranges spread across the file are byte-identical to HTTP range reads of the served file;
#   3. `unzip -tqq` passes (every member matches its CRC-32);
#   4. its sha256 equals the one service_by_ses_2026_09_23/derived/acs_inputs.json recorded.
# Writes nothing outside a temporary directory. Exit 0 only if all four hold.
set -euo pipefail
# lane → immigration-fiscal → infra → repo root
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
HELD="$ROOT/sources/immigration-fiscal/data/census/acs_pums_2023_person.zip"
URL="https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/csv_pus.zip"
RECORDED_SHA="98b6ecb14b4830d1f2b54c265a5bd997828415c2dab14e17369c40e98b78d9d4"
CHUNK=16384
N_CHUNKS=16

fail() { echo "[fail] $*" >&2; exit 1; }

[[ -f "$HELD" ]] || fail "missing $HELD; acquire it with infra/immigration-fiscal/acquire/setup.sh"
size="$(stat -f %z "$HELD")"
served="$(curl -sS --http1.1 -I "$URL" | awk 'tolower($1)=="content-length:"{print $2}' | tr -d '\r')"
[[ -n "$served" ]] || fail "no Content-Length from $URL"
[[ "$served" == "$size" ]] || fail "size: held $size, served $served"
echo "[size] held = served = $size bytes"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
# --max-filesize stops curl if the server ignores Range and starts sending the whole file.
get_range() { curl -sS --http1.1 --fail --max-filesize 1048576 -r "$1" -o "$2" "$URL"; }

get_range "-4096" "$tmp/served_tail"
tail -c 4096 "$HELD" > "$tmp/held_tail"
cmp -s "$tmp/served_tail" "$tmp/held_tail" || fail "last 4096 bytes (central directory) differ"
echo "[range] central directory (last 4096 bytes) identical"

step=$(( size / N_CHUNKS / CHUNK ))
for k in $(seq 0 $(( N_CHUNKS - 1 ))); do
  block=$(( k * step ))
  off=$(( block * CHUNK ))
  get_range "$off-$(( off + CHUNK - 1 ))" "$tmp/served_$k"
  dd if="$HELD" of="$tmp/held_$k" bs="$CHUNK" skip="$block" count=1 2>/dev/null
  [[ "$(stat -f %z "$tmp/served_$k")" == "$CHUNK" ]] || fail "range at $off returned a short body"
  cmp -s "$tmp/served_$k" "$tmp/held_$k" || fail "bytes at offset $off differ"
done
echo "[range] $N_CHUNKS ranges of $CHUNK bytes identical"

unzip -tqq "$HELD" || fail "zip CRC check"
echo "[crc] unzip -tqq passed"

sha="$(shasum -a 256 "$HELD" | awk '{print $1}')"
[[ "$sha" == "$RECORDED_SHA" ]] || fail "sha256 $sha != recorded $RECORDED_SHA"
echo "[ok] census/acs_pums_2023_person.zip verified against $URL sha256=$sha"
