#!/bin/bash
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)"
OUT=/Users/alien/Projects/immigration-research/research/immigration-school-flight-and-public-goods-2026-09-18.md
: > "$OUT.tmp"
for f in "$D"/_parts/*.md; do cat "$f" >> "$OUT.tmp"; printf '\n' >> "$OUT.tmp"; done
mv "$OUT.tmp" "$OUT"
wc -l "$OUT"
