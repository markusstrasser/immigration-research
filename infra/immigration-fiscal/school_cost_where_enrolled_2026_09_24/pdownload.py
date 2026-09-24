"""Parallel HTTP range download for slow single-connection servers (nces.ed.gov serves ~50 KB/s per
connection). Each part is fetched with curl -r and retried until its byte count is exact; the parts
are joined only when every part is complete, and a zip is tested before it replaces the target.

    uv run --no-project python3 pdownload.py URL OUT [--parts 24]
"""
import argparse
import subprocess
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def content_length(url):
    r = subprocess.run(["curl", "-sS", "-I", "-L", "--max-time", "60", url], capture_output=True, text=True, check=True)
    sizes = [int(line.split(":")[1]) for line in r.stdout.splitlines() if line.lower().startswith("content-length")]
    if not sizes or "accept-ranges: bytes" not in r.stdout.lower():
        raise SystemExit("[BLOCKED] server gives no length or no byte ranges")
    return sizes[-1]


def fetch(url, part, lo, hi, tries=8):
    want = hi - lo + 1
    for attempt in range(tries):
        have = part.stat().st_size if part.exists() else 0
        if have == want:
            return
        if have > want:
            part.unlink()
            have = 0
        subprocess.run(["curl", "-sS", "--max-time", "1800", "-r", f"{lo + have}-{hi}", url, "-o", "-"],
                       stdout=part.open("ab"), stderr=subprocess.DEVNULL)
        print(f"  part {part.name}: {part.stat().st_size}/{want} after try {attempt + 1}", flush=True)
    if part.stat().st_size != want:
        raise SystemExit(f"[BLOCKED] part {part.name} incomplete")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("out", type=Path)
    ap.add_argument("--parts", type=int, default=24)
    a = ap.parse_args()
    size = content_length(a.url)
    step = -(-size // a.parts)
    ranges = [(i * step, min(size, (i + 1) * step) - 1) for i in range(a.parts) if i * step < size]
    parts = [a.out.with_name(f"{a.out.name}.p{i:02d}") for i in range(len(ranges))]
    print(f"[download] {size:,} bytes in {len(ranges)} parts", flush=True)
    with ThreadPoolExecutor(len(ranges)) as pool:
        list(pool.map(lambda x: fetch(a.url, *x), [(p, lo, hi) for p, (lo, hi) in zip(parts, ranges)]))
    tmp = a.out.with_name(a.out.name + ".joined")
    with tmp.open("wb") as f:
        for p in parts:
            f.write(p.read_bytes())
    if tmp.stat().st_size != size:
        raise SystemExit(f"[BLOCKED] joined size {tmp.stat().st_size} != {size}")
    if a.out.suffix == ".zip":
        with zipfile.ZipFile(tmp) as z:
            bad = z.testzip()
            if bad:
                raise SystemExit(f"[BLOCKED] corrupt zip member {bad}")
    tmp.replace(a.out)
    for p in parts:
        p.unlink()
    print(f"[download] complete: {a.out} ({size:,} bytes)", flush=True)


if __name__ == "__main__":
    sys.exit(main())
