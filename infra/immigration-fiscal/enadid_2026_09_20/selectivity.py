"""Schooling of Mexico-born residents who lived in the US five years earlier, vs stayers.

ENADID TSDem, ages 25-54, Mexico-born (this state or another Mexican state).
US group is current Mexican residents, so it is returnees plus anyone else who
was in the US at the endpoint and is now back — not people still in the US.
Stayers are everyone else in the same age and birthplace cut.

LTHS: accumulated approved grades < 9 (below completed secundaria).
BA+: NIV >= 8 (licenciatura, especialidad, maestría, doctorado).
Weights: FAC_VIV. Design-naive (no EST_DIS/UPM variance).
"""
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
OUT = HERE / "derived"
BANDS = [(25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 54)]
SPECS = {
    2018: {
        "zip": CACHE / "enadid_2018_csv.zip",
        "member": "conjunto_de_datos_tsdem_enadid_2018/conjunto_de_datos/"
                  "conjunto_de_datos_tsdem_enadid_2018.csv",
        "cols": ["edad", "p3_7", "p3_19", "esco_acum", "niv", "fac_viv"],
        "born": "p3_7", "us": "p3_19",
    },
    2023: {
        "zip": CACHE / "enadid_2023_csv.zip",
        "member": "conjunto_de_datos_tsdem_enadid_2023/conjunto_de_datos/"
                  "conjunto_datos_tsdem_enadid_2023.csv",
        "cols": ["edad", "p3_10", "p3_24", "esco_acum", "niv", "fac_viv"],
        "born": "p3_10", "us": "p3_24",
    },
}


def wmean(x, w):
    m = x.notna() & w.gt(0)
    return float(np.average(x[m], weights=w[m])) if m.any() else np.nan


def cell(year, group, g):
    return {
        "wave": year, "group": group, "n": int(len(g)), "wpop": float(g.w.sum()),
        "mean_years": wmean(g.yrs, g.w),
        "sh_lths": wmean(g.lths, g.w),
        "sh_ba_plus": wmean(g.ba, g.w),
    }


def load(year):
    s = SPECS[year]
    z = zipfile.ZipFile(s["zip"])
    d = pd.read_csv(z.open(s["member"]), usecols=lambda c: c.lower() in s["cols"], dtype=str)
    d.columns = [c.lower() for c in d.columns]
    d["edad"] = pd.to_numeric(d["edad"], errors="coerce")
    d["yrs"] = pd.to_numeric(d["esco_acum"], errors="coerce")
    d.loc[d.yrs > 24, "yrs"] = np.nan
    d["w"] = pd.to_numeric(d["fac_viv"], errors="coerce")
    niv = pd.to_numeric(d["niv"], errors="coerce")
    d["lths"] = np.where(d.yrs.isna(), np.nan, (d.yrs < 9).astype(float))
    d["ba"] = np.where(niv.isna() | (niv > 11), np.nan, (niv >= 8).astype(float))
    mex = d[s["born"]].isin(["1", "2"])
    age = d.edad.between(25, 54)
    d["in_us"] = d[s["us"]].eq("3")
    return d[mex & age & d.w.gt(0)].copy()


def main():
    rows = []
    for year in SPECS:
        base = load(year)
        for label, mask in [("stayer", ~base.in_us), ("in_us_5y_ago", base.in_us)]:
            g = base[mask]
            rows.append(cell(year, label, g))
            for lo, hi in BANDS:
                rows.append(cell(year, f"{label}_{lo}_{hi}", g[g.edad.between(lo, hi)]))
    out = pd.DataFrame(rows)
    OUT.mkdir(exist_ok=True)
    out.to_csv(OUT / "return_selectivity_by_schooling.csv", index=False)
    show = out[out.group.isin(["stayer", "in_us_5y_ago"])]
    print(show.to_string(index=False, float_format=lambda x: f"{x:.3f}"))


if __name__ == "__main__":
    main()
