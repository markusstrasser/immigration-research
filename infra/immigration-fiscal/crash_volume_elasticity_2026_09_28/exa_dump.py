"""Split saved Exa result files into one text file per URL under _cache/exa, and grep them.

Usage: exa_dump.py <saved-result-file>... [--grep REGEX]... [--ctx N]
The saved files are either raw Exa JSON or a list of {"type": "text", "text": <json>} blocks.
"""
import json
import re
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent
CACHE = LANE / "_cache" / "exa"


def results(path):
    raw = Path(path).read_text()
    obj = json.loads(raw)
    if isinstance(obj, list):
        obj = json.loads(obj[0]["text"])
    return obj.get("results", [])


def slug(url):
    return re.sub(r"[^A-Za-z0-9]+", "_", url)[:120]


def main(argv):
    files, pats, ctx = [], [], 300
    it = iter(argv)
    for a in it:
        if a == "--grep":
            pats.append(next(it))
        elif a == "--ctx":
            ctx = int(next(it))
        else:
            files.append(a)
    CACHE.mkdir(parents=True, exist_ok=True)
    for f in files:
        for r in results(f):
            text = r.get("text") or ""
            out = CACHE / (slug(r["url"]) + ".txt")
            out.write_text(f"URL: {r['url']}\nTITLE: {r.get('title')}\n\n{text}")
            print(f"== {r['url']} | {r.get('title')!s:.90} | {len(text)} chars -> {out.name}")
            for p in pats:
                for m in list(re.finditer(p, text, flags=re.I))[:4]:
                    s = text[max(0, m.start() - ctx): m.end() + ctx].replace("\n", " ")
                    print(f"   [{p}] ...{s}...")


if __name__ == "__main__":
    main(sys.argv[1:])
