"""Fetch the MEPS full-year consolidated files 2016-2022 and the HC-036 pooled
linkage file into `_cache/`, and pin URL, size and SHA-256 for every file.

2023 (HC-251) and 2024 (HC-256) are already held under
`sources/immigration-fiscal/data/external/stage3/ahrq/`; they are hashed in
place, not re-downloaded. Every URL below is the link printed on AHRQ's own
download page for that file (`download_data_files_detail.jsp?cboPufNumber=HC-nnn`,
saved under `_cache/pages/`), not a guessed pattern: HC-192 lives at the
`pufs/` root while later years live in `pufs/hnnn/`, and a second, different
`pufs/h209dat.zip` exists at the root that the HC-209 page does not link.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/fetch_meps.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

LANE = Path(__file__).resolve().parent
CACHE = LANE / "_cache"
PAGES = CACHE / "pages"
DERIVED = LANE / "derived"
LOCAL = Path("/Users/alien/research-data/immigration-fiscal/data/external/stage3/ahrq")
BASE = "https://meps.ahrq.gov/mepsweb/"
UA = {"User-Agent": "Mozilla/5.0 (research reproduction; immigration-research)"}

# HC number by data year, from the brief and AHRQ's full-year consolidated series.
YEARS = {2016: "192", 2017: "201", 2018: "209", 2019: "216", 2020: "224",
         2021: "233", 2022: "243", 2023: "251", 2024: "256"}
HELD = {2023: LOCAL / "meps", 2024: LOCAL / "meps_2024"}
SUFFIXES = ["dat.zip", "su.txt", "cb.pdf", "doc.pdf"]


def _ok(msg):
    print(f"  ✓ {msg}", flush=True)


def _header(s):
    print(f"\n[{s}]", flush=True)


def fail(msg):
    print(f"  ✗ [BLOCKED] {msg}", file=sys.stderr, flush=True)
    raise SystemExit(2)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def page_links(hc: str) -> dict[str, str]:
    """Links on AHRQ's detail page for HC-nnn, keyed by file name."""
    page = PAGES / f"HC-{hc}.html"
    if not page.exists():
        req = urllib.request.Request(
            f"{BASE}data_stats/download_data_files_detail.jsp?cboPufNumber=HC-{hc}", headers=UA)
        page.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    html = page.read_text(encoding="latin-1")
    out = {}
    for href in re.findall(r'href="\.\./([^"]+\.(?:zip|txt|pdf))"', html, flags=re.I):
        out[href.rsplit("/", 1)[1]] = BASE + href
    return out


def download(url: str, dest: Path) -> None:
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=300) as r:
                expected = int(r.headers.get("Content-Length", "0"))
                data = r.read()
            if expected and len(data) != expected:
                raise IOError(f"short read {len(data)} of {expected}")
            tmp = dest.with_suffix(dest.suffix + ".part")
            tmp.write_bytes(data)
            tmp.rename(dest)
            return
        except Exception as exc:  # noqa: BLE001 - retried, then fail loud
            print(f"  ! attempt {attempt} {dest.name}: {exc}", flush=True)
            time.sleep(5 * attempt)
    fail(f"could not download {url}")


def main():
    CACHE.mkdir(exist_ok=True)
    PAGES.mkdir(exist_ok=True)
    DERIVED.mkdir(exist_ok=True)
    manifest = []
    jobs = []
    for year, hc in YEARS.items():
        stem = f"h{hc}"
        for suf in SUFFIXES:
            jobs.append((year, hc, stem + suf))
    # HC-036 pooled linkage file, 1996-2024 release (h36u24)
    for suf in SUFFIXES:
        jobs.append((None, "036", "h36u24" + suf))

    _header("fetch")
    for i, (year, hc, name) in enumerate(jobs, 1):
        if year in HELD:
            path = HELD[year] / name
            if not path.exists():
                fail(f"held file missing: {path}")
            links = page_links(hc)
            manifest.append(dict(year=year, hc=f"HC-{hc}", file=name, path=str(path),
                                 url=links.get(name, ""), held_locally=True,
                                 bytes=path.stat().st_size, sha256=sha256(path)))
            _ok(f"[{i}/{len(jobs)}] {name}: held at {path.parent.name}/, {path.stat().st_size:,} bytes")
            continue
        links = page_links(hc)
        if name not in links:
            fail(f"{name} not linked on the HC-{hc} page; links: {sorted(links)}")
        dest = CACHE / name
        if not dest.exists():
            download(links[name], dest)
        manifest.append(dict(year=year, hc=f"HC-{hc}", file=name, path=str(dest.relative_to(LANE)),
                             url=links[name], held_locally=False,
                             bytes=dest.stat().st_size, sha256=sha256(dest)))
        _ok(f"[{i}/{len(jobs)}] {name}: {dest.stat().st_size:,} bytes from {links[name]}")

    (DERIVED / "inputs_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    _ok(f"inputs_manifest.json: {len(manifest)} files pinned")


if __name__ == "__main__":
    main()
