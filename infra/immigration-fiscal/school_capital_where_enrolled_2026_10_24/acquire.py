"""Stage the Census F-33 all-items district files FY1992-FY1999 into _cache/f33_pre2000/.

FY2000-FY2024 are read from school_dilution_2026_09_24/_cache/f33 (that lane's acquire.py). Before FY2000 Census
publishes the all-items file as elsecYY.txt for FY1992-FY1998 and only as elsec99.xls for FY1999, which is
converted here to CSV (LF) with every cell as text. Writes derived/sources_pre2000.json (URL, bytes, SHA-256, rows).
Idempotent: an existing file is hashed, not refetched, unless --refresh.

    uv run --no-project --with xlrd python3 infra/immigration-fiscal/school_capital_where_enrolled_2026_10_24/acquire.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "f33_pre2000"
BASE = "https://www2.census.gov/programs-surveys/school-finances/tables/{y}/secondary-education-finance/{f}"
NEEDED = ["NCESID", "V33", "F12", "G15", "K09", "K10", "K11", "TCAPOUT"]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def curl(url: str, out: Path) -> None:
    tmp = out.with_suffix(out.suffix + ".part")
    r = subprocess.run(["curl", "-sS", "--fail", "-L", "--retry", "3", "--max-time", "900", "-o", str(tmp), url],
                       capture_output=True, text=True)
    if r.returncode:
        tmp.unlink(missing_ok=True)
        raise SystemExit(f"[BLOCKED] curl rc={r.returncode} {url}: {r.stderr.strip()}")
    tmp.replace(out)


def main() -> int:
    CACHE.mkdir(parents=True, exist_ok=True)
    refresh = "--refresh" in sys.argv
    log = []
    for y in range(1992, 2000):
        f = f"elsec{y % 100:02d}.xls" if y == 1999 else f"elsec{y % 100:02d}.txt"
        url, out = BASE.format(y=y, f=f), CACHE / f
        if refresh or not out.exists():
            curl(url, out)
        rec = {"fiscal_year": y, "file": f, "url": url, "bytes": out.stat().st_size, "sha256": sha256(out)}
        if y == 1999:
            import pandas as pd
            d = pd.read_excel(out, dtype=str)
            csv = CACHE / "elsec99_xls.csv"
            d.to_csv(csv, index=False, lineterminator="\n")
            rec.update(converted=csv.name, converted_sha256=sha256(csv), rows=len(d), header=list(d.columns))
        else:
            with open(out, encoding="latin-1") as fh:
                header = fh.readline().strip().replace('"', "").split(",")
                rows = sum(1 for _ in fh)
            rec.update(rows=rows, header=header)
        missing = [c for c in NEEDED if c not in rec["header"]]
        if missing:
            raise SystemExit(f"[BLOCKED] FY{y} {f} lacks {missing}")
        rec["header"] = len(rec["header"])
        log.append(rec)
        print(f"  ✓ FY{y} {f}: {rec['rows']} rows, {rec['bytes']} bytes")
    (HERE / "derived").mkdir(exist_ok=True)
    (HERE / "derived" / "sources_pre2000.json").write_text(json.dumps(log, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
