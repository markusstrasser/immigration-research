"""Fetch the raw inputs this lane does not already hold locally, into ignored _cache/.

ACS 2020-2024 5-year B03001 (Hispanic origin by specific origin) for every unified, elementary and
secondary school district and every county; the NCES School-Level Finance Survey FY2022 file; the
Census F-33 FY2019 district file for the year-matched English-learner check. Content is validated
(JSON shape, header, row counts, zip members), never status or size alone. The Census key is read
from CENSUS_API_KEY and never printed; errors are redacted.

    set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
    uv run --no-project python3 infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/acquire.py
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
ACS = "https://api.census.gov/data/2024/acs/acs5"
FIELDS = ["NAME", "B03001_001E", "B03001_003E", "B03001_004E", "B03001_003M", "B03001_004M"]
GEOS = {"unified": "school district (unified)", "elementary": "school district (elementary)",
        "secondary": "school district (secondary)", "county": "county"}
FILES = {
    # NCES SLFS FY2022 provisional 1a, data zip linked from the IES resource-library page
    "slfs22_data_2025047_4_0_1.zip": "https://ies.ed.gov/sites/default/files/data-asset/study-program-not-applicable/"
    "2025/08/documentation-nces-common-core-data-school-level-finance-survey-slfs-school-year-2021-22-fiscal-year/"
    "2025047_4_0_1.zip",
    "slfs_fy22_2025047r.zip": "https://ies.ed.gov/sites/default/files/data-asset/ccd-common-core-data/2025/09/"
    "documentation-nces-common-core-data-school-level-finance-survey-slfs-school-year-2021-22-fiscal-year/2025047r.zip",
    "elsec19t.txt": "https://www2.census.gov/programs-surveys/school-finances/tables/2019/secondary-education-finance/elsec19t.txt",
}
STATES = ["01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13", "15", "16", "17", "18", "19", "20", "21",
          "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
          "40", "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]


def redact(text):
    return re.sub(r"key=[^&\s\"']*", "key=REDACTED", str(text))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def curl(url, out):
    tmp = out.with_suffix(out.suffix + ".part")
    r = subprocess.run(["curl", "-sS", "--fail", "-L", "--retry", "3", "--max-time", "900", "-o", str(tmp), url],
                       capture_output=True, text=True)
    if r.returncode:
        tmp.unlink(missing_ok=True)
        raise SystemExit(f"[BLOCKED] curl rc={r.returncode} {redact(url)}: {redact(r.stderr.strip())}")
    tmp.replace(out)


def acs_geo(label, geo, key):
    """One request per state: the API needs `in=state:XX` for these geographies."""
    out = CACHE / f"acs5_2024_B03001_{label}.json"
    if out.exists():
        rows = json.loads(out.read_text())
        print(f"[acs] {label}: cached, {len(rows) - 1} rows")
        return
    header, rows = None, []
    for st in STATES:
        part = CACHE / f"_acs_{label}_{st}.json"
        url = f"{ACS}?get={','.join(FIELDS)}&for={geo.replace(' ', '%20')}:*&in=state:{st}&key={key}"
        r = subprocess.run(["curl", "-sS", "--retry", "3", "--max-time", "120", "-o", str(part), "-w", "%{http_code}", url],
                           capture_output=True, text=True)
        code = r.stdout.strip()
        body = part.read_text() if part.exists() else ""
        part.unlink(missing_ok=True)
        if code == "204" or (code == "200" and not body.strip()):
            continue  # state has no district of this type (e.g. no secondary districts)
        if code != "200":
            raise SystemExit(f"[BLOCKED] ACS {label} state {st}: HTTP {code} {redact(body[:200])}")
        data = json.loads(body)
        if not isinstance(data, list) or len(data) < 2 or data[0][:len(FIELDS)] != FIELDS:
            raise SystemExit(f"[BLOCKED] ACS {label} state {st}: unexpected body {redact(body[:200])}")
        header = header or data[0]
        if data[0] != header:
            raise SystemExit(f"[BLOCKED] ACS {label}: header drift in state {st}")
        rows.extend(data[1:])
    if not rows:
        raise SystemExit(f"[BLOCKED] ACS {label}: no rows")
    out.write_text(json.dumps([header] + rows))
    print(f"[acs] {label}: {len(rows)} rows")


def main():
    CACHE.mkdir(exist_ok=True)
    key = os.environ.get("CENSUS_API_KEY", "")
    if not key:
        raise SystemExit("[BLOCKED] CENSUS_API_KEY not set; source acquire/config.local.env first")
    for label, geo in GEOS.items():
        acs_geo(label, geo, key)
    counts = {label: len(json.loads((CACHE / f"acs5_2024_B03001_{label}.json").read_text())) - 1 for label in GEOS}
    # Content gates: ~10.8k unified, ~1.9k elementary, ~0.4k secondary districts, 3,144 counties (50 states + DC).
    if counts["county"] != 3144 or counts["unified"] < 10000 or counts["elementary"] < 1500 or counts["secondary"] < 300:
        raise SystemExit(f"[BLOCKED] ACS row counts off: {counts}")
    for name, url in FILES.items():
        out = CACHE / name
        if not out.exists():
            curl(url, out)
        if name.endswith(".zip"):
            with zipfile.ZipFile(out) as z:
                bad = z.testzip()
                if bad:
                    raise SystemExit(f"[BLOCKED] corrupt member {bad} in {name}")
        if name == "elsec19t.txt":
            head = out.open().readline()
            if "TCURSPND" not in head or "NCESID" not in head or sum(1 for _ in out.open()) < 13000:
                raise SystemExit("[BLOCKED] elsec19t.txt header or row count unexpected")
    manifest = {name: dict(url=FILES.get(name, "Census API " + ACS), bytes=(CACHE / name).stat().st_size,
                           sha256=sha256(CACHE / name))
                for name in list(FILES) + [f"acs5_2024_B03001_{g}.json" for g in GEOS]}
    manifest["_acs_rows"] = counts
    (HERE / "derived").mkdir(exist_ok=True)
    (HERE / "derived" / "acquired_sources.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print(json.dumps(counts))
    print("acquire: all content gates passed")


if __name__ == "__main__":
    sys.exit(main())
