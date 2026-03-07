from __future__ import annotations

import csv
import gzip
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "ecls_k"

DCT_PATH = DATA_DIR / "ECLSK_Kto8_child_STATA.dct"
DAT_PATHS = [
    DATA_DIR / "refresh" / "childk8p.dat",
    DATA_DIR / "childk8p.dat",
]
OUT_PATH = DATA_DIR / "eclsk_early_school_extract.tsv.gz"
LINES_PER_RECORD = 15

SELECT_FIELDS = [
    "CHILDID",
    "GENDER",
    "C1WEIGHT",
    "C2WEIGHT",
    "C3WEIGHT",
    "C4WEIGHT",
    "C5WEIGHT",
    "R1_KAGE",
    "R2_KAGE",
    "R3AGE",
    "R4AGE",
    "R5AGE",
    "C1MTHFLG",
    "C2MTHFLG",
    "C3MTHFLG",
    "C4MTHFLG",
    "C5MTHFLG",
    "C1RDGFLG",
    "C2RDGFLG",
    "C3RDGFLG",
    "C4RDGFLG",
    "C5RDGFLG",
    "C1R4MSCL",
    "C2R4MSCL",
    "C3R4MSCL",
    "C4R4MSCL",
    "C5R4MSCL",
    "C1R4RSCL",
    "C2R4RSCL",
    "C3R4RSCL",
    "C4R4RSCL",
    "C5R4RSCL",
]

LINE_NO_RE = re.compile(r"_line\((\d+)\)")
LINE_RE = re.compile(r"_column\((\d+)\)\s+\w+\s+([A-Z0-9_]+)\s+(%\d+(?:\.\d+)?[a-zA-Z])")
WIDTH_RE = re.compile(r"%(\d+)")


def parse_layout() -> dict[str, tuple[int, int, int]]:
    layout: dict[str, tuple[int, int, int]] = {}
    current_line = 1
    with DCT_PATH.open(encoding="latin1", errors="ignore") as fh:
        for line in fh:
            line_match = LINE_NO_RE.search(line)
            if line_match:
                current_line = int(line_match.group(1))
                continue
            match = LINE_RE.search(line)
            if not match:
                continue
            start, name, fmt = match.groups()
            if name not in SELECT_FIELDS:
                continue
            width_match = WIDTH_RE.search(fmt)
            if not width_match:
                continue
            width = int(width_match.group(1))
            layout[name] = (current_line, int(start) - 1, width)
    missing = sorted(set(SELECT_FIELDS) - set(layout))
    if missing:
        raise KeyError(f"missing fields in dct: {missing}")
    return layout


def find_dat_path() -> Path:
    existing = [path for path in DAT_PATHS if path.exists()]
    if not existing:
        raise FileNotFoundError(f"no childk8p.dat found in {DAT_PATHS}")
    return max(existing, key=lambda path: path.stat().st_size)


def main() -> None:
    layout = parse_layout()
    dat_path = find_dat_path()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with dat_path.open("rb") as raw_fh, gzip.open(OUT_PATH, "wt", encoding="utf-8", newline="") as out_fh:
        writer = csv.writer(out_fh, delimiter="\t")
        writer.writerow(SELECT_FIELDS)
        pending: list[str] = []
        for raw_line in raw_fh:
            pending.append(raw_line.decode("latin1", errors="ignore").rstrip("\r\n"))
            if len(pending) < LINES_PER_RECORD:
                continue
            record_lines = pending
            pending = []
            row = []
            for field in SELECT_FIELDS:
                line_no, start, width = layout[field]
                source = record_lines[line_no - 1]
                row.append(source[start : start + width].strip())
            writer.writerow(row)
            count += 1

        if pending:
            raise ValueError(f"incomplete trailing record with {len(pending)} lines")

    print(f"used {dat_path}")
    print(f"wrote {count} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
