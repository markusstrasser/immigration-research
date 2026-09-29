#!/usr/bin/env python3
"""Rerun the lane from scratch and require byte-identical derived outputs.

Hashes every `derived/*.csv|json` (except verify.json), deletes this lane's rebuildable caches
(`_cache/cps_prepared.parquet`, `_cache/acs_india_*.parquet`; `_cache/context/` is left alone),
reruns every step in order, records each exit code, and compares hashes. Writes
`derived/verify.json`; exits 1 on any failed step, changed output or failed gate.

Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb --with pyarrow python3 \
      infra/immigration-fiscal/indian_cohort_selection_2026_09_29/verify.py
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[2]
DER = LANE / "derived"
STEPS = ["acs_extract.py", "cps_cohorts.py", "census_ysm.py", "acs_cohorts.py", "project_g2.py", "stock_language.py"]


def hashes() -> dict[str, str]:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(DER.iterdir()) if p.suffix in (".csv", ".json") and p.name != "verify.json"}


def main() -> int:
    before = hashes()
    for p in [LANE / "_cache" / "cps_prepared.parquet", *(LANE / "_cache").glob("acs_india_*.parquet")]:
        p.unlink()
    env = {**os.environ, "OPENBLAS_NUM_THREADS": "1", "PYTHONUNBUFFERED": "1"}
    runs = {}
    for s in STEPS:
        r = subprocess.run([sys.executable, str(LANE / s)], cwd=REPO, env=env, capture_output=True, text=True)
        runs[s] = r.returncode
        print(f"  {'✓' if r.returncode == 0 else '✗'} {s} exit {r.returncode}", flush=True)
        if r.returncode != 0:
            print(r.stderr[-3000:])
    after = hashes()
    cmp = {k: ("IDENTICAL" if before.get(k) == after.get(k) else "CHANGED") for k in sorted(set(before) | set(after))}
    gate = json.loads((DER / "gate.json").read_text())
    ok = all(v == 0 for v in runs.values()) and all(v == "IDENTICAL" for v in cmp.values()) \
        and gate["cps"]["status"] == "PASS"
    out = {"exit_codes": runs, "outputs": cmp, "gate_india_g1_edu": gate["cps"], "status": "PASS" if ok else "FAIL"}
    (DER / "verify.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    for k, v in cmp.items():
        print(f"  {v} {k}")
    print(f"VERIFY: {out['status']}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
