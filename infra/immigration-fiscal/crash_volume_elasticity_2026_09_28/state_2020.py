"""US states 2019->2020: deaths (FHWA FI-20) against VMT (FHWA VM-2), by urban share of VMT.

Writes derived/state_2020.csv (one row per state) and prints pooled elasticities by density tercile.
Elasticity = dln(deaths) / dln(VMT). Sources: FHWA Highway Statistics 2019 and 2020, tables VM-2
(VMT by functional system, rural/urban) and FI-20 (persons fatally injured by functional system).
"""
import csv
import math
from io import StringIO
from pathlib import Path

import pandas as pd

LANE = Path(__file__).resolve().parent
CACHE, OUT = LANE / "_cache", LANE / "derived"


def table(name):
    for t in pd.read_html(StringIO((CACHE / name).read_text(errors="ignore"))):
        flat = t.copy()
        flat.columns = [" ".join(str(c) for c in (col if isinstance(col, tuple) else (col,))) for col in t.columns]
        first = flat.iloc[:, 0].astype(str)
        if first.str.contains("Alabama").any():
            return flat
    raise SystemExit(f"[BLOCKED] no state table in {name}")


def by_state(name, pick_urban):
    t = table(name)
    cols = list(t.columns)
    total_col = [c for c in cols if "total" in c.lower()][-1]
    urban_cols = [c for c in cols if "urban" in c.lower() and "total" in c.lower()] if pick_urban else []
    rows = {}
    for _, r in t.iterrows():
        st = str(r.iloc[0]).strip()
        try:
            tot = float(str(r[total_col]).replace(",", ""))
        except ValueError:
            continue
        urb = float(str(r[urban_cols[0]]).replace(",", "")) if urban_cols else None
        rows[st] = (tot, urb)
    return rows, total_col, urban_cols


def main():
    v19, tc, uc = by_state("vm2_2019.html", True)
    v20, _, _ = by_state("vm2_2020.html", True)
    f19, ftc, _ = by_state("fi20_2019.html", False)
    f20, _, _ = by_state("fi20_2020.html", False)
    print("VM-2 total col:", tc, "| urban col:", uc, "| FI-20 total col:", ftc)
    out = []
    for st in v19:
        if st not in v20 or st not in f19 or st not in f20 or "total" in st.lower():
            continue
        dv = math.log(v20[st][0] / v19[st][0])
        dd = math.log(f20[st][0] / f19[st][0])
        out.append({"state": st, "vmt2019_m": v19[st][0], "vmt2020_m": v20[st][0],
                    "urban_share_2019": v19[st][1] / v19[st][0] if v19[st][1] else "",
                    "deaths2019": f19[st][0], "deaths2020": f20[st][0], "dln_vmt": dv, "dln_deaths": dd})
    OUT.mkdir(exist_ok=True)
    with open(OUT / "state_2020.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    out = [r for r in out if r["urban_share_2019"] != ""]
    out.sort(key=lambda r: r["urban_share_2019"])
    n = len(out)
    for name, grp in (("low-urban tercile", out[: n // 3]), ("middle tercile", out[n // 3: 2 * n // 3]),
                      ("high-urban tercile", out[2 * n // 3:])):
        V19, V20 = sum(r["vmt2019_m"] for r in grp), sum(r["vmt2020_m"] for r in grp)
        D19, D20 = sum(r["deaths2019"] for r in grp), sum(r["deaths2020"] for r in grp)
        e = math.log(D20 / D19) / math.log(V20 / V19)
        print(f"{name}: n={len(grp)} urban share {grp[0]['urban_share_2019']:.2f}-{grp[-1]['urban_share_2019']:.2f} "
              f"VMT {V20 / V19 - 1:+.1%} deaths {D20 / D19 - 1:+.1%} elasticity {e:+.2f}")
    top = sorted(out, key=lambda r: -r["urban_share_2019"])[:8]
    for r in top:
        print(f"  {r['state']}: urban {r['urban_share_2019']:.2f} VMT {math.exp(r['dln_vmt']) - 1:+.1%} "
              f"deaths {int(r['deaths2019'])}->{int(r['deaths2020'])} ({math.exp(r['dln_deaths']) - 1:+.1%})")
    V19, V20 = sum(r["vmt2019_m"] for r in out), sum(r["vmt2020_m"] for r in out)
    D19, D20 = sum(r["deaths2019"] for r in out), sum(r["deaths2020"] for r in out)
    print(f"all: VMT {V20 / V19 - 1:+.1%} deaths {D19:.0f}->{D20:.0f} ({D20 / D19 - 1:+.1%}) elasticity "
          f"{math.log(D20 / D19) / math.log(V20 / V19):+.2f}")


if __name__ == "__main__":
    main()
