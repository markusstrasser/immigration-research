"""Selected fields from the held ECLS-K:2011 public K–5 file. Source is read-only."""
import hashlib
import json
import argparse
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "build"))
from paths import reused_surveys_root

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--source-dir",
    type=Path,
    default=reused_surveys_root(require_exists=False) / "ecls_k2011",
)
parser.add_argument(
    "--out",
    type=Path,
    default=Path(__file__).resolve().parent / "_cache" / "ecls_k2011",
)
args = parser.parse_args()
SOURCE, OUT = args.source_dir, args.out
OUT.mkdir(parents=True, exist_ok=True)
dictionary = SOURCE / "ECLSK2011_K5PUF.dct"
data = SOURCE / "childK5p.dat"
if not data.exists():
    alt = SOURCE / "childk5p.dat"
    data = alt if alt.exists() else data

LINES_PER = 27
EXPECTED_ROWS = 18174
requested = """
CHILDID S1_ID T1_ID X_CHSEX_R X_HISP_R X_RACETHP_R X12LANGST X12SESL X1KAGE_R
P2BTHPLC P2CNTRYB
A1FULDAY A1HALFAM A1HALFPM
A1AHISP A1PHISP A1DHISP A1AWHITE A1PWHITE A1DWHITE A1ATOTRA A1PTOTRA A1DTOTRA
A1AELL A1PELL A1DELL A1ANMELL A1PNMELL A1DNMELL
A1ATOTAG A1PTOTAG A1DTOTAG
X1RTHETK5 X2RTHETK5 X1MTHETK5 X2MTHETK5
W1C0 W12AC0
""".split()

layout = {}
line_number = 1
for line in dictionary.read_text(encoding="latin1").splitlines():
    match = re.search(r"_line\((\d+)\)", line)
    if match:
        line_number = int(match.group(1))
    match = re.search(
        r'_column\((\d+)\)\s+(\w+)\s+(\w+)\s+%(\d+)(?:\.\d+)?\w+\s+"(.*)"', line
    )
    if match and match.group(3) in requested:
        start, kind, name, width, label = match.groups()
        layout[name] = {
            "line": line_number,
            "start": int(start) - 1,
            "width": int(width),
            "kind": kind,
            "label": label,
        }
missing = set(requested) - set(layout)
if missing:
    raise ValueError(f"Missing fields {sorted(missing)}")

rows = []
digest = hashlib.sha256()
with data.open("rb") as stream:
    while True:
        lines = [stream.readline() for _ in range(LINES_PER)]
        if not any(lines):
            break
        if not all(lines):
            raise ValueError("Partial trailing record")
        for physical in lines:
            digest.update(physical)
        row = {}
        for name, spec in layout.items():
            physical = lines[spec["line"] - 1].rstrip(b"\r\n")
            start, width = spec["start"], spec["width"]
            if len(physical) < start + width:
                raise ValueError(f"Short physical line {name}")
            row[name] = physical[start : start + width].decode("ascii").strip()
        rows.append(row)

frame = pd.DataFrame(rows)
if frame.CHILDID.duplicated().any():
    raise ValueError("Duplicate CHILDID")
for name, spec in layout.items():
    if not spec["kind"].startswith("str"):
        frame[name] = pd.to_numeric(frame[name], errors="raise")
frame.to_parquet(OUT / "selected.parquet", index=False)

coverage = {}
for name in requested:
    if name == "CHILDID":
        continue
    series = frame[name]
    if layout[name]["kind"].startswith("str"):
        populated = series.astype(str).str.fullmatch(r".+") & ~series.astype(str).isin(["", "-9", "-1"])
        coverage[name] = {
            "label": layout[name]["label"],
            "n_nonempty": int(populated.sum()),
            "n_unique": int(series.nunique()),
        }
    else:
        observed = series.where(series >= 0)
        coverage[name] = {
            "label": layout[name]["label"],
            "n_nonneg": int(observed.notna().sum()),
            "n_unique": int(observed.nunique(dropna=True)),
            "min": None if observed.dropna().empty else float(observed.min()),
            "max": None if observed.dropna().empty else float(observed.max()),
        }

manifest = {
    "data": str(data),
    "data_bytes": data.stat().st_size,
    "data_sha256": digest.hexdigest(),
    "dictionary_sha256": hashlib.sha256(dictionary.read_bytes()).hexdigest(),
    "rows": len(frame),
    "expected_rows": EXPECTED_ROWS,
    "fields": layout,
    "coverage": coverage,
    "selected_sha256": hashlib.sha256((OUT / "selected.parquet").read_bytes()).hexdigest(),
}
(OUT / "probe.json").write_text(json.dumps(manifest, indent=2))
print(json.dumps({"rows": len(frame), "bytes": data.stat().st_size, "sha256": digest.hexdigest()[:16]}, indent=2))
for name in ["P2BTHPLC", "P2CNTRYB", "T1_ID", "S1_ID", "A1ANMELL", "X_HISP_R", "X12LANGST"]:
    print(name, coverage[name])
