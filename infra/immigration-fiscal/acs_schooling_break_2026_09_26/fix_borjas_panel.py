"""Size the 2020 ACS no-schooling step in build/build_borjas_supply_shock_panel.py's headline, the
immigrant share of people aged 18-64 below high school (EDUC 1-5, 'HSD'), 1980 -> 2023.

Until 2026-09-26 the builder kept EDUC 1-11 only, so no-schooling reports (EDUC 0) left the panel. In
the 2023 ACS the step sends part of the HSD population to EDUC 0, where it was dropped. Break correction:
the excess share phi of 2023 EDUC 0 records returns to HSD (its sources are all below grade 12).
  A  phi = 1 - share_2019 / share_2023 of no-schooling reports, 18-64, by nativity (Census PUMS,
     break_anatomy.py inputs)
  B  flow rates of break_anatomy.py (fixed population: foreign-born, US-born) on each nativity's
     own 2023 EDUCD mix
Also shown: EDUC 0 kept in HSD in every year (an adjacent choice, not a break correction).
A positive control first reproduces the builder's CSV. Since 2026-09-26 the builder keeps EDUC 0 in HSD
(this lane's finding), so the control reproduces the kept rule; rows labelled "as built (EDUC 0
dropped)" record the builder before that date.
Output: derived/borjas_panel_corrected.csv. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/acs_schooling_break_2026_09_26/fix_borjas_panel.py
"""
import sys
from pathlib import Path

import duckdb
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "infra/immigration-fiscal/build"))
import breakfix as B  # noqa: E402
import paths  # noqa: E402

PANEL_CSV = paths.derived_root() / "tier_a" / "borjas_supply_shock_panel.csv"
PUMS = ROOT / "infra/immigration-fiscal/dataset_integrity_2026_09_23/_cache"


def pums_none_share(year: int) -> dict:
    """No-schooling share, ages 18-64, by nativity, from the pinned PUMS files."""
    import break_anatomy as A
    d = pd.read_parquet(PUMS / f"acs_person_{year}.parquet", columns=["AGEP", "SCHL", "NATIVITY", "PWGTP"])
    B.gate(A.sha256(PUMS / f"acs_person_{year}.parquet") == A.SHA[year], f"[BLOCKED] {year} PUMS hash")
    d = d[d.AGEP.between(18, 64)]
    out = {}
    for nat, key in ((2, "fb"), (1, "native")):
        t = d[d.NATIVITY == nat]
        out[key] = float(t.PWGTP[t.SCHL == 1].sum() / t.PWGTP.sum())
    return out


def main() -> None:
    con = duckdb.connect(str(paths.microdata_duckdb_path()), read_only=True)
    d = con.execute("""SELECT YEAR, EDUC, EDUCD, PERWT, BPL >= 150 AS fb FROM ipums_usa_borjas_panel
                       WHERE AGE BETWEEN 18 AND 64 AND EDUC BETWEEN 0 AND 11""").fetchdf()
    con.close()
    panel = pd.read_csv(PANEL_CSV)
    hsd = panel[panel.education_bucket == "HSD"].groupby("year")[["immigrant_weight", "native_weight"]].sum()
    rows = []
    for y, g in d.groupby("YEAR"):
        h = g[g.EDUC.between(1, 5)]
        fb, nat = float(h.PERWT[h.fb].sum()), float(h.PERWT[~h.fb].sum())
        z = g[g.EDUC == 0]
        z_fb, z_nat = float(z.PERWT[z.fb].sum()), float(z.PERWT[~z.fb].sum())
        B.gate(abs(fb + z_fb - hsd.loc[y, "immigrant_weight"]) < 1
               and abs(nat + z_nat - hsd.loc[y, "native_weight"]) < 1,
               f"[BLOCKED] control {y}: HSD weights differ from the builder's CSV")
        rows.append({"year": int(y), "rule": "as built (EDUC 0 dropped)", "method": "none", "phi_fb": 0.0,
                     "phi_native": 0.0, "hsd_immigrant_share": fb / (fb + nat)})
        rows.append({"year": int(y), "rule": "adjacent: EDUC 0 kept in HSD", "method": "none", "phi_fb": 1.0,
                     "phi_native": 1.0, "hsd_immigrant_share": (fb + z_fb) / (fb + z_fb + nat + z_nat)})
        if y >= 2020:
            s19, sy = pums_none_share(2019), pums_none_share(int(y))
            phi_a = {k: 1 - s19[k] / sy[k] for k in ("fb", "native")}
            phi_b = {}
            for k, grp, m in (("fb", "foreign_born", g.fb), ("native", "usborn", ~g.fb)):
                gg = g[m]
                phi_b[k], _ = B.split_b(B.weights_by_code(gg.EDUCD.to_numpy(), gg.PERWT.to_numpy(float)),
                                        B.flow_rates(grp, "fixed"), "educd")
            for method, phi in (("A", phi_a), ("B", phi_b)):
                f2, n2 = fb + phi["fb"] * z_fb, nat + phi["native"] * z_nat
                rows.append({"year": int(y), "rule": "as built (EDUC 0 dropped)", "method": method,
                             "phi_fb": phi["fb"], "phi_native": phi["native"], "hsd_immigrant_share": f2 / (f2 + n2)})
    print("positive control passed: HSD weights equal the builder's CSV", flush=True)
    R = pd.DataFrame(rows)
    R.to_csv(HERE / "derived" / "borjas_panel_corrected.csv", index=False, float_format="%.5f", lineterminator="\n")
    print(R.to_string(index=False, float_format=lambda v: f"{v:.4f}"))


if __name__ == "__main__":
    main()
