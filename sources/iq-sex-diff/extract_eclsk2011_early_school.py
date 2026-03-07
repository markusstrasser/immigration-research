from __future__ import annotations

import csv
import gzip
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "ecls_k2011"

DCT_PATH = DATA_DIR / "ECLSK2011_K5PUF.dct"
ZIP_PATH = DATA_DIR / "ChildK5p.zip"
DAT_PATH = DATA_DIR / "childK5p.dat"
OUT_PATH = DATA_DIR / "eclsk2011_early_school_extract.tsv.gz"
LINES_PER_RECORD = 27

SELECT_FIELDS = [
    "CHILDID",
    "X_CHSEX_R",
    "W1C0",
    "W3CF3P_30",
    "W4CF4P_20",
    "W6CF6P_2A0",
    "W6C6P_20",
    "W7CF7P_70",
    "W8CF8P_80",
    "X1KAGE_R",
    "X2KAGE_R",
    "X3AGE",
    "X4AGE",
    "X5AGE",
    "X6AGE",
    "X7AGE",
    "X8AGE",
    "X1MTHFLG",
    "X2MTHFLG",
    "X3MTHFLG",
    "X4MTHFLG",
    "X5MTHFLG",
    "X6MTHFLG",
    "X7MTHFLG",
    "X8MTHFLG",
    "X1RDGFLG",
    "X2RDGFLG",
    "X3RDGFLG",
    "X4RDGFLG",
    "X5RDGFLG",
    "X6RDGFLG",
    "X7RDGFLG",
    "X8RDGFLG",
    "X1MSCALK5",
    "X2MSCALK5",
    "X3MSCALK5",
    "X4MSCALK5",
    "X5MSCALK5",
    "X6MSCALK5",
    "X7MSCALK5",
    "X8MSCALK5",
    "X1RSCALK5",
    "X2RSCALK5",
    "X3RSCALK5",
    "X4RSCALK5",
    "X5RSCALK5",
    "X6RSCALK5",
    "X7RSCALK5",
    "X8RSCALK5",
]

LINE_RE = re.compile(r"_column\((\d+)\)\s+\w+\s+([A-Z0-9_]+)\s+(%\d+(?:\.\d+)?[a-zA-Z])")
WIDTH_RE = re.compile(r"%(\d+)")


def parse_layout() -> dict[str, tuple[int, int]]:
    layout: dict[str, tuple[int, int]] = {}
    with DCT_PATH.open(encoding="utf-8", errors="ignore") as fh:
        for line in fh:
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
            layout[name] = (int(start) - 1, width)
    missing = sorted(set(SELECT_FIELDS) - set(layout))
    if missing:
        raise KeyError(f"missing fields in dct: {missing}")
    return layout


def main() -> None:
    layout = parse_layout()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    if DAT_PATH.exists():
        raw_context = DAT_PATH.open("rb")
    else:
        archive = zipfile.ZipFile(ZIP_PATH)
        member = next(name for name in archive.namelist() if name.lower().endswith(".dat"))
        raw_context = archive.open(member)

    with raw_context as raw_fh, gzip.open(OUT_PATH, "wt", encoding="utf-8", newline="") as out_fh:
        writer = csv.writer(out_fh, delimiter="\t")
        writer.writerow(SELECT_FIELDS)
        count = 0
        pending: list[str] = []
        for raw_line in raw_fh:
            pending.append(raw_line.decode("latin1", errors="ignore").rstrip("\r\n"))
            if len(pending) < LINES_PER_RECORD:
                continue
            line = "".join(pending)
            pending.clear()
            row = []
            for field in SELECT_FIELDS:
                start, width = layout[field]
                row.append(line[start : start + width].strip())
            writer.writerow(row)
            count += 1

        if pending:
            raise ValueError(f"incomplete trailing record with {len(pending)} lines")

    print(f"wrote {count} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
