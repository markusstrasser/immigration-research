#!/usr/bin/env python3
"""Flag routing-layer sentences that make a result conditional without the range.

The failure this catches: "the sign turns on services" without "and the measured
service response is 0.6-1.0". A routing-layer sentence (INDEX, FAQ, CLAUDE.md)
that makes a result conditional on a parameter must state that parameter's
measured range, or link to the lane that does.

    uv run --no-project python3 scripts/check_conditional_ranges.py
    uv run --no-project python3 scripts/check_conditional_ranges.py research/immigration-INDEX.md
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = [
    ROOT / "research/immigration-INDEX.md",
    ROOT / "research/immigration-objections-faq-2026-09-21.md",
    ROOT / "CLAUDE.md",
]
TRIGGERS = re.compile(r"\b(turns? on|break-even|break even|frozen)\b", re.I)
RANGE = re.compile(
    r"[-−+]?\$?\d+(?:\.\d+)?\s*(?:%|bn|k)?\s*(?:–|-|to)\s*[-−+]?\$?\d+(?:\.\d+)?", re.I
)
TWO_PCT = re.compile(r"\d+(?:\.\d+)?%.{0,80}\d+(?:\.\d+)?%")
LINK = re.compile(r"\]\([^)]*scaling[^)]*\)", re.I)
RANGE_WORDS = re.compile(
    r"measured (?:range|scaling)|near-proportional|scaling test|unmeasured|not measured|does not measure", re.I
)
NUMBER = re.compile(r"\d")
WINDOW = 3  # lines after the trigger to look for the range or link


SERVICE_CONTEXT = re.compile(r"\b(sign|service|response|threshold)\b", re.I)


def check(path: Path) -> list[tuple[int, str]]:
    lines = path.read_text().splitlines()
    hits = []
    in_revisions = False
    for i, line in enumerate(lines):
        if re.match(r"^##\s+Revisions", line):
            in_revisions = True
        if in_revisions:
            continue
        window = " ".join(lines[max(0, i - 4) : i + WINDOW])
        if not TRIGGERS.search(line) or not NUMBER.search(window):
            continue
        # "break-even" and "frozen" only matter when the line is about a service
        # response; a dollar break-even or a frozen range elsewhere is another object.
        low = line.lower()
        if ("break-even" in low or "break even" in low or "frozen" in low) and not SERVICE_CONTEXT.search(line):
            continue
        if line.lstrip().startswith("|"):  # tombstone and data tables are not routing claims
            continue
        if RANGE_WORDS.search(window) or LINK.search(window):
            continue
        hits.append((i + 1, line.strip()))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", type=Path, default=DEFAULT)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    total = 0
    for path in args.files:
        hits = check(path)
        if not hits:
            continue
        total += len(hits)
        rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        print(f"\n{rel}")
        for lineno, text in hits:
            print(f"  {lineno}: {text[:170]}")
    if total:
        print(f"\n{total} conditional-without-range sentence(s). Add the measured range or a link.")
        return 1
    if not args.quiet:
        print("no conditional-without-range sentences found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
