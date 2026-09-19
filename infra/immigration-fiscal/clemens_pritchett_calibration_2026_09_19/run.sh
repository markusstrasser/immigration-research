#!/usr/bin/env bash
# Full lane, from the pinned PDF to derived/tables.md. Idempotent: a second run
# leaves derived/ byte-identical.
set -euo pipefail
cd "$(dirname "$0")"

UV="uv run --no-project --with pandas>=2 --with numpy>=2 --with scipy --with openpyxl python3"

echo "[1/6] parse the paper"      ; PYTHONUNBUFFERED=1 $UV parse_paper.py
echo "[2/6] reproduction gate"    ; PYTHONUNBUFFERED=1 $UV gate.py > /dev/null
echo "[3/6] repo parameters"      ; PYTHONUNBUFFERED=1 $UV repo_inputs.py
echo "[4/6] observed rate"        ; PYTHONUNBUFFERED=1 $UV observed_rate.py > /dev/null
echo "[5/6] solve m*"             ; PYTHONUNBUFFERED=1 $UV mstar.py
echo "[6/6] arms and tables"      ; PYTHONUNBUFFERED=1 $UV arms.py > /dev/null
                                    PYTHONUNBUFFERED=1 $UV make_tables.py
echo "done"
