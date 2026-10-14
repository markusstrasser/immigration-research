"""Acquire missing primary sources or verify existing pins; never refresh a digest silently.

Run: uv run --no-project python3 {lane}/acquire.py [--download]
"""
import argparse
import hashlib
import json
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--download", action="store_true")
    args = ap.parse_args()
    pins = json.loads((HERE / "inputs/pins.json").read_text())["files"]
    for row in pins:
        p = (HERE if row["root"] == "lane" else ROOT) / row["path"]
        if not p.exists() and args.download and row.get("url"):
            p.parent.mkdir(parents=True, exist_ok=True)
            req = urllib.request.Request(row["url"], headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
            if hashlib.sha256(data).hexdigest() != row["sha256"]:
                raise SystemExit(f"[BLOCKED] downloaded bytes drifted: {row['path']}")
            p.write_bytes(data)
        if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != row["sha256"]:
            raise SystemExit(f"[BLOCKED] missing/stale source: {row['path']}; use --download for missing external files")
    print(f"PASS: {len(pins)} source pins")


if __name__ == "__main__":
    main()
