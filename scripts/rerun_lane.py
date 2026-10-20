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
An identical run deletes its copy; a failed or differing run keeps it and prints its path, to restore
from. Until 2026-10-15 every copy stayed: 233 of them held 1.5 GB of the temp folder.
The copy carries bytes only, with fresh file times. On 2026-10-15 a metadata-preserving copy kept the
lane files' old access times, and macOS's dirhelper (03:35 daily, files unread for 3 days under
/var/folders) deleted 39 of 197 copies mid-run; a copy missing at comparison time now stops with
BACKUP DAMAGED and exit 5 instead of a traceback.

New or modified scripts in the lane that no command names are listed as NOT RUN, and the exit code is
3; a shell script a command runs (a run_all.sh) counts its text as named. Such a script is either still being written by a worker, or missing from the reproduce list; either
way the rerun does not cover it (3589a4f took a half-written script from a running worker). Check
`ListAgents` and the RESULT, then add a command or pass `--allow-unrun <path>` (repeatable).
A module that a named script reaches through a static `require("./x.cjs")`, `import ... from "./x.mjs"` or
Python `import x` (resolved beside the importing file) counts as run too: the round-2 review of 2026-10-14 found
lanes exempting `v7_split.cjs` and `age_routing.cjs` with `--allow-unrun` because the check did not follow
`require()`, so an exemption kept passing after a caller stopped loading the module. A wrapper's
`"$LANE/x.cjs"` token resolves beside the wrapper, and a script a Python file builds a path to and runs
(`HERE / "x.cjs"`, or a call argument) counts as reached: on 2026-10-15 the generation lane flagged three
modules its run_all.sh ran that way. Other dynamic paths (`require(path.join(...))`, `sys.path` edits) are
not followed; those still need a command or an exemption.

Commands run with UV_OFFLINE=1, so `uv run --with <pkg>` takes packages from uv's cache instead of
asking PyPI on every call. On 2026-09-29 a PyPI connect timeout failed two white_replacement reruns
at `uv run --with statsmodels`: a transport failure, not a lane failure. A package missing from the
cache fails loudly with a hint; pass `--online` to resolve against the index. A UV_OFFLINE the caller
sets wins.

A lane file a commit would carry whose bytes git would convert on the way in (CRLF, under
core.autocrlf=input) is listed as EOL and the exit code is 4: this checkout and a fresh clone would
hold different bytes, so pins fail and reruns differ in the clone. On 2026-10-14 the coverage lane
pinned three Census pages with CRLF, git stored them as LF, and 94 tracked files were in the same
state. Write LF (`csv.writer(f, lineterminator="\\n")`), or list a pinned raw download as `-text` in
.gitattributes.

Before copying or executing anything, scan all tracked and untracked non-ignored lane files
except Markdown for session-temporary paths. Such code/data is not portable to a fresh clone;
report every file:line and exit 6. Captured narrative receipts belong in Markdown, never in an
executable fallback. Scan raw bytes so non-UTF8 data cannot hide a path; ignored local caches
are outside this source scan.

After the run, a file a commit would carry above 95 MiB is listed as TOO LARGE and the exit code is 7:
GitHub rejects a push holding a file over 100 MiB, and the repo has no LFS. Above 50 MiB it is listed as LARGE (a
warning; GitHub warns there too). On 2026-10-20 the v9 propagation wrote a 143.8 MB back-cast table and a 259.5 MB
world-ledger cells file, both found only by a reviewer. Aggregate the table, write `.csv.gz`, or keep the full bytes
in the ignored `_cache/` with a tracked sha256.
"""
from __future__ import annotations

import ast
import filecmp
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_SUFFIXES = {".py", ".cjs", ".mjs", ".js", ".R", ".sh"}


def wrapper_paths(cmds: list[str]) -> list[Path]:
    """Each shell script a command runs."""
    return [ROOT / tok for c in cmds for tok in c.split() if tok.endswith(".sh") and (ROOT / tok).is_file()]


def wrapper_texts(cmds: list[str]) -> list[str]:
    """The text of each shell script a command runs. A wrapper such as run_all.sh names the lane's scripts itself:
    on 2026-09-29 `sh {lane}/run_all.sh` ran all of the world ledger's scripts and eight of them showed as NOT RUN."""
    return [p.read_text() for p in wrapper_paths(cmds)]


def wrapper_scripts(wrapper: Path) -> set[Path]:
    """Scripts beside a wrapper that it names through a variable, as `node "$LANE/run_generations_v8.cjs"`: the
    token does not resolve from the repository root, so on 2026-10-15 the modules that script requires showed as
    NOT RUN although run_all.sh ran it."""
    names = {Path(tok.strip("'\";()")).name for tok in wrapper.read_text().split()}
    return {(wrapper.parent / n).resolve() for n in names
            if Path(n).suffix in SCRIPT_SUFFIXES and (wrapper.parent / n).is_file()}


def py_named_scripts(path: Path, tree: ast.AST) -> set[Path]:
    """Scripts beside a Python file that it builds a path to and runs, as `subprocess.run(["node", str(HERE /
    "routing_variants.cjs")])`: a string literal on the right of `/`, or a call argument (bare or inside a list)."""
    lits: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div) and isinstance(node.right, ast.Constant):
            lits.append(node.right.value)
        elif isinstance(node, ast.Call):
            for arg in node.args:
                elts = arg.elts if isinstance(arg, (ast.List, ast.Tuple)) else [arg]
                lits += [e.value for e in elts if isinstance(e, ast.Constant)]
    return {(path.parent / Path(s).name).resolve() for s in lits if isinstance(s, str)
            and Path(s).suffix in SCRIPT_SUFFIXES and (path.parent / Path(s).name).is_file()}


JS_SPEC = re.compile(r"""(?:\brequire\(\s*|\bimport\s*\(\s*|\bfrom\s+|^\s*import\s+)(['"])([^'"]+)\1""", re.M)
JS_SUFFIXES = ("", ".cjs", ".js", ".mjs", ".json")


def js_deps(path: Path) -> set[Path]:
    """Files a JavaScript module loads through a literal relative specifier (packages are skipped)."""
    deps = set()
    for _, spec in JS_SPEC.findall(path.read_text(errors="replace")):
        if not spec.startswith("."):
            continue
        base = path.parent / spec
        for cand in [base.with_name(base.name + s) for s in JS_SUFFIXES] + [base / "index.js"]:
            if cand.is_file():
                deps.add(cand.resolve())
                break
    return deps


def py_deps(path: Path) -> set[Path]:
    """Modules a Python script imports that sit beside it (sys.path[0] for a script) or in a relative package."""
    try:
        tree = ast.parse(path.read_text(errors="replace"))
    except SyntaxError:
        return set()
    names: list[tuple[str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [(a.name, 0) for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            names += [(mod, node.level)] + [(f"{mod}.{a.name}" if mod else a.name, node.level) for a in node.names]
    deps = py_named_scripts(path, tree)
    for name, level in names:
        if not name:
            continue
        base = path.parent if level <= 1 else path.parents[level - 1]
        cand = base.joinpath(*name.split("."))
        for c in (cand.with_suffix(".py"), cand / "__init__.py"):
            if c.is_file():
                deps.add(c.resolve())
    return deps


def reached_files(cmds: list[str]) -> set[Path]:
    """Every file the commands name (directly or through a shell script they run), closed over static loads."""
    todo = [(ROOT / tok.strip("'\";()")).resolve() for text in cmds + wrapper_texts(cmds) for tok in text.split()]
    todo = [p for p in todo if p.suffix in SCRIPT_SUFFIXES and p.is_file()]
    todo += [p for w in wrapper_paths(cmds) for p in wrapper_scripts(w)]
    seen: set[Path] = set()
    while todo:
        p = todo.pop()
        if p in seen:
            continue
        seen.add(p)
        if p.suffix in {".cjs", ".mjs", ".js"}:
            todo += js_deps(p)
        elif p.suffix == ".py":
            todo += py_deps(p)
    return seen


def unrun_scripts(lane: Path, cmds: list[str], allowed: set[str]) -> list[str]:
    """New or modified scripts under the lane that no command, shell script a command runs, or module those load
    names."""
    r = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", str(lane)],
                       cwd=ROOT, capture_output=True, text=True, check=True)
    reached = reached_files(cmds)
    cmds = cmds + wrapper_texts(cmds)
    out = []
    for line in r.stdout.splitlines():
        path = line[3:].split(" -> ")[-1].strip().strip('"')
        p = Path(path)
        if p.suffix not in SCRIPT_SUFFIXES or {"_cache", "__pycache__", "node_modules"} & set(p.parts):
            continue
        if path in allowed or p.name in allowed or any(p.name in c for c in cmds) or (ROOT / p).resolve() in reached:
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


def session_path_references(lane: Path) -> list[str]:
    """Locate nonportable session paths in the sources a commit would carry."""
    result = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", str(lane)],
                            cwd=ROOT, capture_output=True, text=True, check=True)
    needles = (b"/private/" + b"tmp/", b"/tmp/" + b"claude", b"scratch" + b"pad/")
    hits = []
    for name in sorted(set(result.stdout.split("\0")) - {""}):
        path = ROOT / name
        if not path.is_file() or path.suffix.lower() == ".md":
            continue
        with path.open("rb") as stream:
            for number, line in enumerate(stream, 1):
                if any(needle in line for needle in needles):
                    context = line.decode("utf-8", errors="replace").strip()[:240]
                    hits.append(f"{name}:{number}:{context}")
    return hits


TOO_LARGE, LARGE = 95 * 2**20, 50 * 2**20


def oversized(lane: Path) -> list[tuple[str, int]]:
    """Lane files a commit would carry above the LARGE warning size, largest first."""
    r = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", str(lane)],
                       cwd=ROOT, capture_output=True, text=True, check=True)
    sizes = [(p, (ROOT / p).stat().st_size) for p in r.stdout.split("\0") if p and (ROOT / p).is_file()]
    return sorted(((p, s) for p, s in sizes if s > LARGE), key=lambda x: -x[1])


def converted_on_commit(lane: Path) -> list[str]:
    """Lane files a commit would carry whose stored bytes would differ from the bytes on disk."""
    r = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", str(lane)],
                       cwd=ROOT, capture_output=True, text=True, check=True)
    paths = sorted(p for p in r.stdout.split("\0") if p and (ROOT / p).is_file() and not (ROOT / p).is_symlink())
    if not paths:
        return []
    stdin = "\n".join(paths) + "\n"
    stored, raw = (subprocess.run(["git", "hash-object", *flags, "--stdin-paths"], cwd=ROOT, input=stdin,
                                  capture_output=True, text=True, check=True).stdout.split()
                   for flags in ([], ["--no-filters"]))
    return [p for p, s, w in zip(paths, stored, raw) if s != w]


def child_env(online: bool) -> dict[str, str]:
    """The commands' environment: single-threaded BLAS, no bytecode, and uv offline unless asked."""
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
    if online:
        env.pop("UV_OFFLINE", None)
    else:
        env.setdefault("UV_OFFLINE", "1")
    return env


def main(argv: list[str]) -> int:
    allowed: set[str] = set()
    while "--allow-unrun" in argv:
        i = argv.index("--allow-unrun")
        allowed.add(argv[i + 1])
        del argv[i:i + 2]
    online = "--online" in argv
    argv = [a for a in argv if a != "--online"]
    if len(argv) < 2:
        print(__doc__)
        return 2
    lane = Path(argv[0])
    if not (ROOT / lane).is_dir():
        print(f"[rerun] no lane directory {lane}")
        return 2
    references = session_path_references(lane)
    if references:
        for reference in references:
            print(f"[rerun] SESSION PATH {reference}")
        print("[rerun] BLOCKED: session-only paths in lane source/data; no commands executed")
        return 6
    before = output_files(lane)
    backup = Path(tempfile.mkdtemp(prefix="rerun_")) / "lane"
    for p in before:
        (backup / p).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / p, backup / p)  # bytes only: fresh times keep the temp cleaner off the copy
    env = child_env(online)
    print(f"[rerun] uv {'online' if env.get('UV_OFFLINE') in (None, '0', 'false') else 'offline'}"
          f" (UV_OFFLINE={env.get('UV_OFFLINE', 'unset')})")
    for i, cmd in enumerate(argv[1:], 1):
        cmd = cmd.replace("{lane}", str(lane))
        r = subprocess.run(cmd, shell=True, cwd=ROOT, env=env, capture_output=True, text=True)
        print(f"[rerun] {i}/{len(argv) - 1} rc={r.returncode}  {cmd}")
        if r.returncode != 0:
            tail = (r.stderr or r.stdout).strip().splitlines()[-6:]
            print("\n".join("    " + t for t in tail))
            text = (r.stderr + r.stdout).lower()
            if not online and ("offline" in text or "network connectivity is disabled" in text):
                print("[rerun] hint: reruns run uv offline; a package missing from uv's cache needs --online")
            print(f"[rerun] FAILED at command {i}; outputs not compared (backup: {backup})")
            return 1
    old, new = before, output_files(lane)
    vanished = sorted(str(p) for p in old if not (backup / p).is_file())
    if vanished:
        for it in vanished:
            print(f"[rerun] VANISHED FROM BACKUP {it}")
        print(f"[rerun] BACKUP DAMAGED: {len(vanished)}/{len(old)} copies disappeared from {backup} during the run;"
              " no verdict. Something deleted them (macOS dirhelper clears /var/folders files unread for 3 days at"
              " 03:35); the lane's own files are untouched. Rerun.")
        return 5
    changed = sorted(str(p) for p in old & new if not filecmp.cmp(backup / p, ROOT / p, shallow=False))
    added, missing = sorted(map(str, new - old)), sorted(map(str, old - new))
    for label, items in (("CHANGED", changed), ("NEW", added), ("MISSING", missing)):
        for it in items:
            print(f"[rerun] {label} {it}")
    ok = not (changed or added or missing)
    if ok:
        shutil.rmtree(backup.parent)
    print(f"[rerun] {'IDENTICAL' if ok else 'DIFFERS'}: {len(old & new) - len(changed)}/{len(old)} files unchanged"
          f" ({'backup removed' if ok else f'backup: {backup}'})")
    converted = converted_on_commit(lane)
    for path in converted:
        print(f"[rerun] EOL {path}")
    if converted:
        print("[rerun] CLONE DIFFERS: git would store these files with other bytes than this run left on disk"
              " (CRLF converted to LF), so a fresh clone fails pins and reruns. Write LF"
              " (csv.writer(f, lineterminator=\"\\n\")), or list a pinned raw download as -text in .gitattributes.")
    unrun = unrun_scripts(lane, [c.replace("{lane}", str(lane)) for c in argv[1:]], allowed)
    for path in unrun:
        print(f"[rerun] NOT RUN {path}")
    if unrun:
        print("[rerun] UNCOVERED: new or modified scripts that no command runs. A worker may still be writing,"
              " or the reproduce list misses them; check ListAgents and the RESULT, then add a command or pass"
              " --allow-unrun <path>.")
    big = oversized(lane)
    for path, size in big:
        print(f"[rerun] {'TOO LARGE' if size > TOO_LARGE else 'LARGE'} {path} {size / 2**20:.1f} MiB")
    too_large = any(size > TOO_LARGE for _, size in big)
    if too_large:
        print("[rerun] PUSH WOULD FAIL: GitHub rejects files over 100 MiB and the repo has no LFS. Aggregate, write"
              " .csv.gz, or keep the bytes in the ignored _cache/ with a tracked sha256.")
    if not ok:
        return 1
    return 7 if too_large else 4 if converted else 3 if unrun else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
