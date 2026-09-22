#!/usr/bin/env python3
"""Why G2 Indian adults look stronger than the G3+ ID cell — and whether G4 exists.

Pooled CPS ASEC 2022–2026. Splits that can kill stories:
  noise / year flips already in year_cluster.py
  mixed vs Asian-only race
  age 25-39 (Hart-Celler grandchildren) vs 40-64 (can include pioneer G4)
  BA-conditional earnings
  G2 who do vs don't check PRDASIAN=1
  co-resident grandparents (G3 vs G4 among children; adults rarely live with GP)

Run: uv run --no-project --with pandas --with numpy python3 decompose.py
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
INFRA = HERE.parent
OUT = HERE / "derived"
INDIA, US = 210, [57, 60, 66, 69, 73, 78]
ZIPS = {
    2022: INFRA / "latam_comparison_2026_09_17/_cache/2022/asecpub22csv.zip",
    2023: INFRA / "latam_comparison_2026_09_17/_cache/2023/asecpub23csv.zip",
    2024: INFRA / "same_year_tax_2026_09_20/_cache/asecpub24csv.zip",
    2025: INFRA / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip",
    2026: INFRA / "ledger_asec2026_2026_09_16/_cache/asecpub26csv.zip",
}
COLS = [
    "PH_SEQ", "PPPOS", "A_LINENO", "A_AGE", "A_SEX", "A_HGA", "PRPERTYP", "PRCITSHP",
    "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PEHSPNON", "PRDTRACE", "PRDASIAN",
    "MARSUPWT", "PEARNVAL", "FEDTAX_AC", "FICA", "STATETAX_A", "SS_VAL", "SSI_VAL",
    "PAW_VAL", "PEPAR1", "PEPAR2", "PEPAR1TYP", "PEPAR2TYP",
]


def wmean(x, w):
    s = float(np.sum(w))
    return float("nan") if s <= 0 else float(np.dot(x, w) / s)


def load_year(year, path):
    person = f"pppub{year % 100:02d}.csv"
    with zipfile.ZipFile(path) as z:
        header = z.open(person).readline().decode().strip().split(",")
        cols = [c for c in COLS if c in header]
        d = pd.read_csv(z.open(person), usecols=cols, low_memory=False)
    d["year"] = year
    for c in COLS:
        if c not in d.columns:
            d[c] = np.nan
    return d


def gp_india_and_all_us(d):
    """Co-resident biological parents' own parent birthplaces → person's grandparents."""
    n = len(d)
    keys = pd.MultiIndex.from_frame(d[["year", "PH_SEQ", "A_LINENO"]])
    lookup = pd.Series(np.arange(n), index=keys)
    gp = np.full((n, 4), np.nan)
    for slot in (1, 2):
        line = d[f"PEPAR{slot}"].to_numpy()
        query = pd.MultiIndex.from_arrays([d.year.to_numpy(), d.PH_SEQ.to_numpy(), line])
        parent = lookup.reindex(query).fillna(-1).to_numpy(dtype=int)
        bio = (line > 0) & (parent >= 0) & d[f"PEPAR{slot}TYP"].eq(1).to_numpy()
        p = np.maximum(parent, 0)
        for j, field in enumerate(("PEMNTVTY", "PEFNTVTY")):
            keep = bio.copy()
            gp[keep, 2 * (slot - 1) + j] = d[field].to_numpy()[p[keep]]
    any_india = np.nanmax(np.where(np.isnan(gp), -1, gp == INDIA), axis=1) == 1
    known = np.isfinite(gp).any(axis=1)
    all_known = np.isfinite(gp).all(axis=1)
    all_us = all_known & np.isin(gp, US).all(axis=1)
    return any_india, all_us, known, int(np.isfinite(gp).sum(axis=1).max() or 0)


def row(label, use, w, age, ba, earn, net):
    return {
        "cell": label, "n": int(use.sum()), "weighted": float(w[use].sum()),
        "mean_age": wmean(age[use], w[use]),
        "ba": wmean(ba[use], w[use]),
        "earn": wmean(earn[use], w[use]),
        "net": wmean(net[use], w[use]),
    }


def main():
    frames = []
    for year, path in ZIPS.items():
        print(f"[{year}]", flush=True)
        frames.append(load_year(year, path))
    d = pd.concat(frames, ignore_index=True)
    w = d.MARSUPWT.to_numpy(float) / 100.0
    age = d.A_AGE.to_numpy()
    civ = d.PRPERTYP.eq(2).to_numpy() | (age < 15)
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    foreign = d.PRCITSHP.isin([4, 5]).to_numpy()
    parents_us = d.PEFNTVTY.isin(US).to_numpy() & d.PEMNTVTY.isin(US).to_numpy()
    parent_india = (d.PEFNTVTY.eq(INDIA) | d.PEMNTVTY.eq(INDIA)).to_numpy()
    two_india = d.PEFNTVTY.eq(INDIA).to_numpy() & d.PEMNTVTY.eq(INDIA).to_numpy()
    asian_indian = d.PRDASIAN.eq(1).to_numpy()
    # CPS PRDTRACE: 4 = Asian only in recent ASEC; mixed White-Asian is typically 21.
    asian_only = d.PRDTRACE.eq(4).to_numpy()
    white_asian = d.PRDTRACE.eq(21).to_numpy()
    ba = (d.A_HGA >= 43).to_numpy(float)
    earn = d.PEARNVAL.to_numpy(float)
    net = (d.FEDTAX_AC + d.FICA + d.STATETAX_A - d.SS_VAL - d.SSI_VAL - d.PAW_VAL).to_numpy(float)
    adult = civ & (age >= 25) & (age <= 64)

    g1 = foreign & d.PENATVTY.eq(INDIA).to_numpy()
    g2 = native & parent_india
    g3 = native & parents_us & asian_indian
    white = native & parents_us & d.PEHSPNON.eq(2).to_numpy() & d.PRDTRACE.eq(1).to_numpy()

    print("PRDTRACE among G3 adults 25-64 (unweighted):",
          d.loc[adult & g3, "PRDTRACE"].value_counts().to_dict(), flush=True)
    print("PRDTRACE among G2 adults:",
          d.loc[adult & g2, "PRDTRACE"].value_counts().head(8).to_dict(), flush=True)

    cells = {
        "white_25_64": adult & white,
        "g1_25_64": adult & g1,
        "g2_25_64": adult & g2,
        "g2_prdasian": adult & g2 & asian_indian,
        "g2_white_only": adult & g2 & d.PRDTRACE.eq(1).to_numpy(),
        "g2_two_india_parents": adult & g2 & two_india,
        "g2_one_india_parent": adult & g2 & ~two_india,
        "g3_25_64": adult & g3,
        "g3_asian_only": adult & g3 & asian_only,
        "g3_white_asian": adult & g3 & white_asian,
        "g3_other_race": adult & g3 & ~asian_only & ~white_asian,
        "g3_25_39": civ & g3 & (age >= 25) & (age <= 39),
        "g3_40_64": civ & g3 & (age >= 40) & (age <= 64),
        "g2_25_39": civ & g2 & (age >= 25) & (age <= 39),
        "g2_40_64": civ & g2 & (age >= 40) & (age <= 64),
        "g3_ba": adult & g3 & (d.A_HGA >= 43).to_numpy(),
        "g2_ba": adult & g2 & (d.A_HGA >= 43).to_numpy(),
        "white_ba": adult & white & (d.A_HGA >= 43).to_numpy(),
        "g3_noba": adult & g3 & (d.A_HGA < 43).to_numpy(),
        "g2_noba": adult & g2 & (d.A_HGA < 43).to_numpy(),
        "white_noba": adult & white & (d.A_HGA < 43).to_numpy(),
    }
    rows = [row(k, m, w, age, ba, earn, net) for k, m in cells.items()]
    pd.DataFrame(rows).to_csv(OUT / "g2_g3_decompose.csv", index=False, float_format="%.6f")
    for r in rows:
        print(f"  {r['cell']:24} n={r['n']:5d}  age={r['mean_age']:5.1f}  "
              f"BA={r['ba']:5.1%}  earn={r['earn']:8,.0f}  net={r['net']:8,.0f}", flush=True)

    any_india, all_us, known, _ = gp_india_and_all_us(d)
    print("\n== co-resident grandparents, PRDASIAN=1 natives with US-born parents ==", flush=True)
    base = civ & g3
    gp_rows = []
    for label, ages in (("all_ages", np.ones(len(d), bool)),
                        ("under18", age < 18),
                        ("18plus", age >= 18),
                        ("25_64", (age >= 25) & (age <= 64))):
        b = base & ages
        rec = {
            "age": label,
            "n_g3plus_id": int(b.sum()),
            "n_gp_observed": int((b & known).sum()),
            "n_gp_india": int((b & any_india).sum()),
            "n_gp_all_us": int((b & all_us).sum()),
            "w_g3plus": float(w[b].sum()),
            "w_gp_india": float(w[b & any_india].sum()),
            "w_gp_all_us": float(w[b & all_us].sum()),
        }
        gp_rows.append(rec)
        print(f"  {label:8} g3plus n={rec['n_g3plus_id']:4d}  GP observed {rec['n_gp_observed']:4d}  "
              f"India GP {rec['n_gp_india']:4d}  all-US GP {rec['n_gp_all_us']:4d}", flush=True)
    pd.DataFrame(gp_rows).to_csv(OUT / "g4_coresident.csv", index=False, float_format="%.6f")

    # Child G4 vs G3 earnings not defined; parent BA of children 0-17 in G3plus ID.
    child = civ & g3 & (age < 18) & known
    print(f"\nchildren <18 with observed GP: n={int(child.sum())}  "
          f"India-GP share {wmean(any_india[child].astype(float), w[child]):.1%}  "
          f"all-US-GP share {wmean(all_us[child].astype(float), w[child]):.1%}", flush=True)


if __name__ == "__main__":
    main()
