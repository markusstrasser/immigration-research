"""Fetch the eight public files beside_arms.py and beside_extra.py read, into sources/immigration-fiscal/data/external/
stage3/ (ignored), and check each against its pinned sha256; record them in derived/beside_sources.csv. Each staging
directory holds an ACQUIRED.md with the acquisition date and the publisher's vintage.

Sources: BEA Regional Price Parities by state, metropolitan area and state portion (2008-2024, last updated February 19,
2026); World Bank ICP 2021 PPPs by category for Mexico and the United States (API source 90, two requests); INEGI ENIGH
2024 dwellings; CONEVAL's poverty lines for August 2024; the Census Bureau's 2022 census industry code list.

Run from the repository root:  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
    infra/immigration-fiscal/world_ledger_2026_09_27/acquire_beside.py
Existing files are kept when their hash matches; a mismatch stops the run (a publisher's revision needs a new pin).
"""
import csv
import subprocess
import sys

from acquire import UA
from beside_arms import DERIVED, REPO, SOURCES, gate, sha256
from beside_extra import EXTRA_SOURCES


def fetch(path, url):
    path.parent.mkdir(parents=True, exist_ok=True)
    part = path.with_suffix(path.suffix + ".part")
    for _ in range(4):
        rc = subprocess.run(["curl", "-sS", "-f", "-L", "-A", UA, "--retry", "3", "-o", str(part), url]).returncode
        if rc == 0:
            break
    else:
        raise SystemExit(f"[BLOCKED] {url}: curl failed repeatedly (last rc {rc})")
    part.rename(path)


def main():
    rows = []
    for key, (path, sha, url) in {**SOURCES, **EXTRA_SOURCES}.items():
        if not path.is_file():
            fetch(path, url)
        got = sha256(path)
        gate(f"source_{key}_sha256", got == sha, path=str(path), got=got, pinned=sha)
        rows.append([str(path.relative_to(REPO)), url, path.stat().st_size, sha])
    with open(DERIVED / "beside_sources.csv", "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["file", "url", "bytes", "sha256"])
        w.writerows(rows)
    print(f"beside sources: {len(rows)} files, every sha256 as pinned", file=sys.stderr)


if __name__ == "__main__":
    main()
