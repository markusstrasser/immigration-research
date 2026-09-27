"""Re-run a lane's scripts and check that its tracked outputs reproduce byte for byte.

    uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/<lane> \
        "uv run --no-project python3 {lane}/build.py" \
        "uv run --no-project --with matplotlib python3 {lane}/figure.py" \
        "uv run --no-project python3 {lane}/verify.py"

Each command runs from the repository root with OPENBLAS_NUM_THREADS=1; `{lane}` expands to the lane
path. The lane's `derived/` is copied aside first. The run stops at the first nonzero exit code and
reports FAILED without comparing anything: a failed script leaves the old outputs in place, and they
would compare identical (the 2026-09-23 zsh `$w` trap and the 2026-09-27 missing-pyreadr trap). After
a clean run, every file in `derived/` is compared with its copy; new, missing and changed files are
listed. Exit 0 only when every command succeeded and every output is identical.
"""
from __future__ import annotations

import filecmp
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    lane = Path(argv[0])
    derived = ROOT / lane / "derived"
    if not derived.is_dir():
        print(f"[rerun] no derived/ in {lane}")
        return 2
    backup = Path(tempfile.mkdtemp(prefix="rerun_")) / "derived"
    shutil.copytree(derived, backup)
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
    for i, cmd in enumerate(argv[1:], 1):
        cmd = cmd.replace("{lane}", str(lane))
        r = subprocess.run(cmd, shell=True, cwd=ROOT, env=env, capture_output=True, text=True)
        print(f"[rerun] {i}/{len(argv) - 1} rc={r.returncode}  {cmd}")
        if r.returncode != 0:
            tail = (r.stderr or r.stdout).strip().splitlines()[-6:]
            print("\n".join("    " + t for t in tail))
            print(f"[rerun] FAILED at command {i}; outputs not compared (backup: {backup})")
            return 1
    old = {p.relative_to(backup) for p in backup.rglob("*") if p.is_file()}
    new = {p.relative_to(derived) for p in derived.rglob("*") if p.is_file()}
    changed = sorted(str(p) for p in old & new if not filecmp.cmp(backup / p, derived / p, shallow=False))
    added, missing = sorted(map(str, new - old)), sorted(map(str, old - new))
    for label, items in (("CHANGED", changed), ("NEW", added), ("MISSING", missing)):
        for it in items:
            print(f"[rerun] {label} {it}")
    ok = not (changed or added or missing)
    print(f"[rerun] {'IDENTICAL' if ok else 'DIFFERS'}: {len(old & new) - len(changed)}/{len(old)} files unchanged"
          f" (backup: {backup})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
