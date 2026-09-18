#!/usr/bin/env bash
# Reproducibility gate: re-run every analysis script from scratch into a scratch copy of
# derived/ and cmp each file against the committed one. Exits non-zero on any difference.
# Usage: bash scripts/verify.sh
set -uo pipefail
LANE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SNAP="$LANE/_cache/derived_run1"
UV=(uv run --no-project --with "pandas>=2" --with "numpy>=2")

[[ -d "$LANE/derived" ]] || { echo "[FAIL] no derived/ to verify" >&2; exit 2; }
rm -rf "$SNAP"; cp -R "$LANE/derived" "$SNAP"

cd "$LANE" || exit 2
rm -f derived/*.csv derived/*.txt
rc=0
PYTHONUNBUFFERED=1 "${UV[@]}" python3 scripts/analyze_voting.py    > /dev/null || rc=1
PYTHONUNBUFFERED=1 "${UV[@]}" python3 scripts/analyze_volunteer.py > /dev/null || rc=1
PYTHONUNBUFFERED=1 "${UV[@]}" python3 scripts/asec_entry.py        > /dev/null || rc=1
PYTHONUNBUFFERED=1 "${UV[@]}" --with statsmodels python3 scripts/regressions.py > /dev/null || rc=1
PYTHONUNBUFFERED=1 "${UV[@]}" python3 scripts/summary.py          > /dev/null || rc=1
[[ $rc == 0 ]] || { echo "[FAIL] a script errored on the second run" >&2; exit 1; }

fail=0
for f in "$SNAP"/*; do
  b=$(basename "$f")
  if cmp -s "$f" "derived/$b"; then echo "  cmp OK   $b"
  else echo "  cmp DIFF $b"; fail=1; fi
done
for f in derived/*; do
  b=$(basename "$f"); [[ -e "$SNAP/$b" ]] || { echo "  NEW      $b (absent from run 1)"; fail=1; }
done
[[ $fail == 0 ]] && echo "[PASS] derived/ reproduces byte-identically" || echo "[FAIL] derived/ differs" >&2
exit $fail
