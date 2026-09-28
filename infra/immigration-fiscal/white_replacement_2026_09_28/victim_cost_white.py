"""Victim cost of violent offences by non-Hispanic white offenders, 2024, at the victim lane's victim-only prices,
and the same for a 40.9M slice of NH white residents.

A modified copy of black_comparator_rough_2026_09_28/victim_cost.py (the original is not edited), offender column
"White" (NCVS 2022-2024 codes Hispanic offenders separately, so White is non-Hispanic) and SHR p_off_nh_white.
Non-fatal: NCVS 2024 victimisations by victim group and offence x P(offender white | victim group), pooled 2022-2024,
unknown offenders spread in proportion. Homicide: CDC WONDER 2024 victims x SHR 2024 P(offender NH white | victim
group). Prices: Miller 2021 victim-only set, 2024 dollars. The same code with offender Black reproduces the Black
lane's victim_cost_summary.csv (gate).

The slice: 40,896,574 / CPS ASEC 2025 NH white population (keys.csv) of the total, charged to victims outside the
slice two ways: non-white victims only (every white victim counted inside, the lower bound the union's lane also
reports as its "Hispanic victims all in-group" arm), and outside a slice drawn at random from NH whites (white victims
outside the slice count as others).
Outputs: derived/victim_cost_white_by_offence.csv, derived/victim_cost_white_summary.csv.
"""
import csv
from pathlib import Path

import pandas as pd

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
DER = LANE / "derived"
NC = FISCAL / "ncvs_victim_offender_2026_09_18/derived"
VL = FISCAL / "crime_victim_cost_2026_09_23/derived"
BLACK = FISCAL / "black_comparator_rough_2026_09_28/derived/victim_cost_summary.csv"
NONFATAL = ["Rape/sexual assault", "Robbery", "Aggravated assault", "Simple assault"]
HOM = {"hispanic": "Hispanic", "nh_white": "White", "nh_black": "Black", "nh_other": "Other"}
SHR_COL = {"White": "p_off_nh_white", "Black": "p_off_nh_black"}
# Age arm: the NCVS lane's indirect standardisation (variant B, fine grid) puts the offending expected from the
# Hispanic age structure 1.18x the white one [DATA: ncvs_victim_offender_2026_09_18/derived/age_expected_offender_rate_fine_grid.csv]
AGE = pd.read_csv(NC / "age_expected_offender_rate_fine_grid.csv").set_index("group").index_vs_white_fine
UNION = {"central": 28.9229, "hispanic_victims_all_in_group": 23.4535}   # [DATA: crime_victim_cost_2026_09_23/derived/arms.csv]

nd = pd.read_csv(NC / "ndash_rate_by_victim_race.csv")
n24 = nd[nd.year.eq(2024) & nd.crimeType.isin(NONFATAL)].pivot(index="victim_race", columns="crimeType", values="count")
mx = pd.read_csv(NC / "matrix_pooled_2022_2024.csv")
price = pd.read_csv(VL / "unit_costs_victim_only_2024usd.csv")
price = price[price.price_set.eq("miller2021")].set_index("offence")
shr = pd.read_csv(VL / "shr_p_offender_given_victim.csv")
shr = shr[shr.window.astype(str).eq("2024")].set_index("victim")
won = pd.read_csv(VL / "wonder_2024_homicide_victims.csv").set_index("group").deaths_not_stated_allocated
keys = pd.read_csv(DER / "keys.csv").set_index("key").value
SLICE = 40_896_574.152351856 / float(keys["cps_population_nh_white_all"])


def rows_for(offender):
    p = mx[mx.offender.eq(offender)].set_index("victim").row_share_excl_unknown
    out = []
    for v in n24.index:
        for o in NONFATAL:
            n = n24.loc[v, o] * p[v]
            out.append(dict(offender=offender, victim=v, offence=o, n=n,
                            tangible_bn=n * price.loc[o, "victim_tangible"] / 1e9, full_bn=n * price.loc[o, "full"] / 1e9))
    for g, v in HOM.items():
        n = won[g] * shr.loc[g, SHR_COL[offender]]
        out.append(dict(offender=offender, victim=v, offence="Murder", n=n,
                        tangible_bn=n * price.loc["Murder", "victim_tangible"] / 1e9,
                        full_bn=n * price.loc["Murder", "full"] / 1e9))
    return pd.DataFrame(out)


def totals(x):
    h, nf = x[x.offence.eq("Murder")], x[x.offence.ne("Murder")]
    return dict(full_bn=x.full_bn.sum(), tangible_bn=x.tangible_bn.sum(), homicide_full_bn=h.full_bn.sum(),
                homicides=h.n.sum(), nonfatal_victimisations=nf.n.sum())


def write(name, rows, fields):
    with open(DER / name, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)


def main():
    blk = rows_for("Black")
    ref = pd.read_csv(BLACK)
    ref = ref[ref.arm.eq("ncvs_pooled_2022_2024")].set_index("victims")
    for who, x in (("non-Black victims", blk[blk.victim.ne("Black")]), ("all victims", blk)):
        if abs(totals(x)["full_bn"] - ref.loc[who, "full_bn"]) > 1e-3:
            raise SystemExit(f"[BLOCKED] Black offenders, {who}: {totals(x)['full_bn']} vs {ref.loc[who, 'full_bn']}")
    print("[gate] the Black offender run reproduces the Black lane's victim_cost_summary.csv")
    wht = rows_for("White")
    write("victim_cost_white_by_offence.csv",
          [{**r, "n": f"{r['n']:.2f}", "tangible_bn": f"{r['tangible_bn']:.5f}", "full_bn": f"{r['full_bn']:.5f}"}
           for r in wht.to_dict("records")], ["offender", "victim", "offence", "n", "tangible_bn", "full_bn"])
    nonwhite, white = totals(wht[wht.victim.ne("White")]), totals(wht[wht.victim.eq("White")])
    allv = totals(wht)
    summ = []

    def add(scope, victims, t, note=""):
        summ.append({"scope": scope, "victims": victims, **{k: f"{v:.4f}" for k, v in t.items()}, "note": note})

    add("all NH white offenders", "non-white victims", nonwhite)
    add("all NH white offenders", "white victims", white)
    add("all NH white offenders", "all victims", allv)
    sl = {k: v * SLICE for k, v in nonwhite.items()}
    add("40.9M slice", "non-white victims (lower bound)", sl,
        f"slice fraction {SLICE:.6f}; comparable to the union's {UNION['hispanic_victims_all_in_group']}")
    rnd = {k: SLICE * (nonwhite[k] + (1 - SLICE) * white[k]) for k in nonwhite}
    add("40.9M slice", "outside a random slice (central)", rnd,
        f"white victims outside the slice at 1 - {SLICE:.4f}; comparable to the union's central {UNION['central']}")
    for lab, t in (("non-white victims (lower bound)", sl), ("outside a random slice (central)", rnd)):
        add("40.9M slice at union ages", lab, {k: v * AGE["Hispanic"] for k, v in t.items()},
            f"x {AGE['Hispanic']:.4f}, the NCVS lane's age-only offending index, Hispanic over white")
    write("victim_cost_white_summary.csv", summ, list(summ[0]))
    for s in summ:
        print(f"{s['scope']:28s} {s['victims']:34s} full ${float(s['full_bn']):6.1f}bn tangible ${float(s['tangible_bn']):5.1f}bn"
              f" homicides {float(s['homicides']):7.0f} non-fatal {float(s['nonfatal_victimisations']) / 1e6:5.2f}m")


if __name__ == "__main__":
    main()
