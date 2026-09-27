"""Re-run a lane's scripts and check that its tracked outputs reproduce byte for byte.

    uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/<lane> \
        "uv run --no-project python3 {lane}/build.py" \
        "uv run --no-project --with matplotlib python3 {lane}/figure.py" \
        "uv run --no-project python3 {lane}/verify.py"

Each command runs from the repository root with OPENBLAS_NUM_THREADS=1; `{lane}` expands to the lane
path. Every file a commit of the lane would carry (tracked, or untracked and not ignored) and every
file under its `derived/` is copied aside first. Outputs outside `derived/`, such as a nested
`credentials/derived/` or a `design_table/*.csv`, count too: the 2026-09-28 school lane wrote to
four places and the old `derived/`-only check would have missed three. The run stops at the first
nonzero exit code and reports FAILED without comparing anything: a failed script leaves the old
outputs in place, and they would compare identical (the 2026-09-23 zsh `$w` trap and the 2026-09-27
missing-pyreadr trap). After a clean run, the same set is compared with its copy; new, missing and
changed files are listed. Exit 0 only when every command succeeded and every output is identical.

New or modified scripts in the lane that no command names are listed as NOT RUN, and the exit code is
3. Such a script is either still being written by a worker, or missing from the reproduce list; either
way the rerun does not cover it (3589a4f took a half-written script from a running worker). Check
`ListAgents` and the RESULT, then add a command or pass `--allow-unrun <path>` (repeatable).
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
SCRIPT_SUFFIXES = {".py", ".cjs", ".mjs", ".js", ".R", ".sh"}


def unrun_scripts(lane: Path, cmds: list[str], allowed: set[str]) -> list[str]:
    """New or modified scripts under the lane that no command names."""
    r = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", str(lane)],
                       cwd=ROOT, capture_output=True, text=True, check=True)
    out = []
    for line in r.stdout.splitlines():
        path = line[3:].split(" -> ")[-1].strip().strip('"')
        p = Path(path)
        if p.suffix not in SCRIPT_SUFFIXES or {"_cache", "__pycache__", "node_modules"} & set(p.parts):
            continue
        if path in allowed or p.name in allowed or any(p.name in c for c in cmds):
            continue
        out.append(path)
    return out


def output_files(lane: Path) -> set[Path]:
    """Lane files a commit would carry, plus everything under derived/ (ignored files included)."""
    r = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", str(lane)],
                       cwd=ROOT, capture_output=True, text=True, check=True)
    files = {Path(p) for p in r.stdout.split("\0") if p}
    derived = ROOT / lane / "derived"
    if derived.is_dir():
        files |= {p.relative_to(ROOT) for p in derived.rglob("*")}
    return {p for p in files if (ROOT / p).is_file() and "__pycache__" not in p.parts}


def main(argv: list[str]) -> int:
    allowed: set[str] = set()
    while "--allow-unrun" in argv:
        i = argv.index("--allow-unrun")
        allowed.add(argv[i + 1])
        del argv[i:i + 2]
    if len(argv) < 2:
        print(__doc__)
        return 2
    lane = Path(argv[0])
    if not (ROOT / lane).is_dir():
        print(f"[rerun] no lane directory {lane}")
        return 2
    before = output_files(lane)
    backup = Path(tempfile.mkdtemp(prefix="rerun_")) / "lane"
    for p in before:
        (backup / p).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / p, backup / p)
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
    old, new = before, output_files(lane)
    changed = sorted(str(p) for p in old & new if not filecmp.cmp(backup / p, ROOT / p, shallow=False))
    added, missing = sorted(map(str, new - old)), sorted(map(str, old - new))
    for label, items in (("CHANGED", changed), ("NEW", added), ("MISSING", missing)):
        for it in items:
            print(f"[rerun] {label} {it}")
    ok = not (changed or added or missing)
    print(f"[rerun] {'IDENTICAL' if ok else 'DIFFERS'}: {len(old & new) - len(changed)}/{len(old)} files unchanged"
          f" (backup: {backup})")
    unrun = unrun_scripts(lane, [c.replace("{lane}", str(lane)) for c in argv[1:]], allowed)
    for path in unrun:
        print(f"[rerun] NOT RUN {path}")
    if unrun:
        print("[rerun] UNCOVERED: new or modified scripts that no command runs. A worker may still be writing,"
              " or the reproduce list misses them; check ListAgents and the RESULT, then add a command or pass"
              " --allow-unrun <path>.")
        return 3 if ok else 1
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
