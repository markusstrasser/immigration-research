#!/usr/bin/env python3
"""Re-find every quotation in the lane's reading notes and in RESULT.md in the cached source texts.

Sources: `_cache/papers/*.txt` (pdftotext -layout output or saved page text). A quote is a run of
20 or more characters between straight or curly double quotes. Its candidate files are, in order:
a `.txt` name on the same line; the nearest `<!-- src: ... -->` marker above it; any `.txt` name in
the same section. Matching collapses whitespace and unifies quote marks, dashes and ligatures
(NFKC); a second pass also drops all spaces, because layout text can split table columns
differently. RESULT.md quotes are the rows of its "Quotes used" table: | "quote" | file | where |.

Output: derived/quote_check.csv. Exit code 1 if any RESULT.md quote is not found.

Run from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/compliance_gap_2026_09_24/quote_check.py
"""
from __future__ import annotations

import csv
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPERS = HERE / "_cache" / "papers"
QUOTE = re.compile(r"[\"“]([^\"“”]{20,}?)[\"”]")
TXT = re.compile(r"([A-Za-z0-9_.\-]+\.txt)")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("“", '"'), ("”", '"'), ("’", "'"), ("‘", "'"), ("–", "-"), ("—", "-"), ("−", "-"),
                 ("∗", "*"), ("­", "")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def load_texts() -> dict[str, tuple[str, str]]:
    out = {}
    for p in sorted(PAPERS.glob("*.txt")):
        t = norm(p.read_text(encoding="utf-8", errors="replace"))
        out[p.name] = (t, t.replace(" ", ""))
    return out


def find(quote: str, files: list[str], texts: dict) -> tuple[str, str]:
    q = norm(quote)
    qn = q.replace(" ", "")
    for f in files:
        if f in texts and q in texts[f][0]:
            return "found", f
    for f in files:
        if f in texts and qn in texts[f][1]:
            return "found_ignoring_spaces", f
    for f, (t, tn) in texts.items():
        if q in t or qn in tn:
            return "found_in_other_file", f
    return "missing", ""


def notes_quotes(path: Path) -> list[dict]:
    rows, section_files, src = [], [], []
    lines = path.read_text().splitlines()
    sections: list[list[int]] = []
    for i, line in enumerate(lines):
        if line.startswith("#"):
            sections.append([i])
    bounds = [s[0] for s in sections] + [len(lines)]
    for k in range(len(bounds) - 1):
        block = lines[bounds[k]:bounds[k + 1]]
        section_files = sorted(set(TXT.findall("\n".join(block))))
        src = []
        for j, line in enumerate(block):
            m = re.search(r"<!-- src: (.*?) -->", line)
            if m:
                src = [Path(x).name for x in m.group(1).split() if x.endswith(".txt")]
            for q in QUOTE.findall(line):
                same_line = [f for f in TXT.findall(line) if f not in q]
                rows.append({"file": path.name, "line": bounds[k] + j + 1, "quote": q,
                             "candidates": same_line or src or section_files})
    return rows


def result_quotes(path: Path) -> list[dict]:
    rows, on = [], False
    for i, line in enumerate(path.read_text().splitlines()):
        if line.startswith("## Quotes used"):
            on = True
            continue
        if on and line.startswith("## "):
            break
        if on and line.startswith("|") and not line.startswith("|---") and not line.startswith("| Quote"):
            # a quote may carry a literal pipe written as \| (markdown table escape)
            cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            m = QUOTE.search(cells[0])
            if m and len(cells) >= 2:
                rows.append({"file": path.name, "line": i + 1, "quote": m.group(1), "candidates": [cells[1]]})
    return rows


def main() -> None:
    texts = load_texts()
    rows = []
    for p in sorted((HERE / "reads").glob("*.md")):
        rows += notes_quotes(p)
    res = result_quotes(HERE / "RESULT.md")
    rows += res
    for r in rows:
        r["status"], r["matched_file"] = find(r["quote"], r["candidates"], texts)
    with open(HERE / "derived" / "quote_check.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["file", "line", "status", "matched_file", "candidates", "quote"],
                           lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({**r, "candidates": " ".join(r["candidates"])})
    by = {}
    for r in rows:
        by.setdefault((r["file"], r["status"]), 0)
        by[(r["file"], r["status"])] += 1
    for (f, s), n in sorted(by.items()):
        print(f"  {f:28s} {s:24s} {n}")
    for r in rows:
        if r["status"] == "missing":
            print(f"  ✗ {r['file']}:{r['line']} {r['quote'][:110]!r}")
    bad = [r for r in res if r["status"] == "missing"]
    print(f"{'✓' if not bad else '✗'} RESULT.md quotes found: {len(res) - len(bad)} of {len(res)}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
