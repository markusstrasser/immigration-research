"""Rough victim cost of violent offences by non-Hispanic Black offenders, 2024, on the victim lane's victim-only prices.

Non-fatal: NCVS 2024 victimisations by victim group and offence (ncvs lane ndash table) x P(offender Black | victim
group) from the pooled 2022-2024 NCVS matrix, unknown offenders spread in proportion. A second arm takes the 2019
by-crime-type matrix. Homicide: CDC WONDER 2024 victims x SHR 2024 P(offender NH Black | victim group). Prices: Miller
2021 victim-only set in 2024 dollars. The national row applies the same prices to every 2024 victimisation and homicide.
Also writes the CPS ASEC 2025 profile of the two groups.
Outputs: derived/victim_cost_by_offence.csv, derived/victim_cost_summary.csv, derived/cps_profile.csv.
"""
import csv
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
DER = LANE / "derived"
NC = FISCAL / "ncvs_victim_offender_2026_09_18/derived"
VL = FISCAL / "crime_victim_cost_2026_09_23/derived"
ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
NONFATAL = ["Rape/sexual assault", "Robbery", "Aggravated assault", "Simple assault"]
HOM = {"hispanic": "Hispanic", "nh_white": "White", "nh_black": "Black", "nh_other": "Other"}

nd = pd.read_csv(NC / "ndash_rate_by_victim_race.csv")
n24 = nd[nd.year.eq(2024) & nd.crimeType.isin(NONFATAL)].pivot(index="victim_race", columns="crimeType", values="count")
mx = pd.read_csv(NC / "matrix_pooled_2022_2024.csv")
p_blk = mx[mx.offender.eq("Black")].set_index("victim").row_share_excl_unknown
m19 = pd.read_csv(NC / "matrix_by_crime_type_2019.csv")
m19 = m19[m19.offender.ne("Unknown")]
p19 = {s: (m19[m19.scope.eq(s)].pivot(index="victim", columns="offender", values="count")
           .pipe(lambda t: t["Black"] / t.sum(axis=1))) for s in ("serious_violent", "simple_assault")}
price = pd.read_csv(VL / "unit_costs_victim_only_2024usd.csv")
price = price[price.price_set.eq("miller2021")].set_index("offence")
shr = pd.read_csv(VL / "shr_p_offender_given_victim.csv")
shr = shr[shr.window.astype(str).eq("2024")].set_index("victim").p_off_nh_black
won = pd.read_csv(VL / "wonder_2024_homicide_victims.csv").set_index("group").deaths_not_stated_allocated
ARMS = {
    "ncvs_pooled_2022_2024": lambda v, o: p_blk[v],
    # the 2019 matrix has no Other victim row; that row keeps the pooled share
    "ncvs_2019_by_crime_type": lambda v, o: p19["simple_assault" if o == "Simple assault" else "serious_violent"]
    .get(v, p_blk[v]),
}


def rows_for(arm, p_of):
    out = []
    for v in n24.index:
        for o in NONFATAL:
            n = n24.loc[v, o] * p_of(v, o)
            out.append(dict(arm=arm, victim=v, offence=o, n=n, tangible_bn=n * price.loc[o, "victim_tangible"] / 1e9,
                            full_bn=n * price.loc[o, "full"] / 1e9))
    for g, v in HOM.items():
        n = won[g] * (1.0 if arm == "national_all_offenders" else shr[g])
        out.append(dict(arm=arm, victim=v, offence="Murder", n=n,
                        tangible_bn=n * price.loc["Murder", "victim_tangible"] / 1e9,
                        full_bn=n * price.loc["Murder", "full"] / 1e9))
    return out


def write(name, rows, fields):
    with open(DER / name, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)


def main():
    by = [r for arm, f in ARMS.items() for r in rows_for(arm, f)] + rows_for("national_all_offenders", lambda v, o: 1.0)
    df = pd.DataFrame(by)
    write("victim_cost_by_offence.csv", [{**r, "n": f"{r['n']:.2f}", "tangible_bn": f"{r['tangible_bn']:.5f}",
                                          "full_bn": f"{r['full_bn']:.5f}"} for r in by],
          ["arm", "victim", "offence", "n", "tangible_bn", "full_bn"])
    summ = []
    for arm, d in df.groupby("arm", sort=False):
        whos = [("all victims", d)] if arm == "national_all_offenders" else [
            ("non-Black victims", d[d.victim.ne("Black")]), ("Black victims", d[d.victim.eq("Black")]), ("all victims", d)]
        for who, x in whos:
            h, nf = x[x.offence.eq("Murder")], x[x.offence.ne("Murder")]
            summ.append({"arm": arm, "victims": who, "full_bn": f"{x.full_bn.sum():.4f}",
                         "tangible_bn": f"{x.tangible_bn.sum():.4f}", "homicide_full_bn": f"{h.full_bn.sum():.4f}",
                         "homicides": f"{h.n.sum():.1f}", "nonfatal_victimisations": f"{nf.n.sum():.0f}"})
            print(f"{arm:24s} {who:18s} full ${x.full_bn.sum():6.1f}bn (homicide {h.full_bn.sum():5.1f}, "
                  f"{h.n.sum():6.0f} deaths)  tangible ${x.tangible_bn.sum():5.1f}bn  non-fatal {nf.n.sum() / 1e6:.2f}m")
    write("victim_cost_summary.csv", summ, list(summ[0]))

    # CPS ASEC 2025: who the two groups are.
    C = ["PH_SEQ", "MARSUPWT", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PRDTHSP",
         "PEHSPNON", "PRDTRACE", "PEARNVAL", "PTOTVAL"]
    with zipfile.ZipFile(ZIP) as z:
        c = pd.read_csv(z.open("pppub25.csv"), usecols=C)
    us = [57, 60, 66, 69, 73, 78]
    civ = (c.PRPERTYP.eq(2) | c.A_AGE.lt(15)).to_numpy()
    nat = c.PRCITSHP.isin([1, 2, 3])
    grp = {"mexican_origin": ((c.PRCITSHP.isin([4, 5]) & c.PENATVTY.eq(303)) | (nat & (c.PEFNTVTY.eq(303) | c.PEMNTVTY.eq(303)))
                              | (nat & c.PEFNTVTY.isin(us) & c.PEMNTVTY.isin(us) & c.PRDTHSP.eq(1))).to_numpy() & civ,
           "nh_black": (c.PEHSPNON.eq(2) & c.PRDTRACE.eq(2)).to_numpy() & civ, "all": civ}
    w = c.MARSUPWT.to_numpy(float) / 100
    hsize = c.groupby("PH_SEQ").PH_SEQ.transform("size").to_numpy(float)
    earn = c.PEARNVAL.clip(lower=0).to_numpy(float)
    inc = c.PTOTVAL.clip(lower=0).to_numpy(float)
    age = c.A_AGE.to_numpy()
    prof = []
    for g, m in grp.items():
        a = m & (age >= 25) & (age <= 64)
        ww = w[m]
        prof.append({"group": g, "population": f"{ww.sum():.0f}",
                     "under_18_share": f"{w[m & (age < 18)].sum() / ww.sum():.4f}",
                     "age_65_plus_share": f"{w[m & (age >= 65)].sum() / ww.sum():.4f}",
                     "household_size": f"{np.average(hsize[m], weights=ww):.3f}",
                     "income_per_person": f"{np.average(inc[m], weights=ww):.0f}",
                     "working_share_25_64": f"{np.average(earn[a] > 0, weights=w[a]):.4f}",
                     "earnings_per_adult_25_64": f"{np.average(earn[a], weights=w[a]):.0f}",
                     "earnings_per_worker_25_64": f"{np.average(earn[a & (earn > 0)], weights=w[a & (earn > 0)]):.0f}"})
        print(" ".join(f"{k}={v}" for k, v in prof[-1].items()))
    write("cps_profile.csv", prof, list(prof[0]))


if __name__ == "__main__":
    main()
