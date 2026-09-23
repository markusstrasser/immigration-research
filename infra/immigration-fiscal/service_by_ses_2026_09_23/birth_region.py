"""Where is the Mexican-origin service gap? Ever on active duty by region of birth and by region
of residence, US-born men and women, against US-born non-Hispanic whites born (or living) in the
same region, raw and at the same ages.

Raking to the white geography (`service.py` b_raked_*, `birthplace.py` b_birthstate_raked_*)
puts US-born Mexican-origin men above whites; indirect standardisation on the same cells puts
them below. The two answer different questions when the group-to-white ratio differs by place:
raking weights the regions where whites live, indirect standardisation those where the group
lives. This table shows the ratio region by region. Regions are the nine census divisions with
California and Texas split out, and one bucket for births outside the 50 states and DC.
"Age-standardised" = the group's rate against white rates by age cell (`service.AGE_CELL`) in
the same region, weighted by the group's own ages. Writes `derived/military_by_region.csv`.
"""
import importlib.util
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("service", HERE / "service.py")
svc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(svc)

GROUPS = ["usb_mexican_hisp", "usb_mexican_ancestry", "usb_asian_indian_ancestry", "usb_nh_white"]
DIVISIONS = {1: "new_england", 2: "middle_atlantic", 3: "east_north_central", 4: "west_north_central",
             5: "south_atlantic", 6: "east_south_central", 7: "west_south_central_ex_texas", 8: "mountain",
             9: "pacific_ex_california", 10: "outside_states", 11: "california", 12: "texas"}
BANDS = ("18_49", "25_49")


def region(state, division):
    return f"CASE WHEN {state} = 6 THEN 11 WHEN {state} = 48 THEN 12 ELSE COALESCE({division}, 10) END"


def cells(con, predicate):
    sums = []
    for name, flag in (("pop", None), ("ever", "MIL IN (1, 2)")):
        sums += [f"{expr} AS {name}_{r}" for r, expr in enumerate(svc.replicate_sums(flag))]
    query = f"""
        WITH division AS (SELECT DISTINCT ST AS d_st, DIVISION AS d_div FROM persons)
        SELECT SEX AS sex, {svc.AGE_CELL} AS age_cell,
               {region('POBP', 'd.d_div')} AS birth_region, {region('p.ST', 'p.DIVISION')} AS residence_region,
               COUNT(*) AS n, {', '.join(sums)}
        FROM persons p LEFT JOIN division d ON d.d_st = p.POBP
        WHERE AGEP BETWEEN 18 AND 49 AND ({predicate})
        GROUP BY ALL"""
    return con.execute(query).df()


def main():
    con = svc.connect()
    frames = {name: cells(con, svc.GROUPS[name][0]) for name in GROUPS}
    pop = [f"pop_{r}" for r in range(svc.R)]
    ever = [f"ever_{r}" for r in range(svc.R)]
    white = frames[svc.REFERENCE]
    rows = []
    for name, frame in frames.items():
        for sex in (1, 2):
            for band in BANDS:
                ages = svc.BANDS[band][0]
                for by in ("birth_region", "residence_region"):
                    def pick(f, where):
                        m = (f.sex == sex) & f.age_cell.isin(ages)
                        return f[m & (f[by] == where)] if where != "all" else f[m]
                    total = pick(frame, "all")[pop].sum().to_numpy()
                    for where in ["all"] + sorted(frame[by].unique()):
                        g, w = pick(frame, where), pick(white, where)
                        if g.empty or w.empty:
                            continue
                        g_age = g.groupby("age_cell")[pop + ever].sum()
                        w_age = w.groupby("age_cell")[pop + ever].sum().reindex(g_age.index).fillna(0.0)
                        white_by_age = svc.ratio(w_age[ever].to_numpy(), w_age[pop].to_numpy())
                        expected = (g_age[pop].to_numpy() * white_by_age).sum(0)
                        observed = g[ever].sum().to_numpy()
                        theta = svc.ratio(observed, g[pop].sum().to_numpy())
                        ref = svc.ratio(w[ever].sum().to_numpy(), w[pop].sum().to_numpy())
                        share = svc.ratio(g[pop].sum().to_numpy(), total)
                        age_ratio = svc.ratio(observed, expected)
                        rows.append({"group": name, "sex": "men" if sex == 1 else "women", "age_band": band,
                                     "by": by, "region": "all" if where == "all" else DIVISIONS[int(where)],
                                     "n_records": int(g.n.sum()), "share_of_group": share[0],
                                     "share_se": svc.se(share), "rate": theta[0], "se": svc.se(theta),
                                     "white_rate": ref[0], "white_se": svc.se(ref), "ratio": (theta / ref)[0],
                                     "ratio_se": svc.se(theta / ref), "ratio_age_standardised": age_ratio[0],
                                     "ratio_age_standardised_se": svc.se(age_ratio),
                                     "white_age_cells_missing": int((w_age[pop[0]] == 0).sum())})
        print(f"  ✓ {name}", flush=True)
    out = pd.DataFrame(rows)
    out.to_csv(svc.DERIVED / "military_by_region.csv", index=False, float_format="%.6g", lineterminator="\n")
    print(f"  ✓ military_by_region.csv: {len(out)} rows")
    show = out[(out.sex == "men") & (out.age_band == "18_49") & (out.group == "usb_mexican_hisp")]
    print(show[["by", "region", "n_records", "share_of_group", "rate", "white_rate", "ratio",
                "ratio_age_standardised", "ratio_age_standardised_se"]].round(3).to_string(index=False))


if __name__ == "__main__":
    sys.exit(main())
