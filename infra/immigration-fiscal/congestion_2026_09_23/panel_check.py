"""Volume-delay elasticity of the whole network, from the Urban Mobility Report's own 2018-2024 series.

With per-vehicle delay proportional to (V/C)^beta, total delay D = V * delay per vehicle moves with
elasticity 1 + beta in traffic V at a fixed network. The UMR workbook carries daily VMT (freeway +
arterial) only for the 101 largest areas; its "101 Area Sum" rows give national VMT and delay.
  Year pairs: 2019-2020 (traffic collapse) and 2020-2021 (rebound) overstate beta for a uniform
  removal, because peak traffic, where delay sits, fell and returned more than daily traffic did;
  2021-2024 changes are small and mix in work-from-home shifts in timing and new lanes.
  Cross-area regressions are not identified: in 2020 each area's freeway and arterial VMT change
  by one common factor (correlation 0.99999), i.e. the area VMT changes are imputed, not measured.

Output: derived/umr_panel_elasticity.csv
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/congestion_2026_09_23/panel_check.py
"""
from __future__ import annotations

import pathlib

import numpy as np
import openpyxl
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
YEARS = range(2018, 2025)


def load():
    wb = openpyxl.load_workbook(CACHE / "complete-data-2025-umr-by-tti.xlsx", read_only=True, data_only=True)
    # summaries sheet: 7 freeway DVMT, 8 arterial DVMT, 20 total delay, 34 truck delay (thousands)
    nat = [(int(r[3]), r[7], r[8], r[20], r[34]) for r in wb["summaries"].iter_rows(values_only=True)
           if r[1] == "101 Area Sum" and str(r[3]).isdigit() and int(r[3]) in YEARS]
    nat = pd.DataFrame(nat, columns=["year", "fwy", "art", "delay", "truck_delay"]).set_index("year")
    # urban areas sheet: 1 name, 4 year, 8 freeway DVMT, 9 arterial DVMT
    areas = [(r[1], int(r[4]), r[8], r[9]) for r in wb["urban areas"].iter_rows(values_only=True)
             if r[4] is not None and str(r[4]).isdigit() and int(r[4]) in (2019, 2020) and r[8] is not None]
    areas = pd.DataFrame(areas, columns=["name", "year", "fwy", "art"]).drop_duplicates(["name", "year"])
    return nat.astype(float), areas


def main():
    nat, areas = load()
    nat["vmt"] = nat.fwy + nat.art
    nat["pdelay"] = nat.delay - nat.truck_delay
    rows = []
    pairs = [(y, y + 1) for y in range(2018, 2024)] + [(2019, 2024), (2019, 2021)]
    for y0, y1 in pairs:
        dv = np.log(nat.vmt[y1] / nat.vmt[y0])
        for dep in ("pdelay", "delay"):
            dd = np.log(nat[dep][y1] / nat[dep][y0])
            rows.append({"series": "101 Area Sum", "years": f"{y0}-{y1}", "dependent": dep, "dlog_vmt": dv,
                         "dlog_delay": dd, "elasticity_delay_on_vmt": dd / dv, "implied_beta": dd / dv - 1})
    w = areas.pivot(index="name", columns="year", values=["fwy", "art"])
    rf, ra = np.log(w[("fwy", 2020)] / w[("fwy", 2019)]), np.log(w[("art", 2020)] / w[("art", 2019)])
    rows.append({"series": "101 areas, 2019-2020 area VMT changes", "years": "2019-2020", "dependent": "imputation test",
                 "dlog_vmt": float(rf.mean()), "dlog_delay": np.nan,
                 "elasticity_delay_on_vmt": float(rf.corr(ra)), "implied_beta": np.nan,
                 "note": "correlation of freeway and arterial log VMT changes across areas"})
    out = pd.DataFrame(rows)
    out.to_csv(DERIVED / "umr_panel_elasticity.csv", index=False)
    print(nat.round(0).to_string())
    print(out.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
