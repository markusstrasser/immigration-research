"""Re-anchor file:line citations that no longer verify, by mapping the cited lines from the file as it
stood at a base commit to the file as it stands now (difflib over lines), keeping the citation's shape.

Library for build_inventory.py: reanchor(value, ref, base) -> (new_ref, how) or (None, reason).
"""
import difflib
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

LANE = Path("/Users/alien/Projects/immigration-research/infra/immigration-fiscal/assumption_explorer_2026_09_21")
sys.path.insert(0, str(LANE))
import build_context as bc  # noqa: E402

ROOT = bc.ROOT
REF = re.compile(r"(.+?):(\d+)((?:\s*[-,]\s*\d+)*)$")


@lru_cache(maxsize=None)
def old_lines(base, path):
    out = subprocess.run(["git", "-C", str(ROOT), "show", f"{base}:{path}"], capture_output=True, text=True)
    if out.returncode:
        return None
    return out.stdout.splitlines()


@lru_cache(maxsize=None)
def new_lines(path):
    return (ROOT/path).read_text(errors="replace").splitlines()


@lru_cache(maxsize=None)
def line_map(base, path):
    """1-based old line -> 1-based new line, for lines inside equal blocks."""
    a, b = old_lines(base, path), new_lines(path)
    if a is None:
        return None
    m = {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2-i1):
                m[i1+k+1] = j1+k+1
    return m


def map_line(base, path, line):
    m = line_map(base, path)
    if m is None:
        return None
    if line in m:
        return m[line]
    # A changed line: carry the offset of the nearest mapped line above it.
    above = [k for k in m if k < line]
    return m[max(above)]+(line-max(above)) if above else None


def parse(ref):
    match = REF.match(str(ref))
    if not match:
        return None
    path = match.group(1)
    nums = [int(match.group(2))]+[int(n) for n in re.findall(r"\d+", match.group(3))]
    seps = re.findall(r"\s*([-,])\s*", match.group(3))
    return path, nums, seps


def fmt(path, nums, seps):
    text = str(nums[0])
    for sep, n in zip(seps, nums[1:]):
        text += sep+str(n)
    return f"{path}:{text}"


def reanchor(value, ref, base):
    if bc.confirmed(value, ref):
        return ref, "verifies"
    parsed = parse(ref)
    if not parsed:
        return None, "unparseable ref"
    path, nums, seps = parsed
    mapped = [map_line(base, path, n) for n in nums]
    if all(x is not None for x in mapped):
        candidate = fmt(path, mapped, seps)
        if bc.confirmed(value, candidate):
            return candidate, "mapped"
    # Fall back: shift the whole citation, closest shift first.
    for d in sorted(range(-60, 61), key=abs):
        shifted = [n+d for n in nums]
        if min(shifted) < 1:
            continue
        candidate = fmt(path, shifted, seps)
        if bc.confirmed(value, candidate):
            return candidate, f"shifted {d:+d}"
    return None, "no window verifies"
