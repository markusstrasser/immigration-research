"""Extract NYC rows of two NYSED report-card tables from the pinned SRC Access databases.

Reads `_cache/nyc/nysed_src/SRC{2019,2021,2022,2023,2024,2025}.zip` (sha256-pinned), unzips each `.mdb`
member to a temporary directory, exports "Expenditures per Pupil" and "Inexperienced Teachers and Principals" ("Staff Qualifications"
before 2021)
with `mdb-export` (Homebrew mdbtools 1.0.1), keeps New York City rows (ENTITY_CD county codes 30-35), and
writes `_cache/nyc/nysed_src/tables/SRC{Y}_{expenditures,teachers}.csv` plus `tables/MANIFEST.json`.
Each database carries two school years; `build_nyc.py` takes each year from the latest release.

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
        infra/immigration-fiscal/newcomer_school_shock_2026_09_28/extract_nysed_src.py
"""

import csv
import hashlib
import io
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

LANE = Path(__file__).resolve().parent
SRC_DIR = LANE / "_cache" / "nyc" / "nysed_src"
OUT_DIR = SRC_DIR / "tables"

PINS = {
    "SRC2019": "5d6e5c7b33734ad3d8dffdcbe891eadb1f92c274c66a3801d1848659a9b42119",
    "SRC2021": "96e1b83655ea61967055e50c934fb0d1b621b35ac983d1977c9858931786adb9",
    "SRC2022": "0de139eb8f31c3f8ffe159887e1544ea1017cc8267e10c0e54319d4b8a5456cf",
    "SRC2023": "eaa5d2e4d3272c7f891d65f417ec9195b98594eb938241752a26e7c9b3af3315",
    "SRC2024": "b3a53e7f5b3e3ab76136355ae2e64184fd1f8fa87fe5c7bd8d2aec1ca2bc5165",
    "SRC2025": "fe9d2e0e2a365077560d6f7656c4a94e273d154d92bcd02d24f19f587b60e67a",
}
TABLES = {
    "expenditures": re.compile(r"^expenditures? per pupil$", re.I),
    "teachers": re.compile(r"^(inexperienced teachers and principals|staff qualifications)$", re.I),
}
NYC_COUNTY = ("30", "31", "32", "33", "34", "35")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    OUT_DIR.mkdir(exist_ok=True)
    manifest = {"mdb_export": subprocess.run(["mdb-export", "--version"], capture_output=True, text=True).stdout.strip(),
                "inputs": {}, "outputs": {}}
    for name, want in sorted(PINS.items()):
        zpath = SRC_DIR / f"{name}.zip"
        if not zpath.exists():
            raise SystemExit(f"[BLOCKED] missing {zpath}")
        got = sha256(zpath)
        if got != want:
            raise SystemExit(f"[BLOCKED] sha256 mismatch for {zpath.name}: {got} != {want}")
        manifest["inputs"][zpath.name] = got
        with zipfile.ZipFile(zpath) as z:
            members = [m for m in z.namelist() if m.lower().endswith(".mdb")]
            if len(members) != 1:
                raise SystemExit(f"[BLOCKED] {zpath.name}: expected one .mdb member, found {members}")
            with tempfile.TemporaryDirectory(dir=SRC_DIR) as tmp:
                mdb = Path(z.extract(members[0], tmp))
                tables = subprocess.run(["mdb-tables", "-1", str(mdb)], capture_output=True, text=True,
                                        check=True).stdout.splitlines()
                for key, pat in TABLES.items():
                    hits = [t for t in tables if pat.match(t.strip())]
                    if len(hits) != 1:
                        raise SystemExit(f"[BLOCKED] {zpath.name}: table {key} matched {hits} in {tables}")
                    raw = subprocess.run(["mdb-export", str(mdb), hits[0]], capture_output=True, text=True,
                                         check=True).stdout
                    rows = list(csv.reader(io.StringIO(raw)))
                    header, body = rows[0], rows[1:]
                    ent = header.index("ENTITY_CD")
                    keep = sorted((r for r in body if r[ent][:2] in NYC_COUNTY), key=lambda r: (r[ent], r))
                    out = OUT_DIR / f"{name}_{key}.csv"
                    with open(out, "w", newline="") as f:
                        w = csv.writer(f, lineterminator="\n")
                        w.writerow(header)
                        w.writerows(keep)
                    manifest["outputs"][out.name] = {"table": hits[0], "rows_all": len(body),
                                                     "rows_nyc": len(keep), "sha256": sha256(out)}
                    print(f"{name} {key}: {len(body)} rows, {len(keep)} NYC")
                mdb.unlink()
    (OUT_DIR / "MANIFEST.json").write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
