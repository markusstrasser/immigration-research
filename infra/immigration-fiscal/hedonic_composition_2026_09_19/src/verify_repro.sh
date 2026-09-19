#!/usr/bin/env bash
# Re-run every computation step from scratch over the existing cache and prove
# derived/ comes back byte-identical. Network steps are NOT re-run; they are
# idempotent by construction (fetch scripts skip any cache file that parses).
set -euo pipefail
LANE="/Users/alien/Projects/immigration-research/infra/immigration-fiscal/hedonic_composition_2026_09_19"
cd "$LANE"
UV="uv run --no-project --with pandas>=2 --with numpy>=2 --with statsmodels --with scipy"

hash_derived() { find derived -type f | sort | xargs shasum -a 256 | shasum -a 256 | cut -d' ' -f1; }

BEFORE_DIR="$(mktemp -d)"
cp -R derived "$BEFORE_DIR/derived"
H1="$(hash_derived)"
N1="$(find derived -type f | wc -l | tr -d ' ')"
echo "[repro] before: $N1 files, tree sha256 $H1"

rm -rf derived && mkdir derived
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" --with xlrd python3 src/build_geo.py > /dev/null
PYTHONUNBUFFERED=1 $UV python3 src/build_panel.py    > /dev/null
PYTHONUNBUFFERED=1 $UV python3 src/analyze.py        > /dev/null
PYTHONUNBUFFERED=1 $UV python3 src/analyze2.py       > /dev/null
PYTHONUNBUFFERED=1 $UV python3 src/zillow.py         > /dev/null 2>&1
PYTHONUNBUFFERED=1 $UV python3 src/attenuation.py    > /dev/null
PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 src/dollars.py > /dev/null

H2="$(hash_derived)"
N2="$(find derived -type f | wc -l | tr -d ' ')"
echo "[repro] after:  $N2 files, tree sha256 $H2"

RC=0
if [ "$H1" = "$H2" ]; then
  echo "[repro] PASS: derived/ is byte-identical after a from-scratch rebuild"
else
  echo "[repro] FAIL: derived/ differs. Per-file diff:"
  for f in $(cd derived && find . -type f | sort); do
    if ! cmp -s "derived/$f" "$BEFORE_DIR/derived/$f"; then echo "  DIFFERS: $f"; fi
  done
  for f in $(cd "$BEFORE_DIR/derived" && find . -type f | sort); do
    [ -f "derived/$f" ] || echo "  MISSING NOW: $f"
  done
  RC=1
fi
rm -rf "$BEFORE_DIR"
exit $RC
