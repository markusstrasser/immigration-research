"""Naturalization share by birthplace and years since entry, from the CPS ASEC.

Why a second instrument: PEINUSYR (year of entry) is carried by the ASEC but not by the
November voting or September volunteering supplements, so the years-since-entry cut the
brief asks for has to come from here. Different month, different weight (MARSUPWT), so the
levels are not the supplements' levels; the column to read is the India/China/Mexico
contrast within a years-since-entry band.

Input: ~/research-data/immigration-fiscal/data/external/cps/asec/asec_<year>_{persons,supp}.json
       (pulled 2026-09-16 by ../cps_generation_welfare_2026_09_16/pull_cps_asec.sh)
Run: uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 scripts/asec_entry.py
Output: derived/asec_naturalization_by_entry.csv
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CACHE, CHINA, INDIA, MEXICO, kish_neff, write_csv  # noqa: E402

YEARS = [2024, 2025]
BANDS = [(0, 4), (5, 9), (10, 19), (20, 29), (30, 99)]


def data_dir() -> Path:
    root = os.environ.get("PNY_DATA_ROOT")
    if not root:
        cfg = Path(__file__).resolve().parent.parent.parent / "acquire" / "config.local.env"
        for line in cfg.read_text().splitlines() if cfg.exists() else []:
            if "PNY_DATA_ROOT" in line and "=" in line:
                root = line.split("=", 1)[1].strip().strip('"')
                break
    if not root:
        raise SystemExit("[DEGRADED] PNY_DATA_ROOT unset")
    return Path(root) / "external" / "cps" / "asec"


def load(p: Path) -> pd.DataFrame:
    a = json.loads(p.read_text())
    return pd.DataFrame(a[1:], columns=a[0])


def entry_midpoints(year: int) -> dict[int, float]:
    """PEINUSYR code -> band midpoint, parsed from that ASEC year's own value labels.

    The bands are not a fixed arithmetic series ("Before 1950", "1950-1959", five-year
    bands to 1979, then two-year bands) and the top band moves with the survey year
    (2022-2024 in ASEC 2024, 2022-2025 in ASEC 2025), so the mapping is read from
    _cache/asec_<year>_PEINUSYR.json rather than hard-coded.
    """
    f = CACHE / f"asec_{year}_PEINUSYR.json"
    items = json.loads(f.read_text())["values"]["item"]
    out: dict[int, float] = {}
    for code, label in items.items():
        c = int(code)
        if c == 0 or label.strip().upper() == "NIU":
            continue
        lab = label.strip()
        if lab.lower().startswith("before "):
            hi = float(lab.split()[-1])
            out[c] = hi - 5.0                 # open band; midpoint is a convention
        elif "-" in lab:
            lo, hi = (float(x) for x in lab.split("-"))
            out[c] = (lo + hi) / 2.0
        else:
            out[c] = float(lab)
    return out


def main() -> None:
    d = data_dir()
    rows = []
    for year in YEARS:
        fp, fs = d / f"asec_{year}_persons.json", d / f"asec_{year}_supp.json"
        if not (fp.exists() and fs.exists()):
            print(f"[skip] ASEC {year} absent under {d}")
            continue
        p = load(fp)
        s = load(fs)[["H_SEQ", "PPPOS", "PEINUSYR"]]
        p = p.merge(s, on=["H_SEQ", "PPPOS"], validate="one_to_one")
        for c in ["PENATVTY", "PRCITSHP", "A_AGE", "PEINUSYR"]:
            p[c] = pd.to_numeric(p[c], errors="coerce")
        p["MARSUPWT"] = pd.to_numeric(p["MARSUPWT"], errors="coerce")
        p = p[(p.MARSUPWT > 0) & (p.A_AGE >= 18) & p.PRCITSHP.isin([4, 5])].copy()
        p["entry_year"] = p.PEINUSYR.map(entry_midpoints(year))
        p = p[p.entry_year.notna()]
        p["ysu"] = year - p.entry_year
        grp = pd.Series("4 Other foreign-born", index=p.index)
        grp[p.PENATVTY.eq(INDIA)] = "1 India-born"
        grp[p.PENATVTY.eq(CHINA)] = "2 China-born"
        grp[p.PENATVTY.eq(MEXICO)] = "3 Mexico-born"
        p["grp"] = grp
        for lo, hi in BANDS:
            sub = p[(p.ysu >= lo) & (p.ysu <= hi)]
            for g, x in sub.groupby("grp", sort=True):
                w = x.MARSUPWT.to_numpy(float)
                y = x.PRCITSHP.eq(4).to_numpy(float)
                if len(x) < 50 or w.sum() <= 0:
                    rate = se = float("nan")
                else:
                    rate = float((w * y).sum() / w.sum())
                    neff = kish_neff(w)
                    se = float(np.sqrt(rate * (1 - rate) / neff)) if neff > 0 else float("nan")
                rows.append(dict(asec_year=year, years_since_entry=f"{lo}_{hi}", group=g,
                                 n=int(len(x)), wpop=float(w.sum()),
                                 naturalized_rate=rate, se=se))
        print(f"[load] ASEC {year}: {len(p):,} foreign-born adults with a usable entry year")
    if not rows:
        raise SystemExit("[DEGRADED] no ASEC data")
    t = pd.DataFrame(rows).sort_values(["asec_year", "years_since_entry", "group"],
                                       kind="stable").reset_index(drop=True)
    write_csv(t, "asec_naturalization_by_entry.csv")
    print("[done] asec_naturalization_by_entry.csv")


if __name__ == "__main__":
    main()
