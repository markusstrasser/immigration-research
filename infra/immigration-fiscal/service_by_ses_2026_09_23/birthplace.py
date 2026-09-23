"""Does current residence contaminate the geographic adjustment? A check with state of birth.

Military service moves people: soldiers live where they are stationed and many veterans settle
near bases. Adjustment (b) in `service.py` uses the state and metro of current residence, so a
group whose civilians cluster in a few states but whose service members are scattered over
white-majority base towns looks more military once it is reweighted to where whites live. For
the US-born, state of birth (`POBP` 1-56) is fixed before service. This script:
  1. tabulates, for US-born men and women, the share living outside their birth state and the
     service rates of stayers and movers (`derived/military_movers.csv`);
  2. repeats (b) with birth state and birth division in place of residence and without metro
     size (`derived/military_birthstate.csv`): raked on age (x education) and birth state, and
     indirectly standardised on white rates by age (x education) and birth state.
Persons born in Puerto Rico, the island areas or abroad to US parents form one "other" birth
state. Foreign-born groups have no US birthplace, so the check covers the US-born groups only.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("service", HERE / "service.py")
svc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(svc)

US_BORN = ["usb_mexican_hisp", "usb_mexican_ancestry", "usb_asian_indian_ancestry", "usb_asian_indian_race",
           "usb_nh_white", "usb_all"]
BANDS = {band: svc.BANDS[band] for band in ("18_49", "25_49", "25_34", "18_plus_born_1956_on")}


def cells(con, predicate):
    measures = {"pop": None, **svc.MILITARY}
    sums = []
    for name, flag in measures.items():
        sums += [f"{expr} AS {name}_{r}" for r, expr in enumerate(svc.replicate_sums(flag))]
    query = f"""
        WITH division AS (SELECT DISTINCT ST AS d_st, DIVISION AS d_div FROM persons)
        SELECT SEX AS sex, {svc.AGE_CELL} AS age_cell, (year - AGEP >= 1956)::INT AS post_draft,
               {svc.EDUC} AS educ,
               CASE WHEN POBP BETWEEN 1 AND 56 THEN POBP ELSE 99 END AS st,
               COALESCE(d.d_div, 10) AS division, 0 AS metro,
               (POBP <> p.ST)::INT AS mover,
               COUNT(*) AS n, SUM(PWGTP::BIGINT * PWGTP)::DOUBLE AS w2, {', '.join(sums)}
        FROM persons p LEFT JOIN division d ON d.d_st = p.POBP
        WHERE AGEP >= 18 AND ({predicate})
        GROUP BY ALL"""
    frame = con.execute(query).df()
    return svc.Cells(frame, ["sex", "age_cell", "post_draft", "educ", "st", "division", "metro", "mover"],
                     list(measures))


def main():
    con = svc.connect()
    data = {name: cells(con, svc.GROUPS[name][0]) for name in US_BORN}
    ref = data[svc.REFERENCE]
    outcomes = list(svc.MILITARY)
    mover_rows, adjusted_rows = [], []
    for name, group in data.items():
        for sex in (1, 2):
            for band, (ages, post_draft) in BANDS.items():
                def mask(c, mover=None):
                    m = (c.col("sex") == sex) & np.isin(c.col("age_cell"), ages)
                    if post_draft:
                        m &= c.col("post_draft") == 1
                    if mover is not None:
                        m &= c.col("mover") == mover
                    return m
                base = {"group": name, "sex": "men" if sex == 1 else "women", "age_band": band}
                mg, mr = mask(group), mask(ref)
                pop = group.data["pop"][mg].sum(0)
                share_movers = svc.ratio(group.data["pop"][mask(group, 1)].sum(0), pop)
                row = {**base, "share_outside_birth_state": share_movers[0], "share_se": svc.se(share_movers)}
                for label, flag in (("stayers", 0), ("movers", 1)):
                    g, r = mask(group, flag), mask(ref, flag)
                    theta = svc.ratio(group.data["ever_active_duty"][g].sum(0), group.data["pop"][g].sum(0))
                    white = svc.ratio(ref.data["ever_active_duty"][r].sum(0), ref.data["pop"][r].sum(0))
                    row.update({f"ever_rate_{label}": theta[0], f"ever_se_{label}": svc.se(theta),
                                f"ratio_{label}": (theta / white)[0], f"ratio_se_{label}": svc.se(theta / white),
                                f"records_{label}": int(group.n[g].sum())})
                mover_rows.append(row)
                if name == svc.REFERENCE:
                    continue
                specs = svc.specifications(group, ref, mg, mr, "pop", outcomes, False, "ever_active_duty")
                specs = {k.replace("b_", "b_birthstate_"): v for k, v in specs.items() if k.startswith("b_")}
                base["n_records"] = int(group.n[mg].sum())
                adjusted_rows += svc.spec_rows(base, specs, outcomes)
        print(f"  ✓ {name}", flush=True)
    pd.DataFrame(mover_rows).to_csv(svc.DERIVED / "military_movers.csv", index=False, float_format="%.6g",
                                    lineterminator="\n")
    pd.DataFrame(adjusted_rows).to_csv(svc.DERIVED / "military_birthstate.csv", index=False, float_format="%.6g",
                                       lineterminator="\n")
    print("  ✓ military_movers.csv, military_birthstate.csv")


if __name__ == "__main__":
    sys.exit(main())
