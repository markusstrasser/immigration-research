"""US births to Mexico-born mothers, 1980-2010, from the NCHS natality counts tabulated on Modal.

Input: `_cache/natality_counts_<run>.json` (natality_modal.py collect <run>; default r2, which
adds live birth order to r1 and must reproduce r1's totals). Output:
`derived/births_mexico_mothers.csv`.

Mother's birthplace by year (codes in sources/nchs_natality_codebook_excerpts.txt):
  1980-2002  mplbir == "57" (Mexico); foreign-born = mplbir in 55 Canada, 56 Cuba, 57 Mexico,
             59 remainder of world (52-54 are Puerto Rico, Virgin Islands, Guam: US-born)
  2003-2004  umbstate == "MX"; foreign-born = umbstate in CC Canada, CU Cuba, MX, YY rest of
             world (mbstate_rec == 2 "includes possessions", so it is not used)
  2005-2010  not on the public-use file ("available in the territory file only"; mbcntry
             blank, no nativity item). [MODEL]: births to mothers of Mexican Hispanic origin
             (umhisp == 1) times the Mexico-born share of those births. Central: share held at
             its 2003-04 measured mean (it was flat 2001-04). High: the 1995-2004 linear trend.
Live birth order: livord9 (1980-2002) / lbo_rec (2003+), 1 = first live birth, 9 = not stated.
Order counts births abroad too, so order 1 is a lower bound on a mother's first US-born child.
Resident births exclude restatus 4 (foreign residents), matching NCHS published totals.
Births to Mexico-born mothers resident abroad (restatus 4) are reported separately: those
children are US citizens too.
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = sys.argv[1] if len(sys.argv) > 1 else "r2"
COUNTS = HERE / "_cache" / f"natality_counts_{RUN}.json"
NCHS = HERE / "sources" / "nchs_births_gfr_us_1909_2018.csv"
OUT = HERE / "derived" / "births_mexico_mothers.csv"
TREND_YEARS = range(1995, 2005)
CONST_YEARS = (2003, 2004)
FOREIGN_MPLBIR = {"55", "56", "57", "59"}
FOREIGN_UMBSTATE = {"CC", "CU", "MX", "YY"}  # same four; mbstate_rec==2 would add possessions


def tabulate(rec: dict) -> dict:
    f = rec["fields"]
    t = dict(total_res=0, total_foreign_res=0, mx_res=0, mx_foreign_res=0, fb_res=0,
             mexorig_res=0, mx_first_res=0, mx_order_unknown_res=0, mexorig_first_res=0)
    for key, n in rec["counts"]:
        kv = dict(zip(f, key))
        w = int(kv["recwt"]) if kv.get("recwt", "").strip() else 1
        n *= w
        resident = kv["restatus"] != "4"
        if "mplbir" in kv:
            mx, fb = kv["mplbir"] == "57", kv["mplbir"] in FOREIGN_MPLBIR
        elif "umbstate" in kv:
            mx, fb = kv["umbstate"] == "MX", kv["umbstate"] in FOREIGN_UMBSTATE
        else:
            mx = fb = None
        hisp = kv.get("ormoth", kv.get("umhisp"))
        mexorig = hisp == "1" if hisp is not None else None
        order = kv.get("livord9", kv.get("lbo_rec"))
        if resident:
            t["total_res"] += n
            t["mx_res"] += n if mx else 0
            t["fb_res"] += n if fb else 0
            t["mexorig_res"] += n if mexorig else 0
            t["mx_first_res"] += n if (mx and order == "1") else 0
            t["mx_order_unknown_res"] += n if (mx and order == "9") else 0
            t["mexorig_first_res"] += n if (mexorig and order == "1") else 0
        else:
            t["total_foreign_res"] += n
            t["mx_foreign_res"] += n if mx else 0
        t["has_birthplace"] = mx is not None
        t["has_hispanic"] = mexorig is not None
        t["has_order"] = order is not None
    return t


def main() -> None:
    data = json.loads(COUNTS.read_text())
    nchs = {int(r["Year"]): int(r["Birth Number"]) for r in csv.DictReader(NCHS.open())}
    rows = {int(y): tabulate(rec) for y, rec in data.items()}
    if RUN != "r1":  # the birth-order run must reproduce r1 exactly
        r1 = {int(y): tabulate(rec) for y, rec in
              json.loads((HERE / "_cache" / "natality_counts_r1.json").read_text()).items()}
        for y in r1:
            for k in ("total_res", "mx_res", "mx_foreign_res", "mexorig_res"):
                if rows[y][k] != r1[y][k]:
                    sys.exit(f"[BLOCKED] {RUN} {y} {k} {rows[y][k]} != r1 {r1[y][k]}")

    share = {y: r["mx_res"] / r["mexorig_res"] for y, r in rows.items()
             if r["has_birthplace"] and r["has_hispanic"] and r["mexorig_res"]}
    xs = list(TREND_YEARS)
    ys = [share[y] for y in xs]
    mx_, my_ = sum(xs) / len(xs), sum(ys) / len(ys)
    slope = sum((x - mx_) * (y - my_) for x, y in zip(xs, ys)) / sum((x - mx_) ** 2 for x in xs)
    const = sum(share[y] for y in CONST_YEARS) / len(CONST_YEARS)
    has_order = all(r["has_order"] for r in rows.values())
    if has_order:
        first_share = sum(rows[y]["mx_first_res"] / rows[y]["mexorig_first_res"]
                          for y in CONST_YEARS) / len(CONST_YEARS)
    fr = [rows[y]["mx_foreign_res"] / rows[y]["mx_res"] for y in xs]
    fr_mean = sum(fr) / len(fr)

    out = []
    for y in sorted(rows):
        r = rows[y]
        trend = my_ + slope * (y - mx_)
        row = {"birth_year": y, "births_us_residents": r["total_res"],
               "nchs_published": nchs.get(y, ""),
               "gate_pct_diff": round(100 * (r["total_res"] / nchs[y] - 1), 4) if y in nchs else ""}
        if r["has_birthplace"]:
            row.update(
                births_mexico_born_mother=r["mx_res"],
                births_mexico_born_mother_high=r["mx_res"],
                births_mexico_born_mother_foreign_resident=r["mx_foreign_res"],
                births_mexico_born_mother_first=r["mx_first_res"] if has_order else "",
                births_mexico_born_mother_order_unknown=r["mx_order_unknown_res"] if has_order else "",
                births_foreign_born_mother=r["fb_res"],
                status="measured",
                field="mplbir==57" if y <= 2002 else "umbstate==MX")
        else:
            row.update(
                births_mexico_born_mother=round(r["mexorig_res"] * const),
                births_mexico_born_mother_high=round(r["mexorig_res"] * trend),
                births_mexico_born_mother_foreign_resident=round(r["mexorig_res"] * const * fr_mean),
                births_mexico_born_mother_first=(round(r["mexorig_first_res"] * first_share)
                                                 if has_order else ""),
                births_mexico_born_mother_order_unknown="",
                births_foreign_born_mother="",
                status="[MODEL]",
                field=f"umhisp==1 x Mexico-born share {const:.4f} (high: 1995-2004 trend)")
        row.update(
            births_mexican_origin_mother=r["mexorig_res"] if r["has_hispanic"] else "",
            mexico_born_share_of_mexican_origin=round(share[y], 4) if y in share else "",
            model_share_central=round(const, 4), model_share_high=round(trend, 4))
        out.append(row)
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    print(f"✓ wrote {OUT.name} from {RUN}: {len(out)} years; share central {const:.4f} "
          f"(2003-04), trend {my_:.3f} at {mx_:.1f} slope {slope:+.4f}/yr; "
          f"foreign-resident ratio {fr_mean:.4f}; birth order {'yes' if has_order else 'no'}")


if __name__ == "__main__":
    main()
