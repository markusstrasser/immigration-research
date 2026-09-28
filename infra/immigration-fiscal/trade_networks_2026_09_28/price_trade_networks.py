"""Price the trade, travel and FDI network benefit of the Mexican-origin union to other US residents.

Welfare, never volume: a three-region (US, Mexico, rest of world) one-sector Armington/ACR model solved in
exact hat algebra with fixed nominal deficits (Dekle-Eaton-Kortum 2008; Arkolakis-Costinot-Rodriguez-Clare
2012). Removing the network raises US<->Mexico trade costs so that, holding prices, the affected flow falls
by share s. The US welfare change is real expenditure; other residents get (1 - group consumption share).

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/trade_networks_2026_09_28/price_trade_networks.py
"""

import csv
import json
import math
from pathlib import Path

import numpy as np

LANE = Path(__file__).resolve().parent
OUT = LANE / "derived"

# ---- inputs, $bn 2024 (sources in RESULT.md and derived/inputs.csv) ----
IN = {
    "us_gdp": 29298.013,  # BEA NIPA A191RC 2024
    "us_exports_gs": 3215.368,  # BEA NIPA B020RC 2024
    "us_imports_gs": 4113.828,  # BEA NIPA B021RC 2024
    "us_goods_exports_mx": 334.4921,  # Census c2010 (Mexico) 2024 total
    "us_goods_imports_mx": 503.1101,  # Census c2010 (Mexico) 2024 total
    "us_services_exports_mx": 50.4,  # BEA services by country (mirror; GAP)
    "us_services_imports_mx": 45.1,  # BEA services by country (mirror; GAP)
    "us_travel_exports_mx": 22.2,  # BEA travel exports to Mexico (mirror; GAP)
    "us_travel_imports_mx": 26.3,  # BEA travel imports from Mexico (mirror; GAP)
    "us_travel_exports_all": 215.039,  # BEA ITA Table 3 line 17, 2024
    "us_travel_imports_all": 177.755,  # BEA ITA Table 3 line 49, 2024
    "mx_gdp": 1830.489311,  # World Bank NY.GDP.MKTP.CD 2024
    "mx_exports_gs": 682.472610,  # World Bank NE.EXP.GNFS.CD 2024
    "mx_imports_gs": 698.190456,  # World Bank NE.IMP.GNFS.CD 2024
    "world_gdp": 111669.432109,  # World Bank NY.GDP.MKTP.CD 2024 (WLD)
    "usdia_position_mx": 155.901,  # BEA usdia-detailedcountry, 2024 historical cost
    "usdia_position_all": 6697.705,  # same file, all countries 2024
    "usdia_holding_mx": 15.294,  # BEA usdia-position-2020-2025.xlsx sheet 2024, holding companies (nonbank)
    "usdia_holding_all": 3192.847,  # same sheet, all countries
    "general_sales_tax": 602.43,  # consumption_key_2026_09_24 RESULT, national line
    "selective_excise": 371.262,  # same table
    "pce": 19896.009,  # BEA NIPA DPCERC 2024
}
POP = {  # CPS 2025 target population (crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv)
    "union": 40896574.2,
    "mexico_born": 12220781.9,
    "descendants": 14333217.7 + 14342574.6,
    "cps_all": 336727803.0,
}
GROUP_CONSUMPTION_SHARE = 0.0889377186431963  # consumption_key_2026_09_24 key_specs.csv saving_central key_share
VFR_SHARE_ALL_INBOUND = 0.229  # NTTO SIAT 2024, all inbound air travelers, VFR main purpose

ARMS = {
    # s_first: share of US<->Mexico non-travel trade that the Mexico-born network creates (PE)
    "low": {"eps": 8.0, "s_first": 0.02, "w_desc": 0.0, "vfr_share": 0.15, "vfr_attrib": 0.8,
            "tax": IN["general_sales_tax"] / IN["pce"], "fdi_s": 0.0, "fdi_excess": 0.0},
    "central": {"eps": 5.0, "s_first": 1 - math.exp(-0.0860), "w_desc": 0.0, "vfr_share": 0.215,
                "vfr_attrib": 0.9, "tax": IN["general_sales_tax"] / IN["pce"],
                "fdi_s": 1 - math.exp(-0.0860), "fdi_excess": 0.01},
    "high": {"eps": 4.0, "s_first": 1 - math.exp(-0.17), "w_desc": 0.2, "vfr_share": 0.25, "vfr_attrib": 1.0,
             "tax": (IN["general_sales_tax"] + IN["selective_excise"]) / IN["pce"],
             "fdi_s": 1 - math.exp(-math.log(1.29) / math.log(2)), "fdi_excess": 0.02},
}
U, M, R = 0, 1, 2


def trade_matrix():
    """X[i, j] = sales of region i to region j, $bn; income Y_i = GDP_i by construction."""
    x_um = IN["us_goods_exports_mx"] + IN["us_services_exports_mx"]
    x_mu = IN["us_goods_imports_mx"] + IN["us_services_imports_mx"]
    x_ur = IN["us_exports_gs"] - x_um
    x_ru = IN["us_imports_gs"] - x_mu
    x_mr = IN["mx_exports_gs"] - x_mu
    x_rm = IN["mx_imports_gs"] - x_um
    gdp_r = IN["world_gdp"] - IN["us_gdp"] - IN["mx_gdp"]
    X = np.array([
        [IN["us_gdp"] - IN["us_exports_gs"], x_um, x_ur],
        [x_mu, IN["mx_gdp"] - IN["mx_exports_gs"], x_mr],
        [x_ru, x_rm, gdp_r - x_ru - x_rm],
    ])
    assert (X > 0).all()
    return X


X = trade_matrix()
Y = X.sum(axis=1)
E = X.sum(axis=0)
D = E - Y
PI = X / E[None, :]


def solve(keep, eps):
    """keep[i, j] = tau_hat_ij^(-eps): the PE share of flow i->j that survives. Returns welfare hats."""
    w = np.ones(3)
    for _ in range(200000):
        num = PI * (w[:, None] ** (-eps)) * keep
        den = num.sum(axis=0)
        e_new = w * Y + D
        y_new = ((num / den[None, :]) * e_new[None, :]).sum(axis=1)
        excess = (y_new - w * Y) / (w * Y)  # labour-market excess demand, relative
        if np.max(np.abs(excess)) < 1e-13:
            break
        w = w * (1.0 + 0.2 * excess / eps)
        w *= Y.sum() / (w * Y).sum()  # numeraire: world GDP unchanged
    else:
        raise RuntimeError("GE solver did not converge")
    num = PI * (w[:, None] ** (-eps)) * keep
    p_hat = num.sum(axis=0) ** (-1.0 / eps)
    return ((w * Y + D) / E) / p_hat


def keep_matrix(cuts):
    """cuts: {(i, j): $bn of PE flow removed}; returns keep = 1 - cut/flow."""
    k = np.ones((3, 3))
    for (i, j), amount in cuts.items():
        k[i, j] -= amount / X[i, j]
    return k


def us_gain(cuts, eps):
    """Real US expenditure lost when the network's flows are removed = the network's benefit, $bn."""
    return (1.0 - solve(keep_matrix(cuts), eps)[U]) * E[U]


def info_cuts(s, scale_all=None):
    """Information channel on non-travel flows. scale_all=phi applies phi*s to every US partner."""
    nt_um = X[U, M] - IN["us_travel_exports_mx"]
    nt_mu = X[M, U] - IN["us_travel_imports_mx"]
    cuts = {(U, M): s * nt_um, (M, U): s * nt_mu}
    if scale_all is not None:
        nt_ur = X[U, R] - (IN["us_travel_exports_all"] - IN["us_travel_exports_mx"])
        nt_ru = X[R, U] - (IN["us_travel_imports_all"] - IN["us_travel_imports_mx"])
        cuts = {k: v * scale_all for k, v in cuts.items()}
        cuts[(U, R)] = scale_all * s * nt_ur
        cuts[(R, U)] = scale_all * s * nt_ru
    return cuts


def main():
    OUT.mkdir(exist_ok=True)
    assert abs(D.sum()) < 1e-6
    assert abs(solve(np.ones((3, 3)), 5.0)[U] - 1.0) < 1e-12
    phi = POP["union"] / POP["cps_all"]
    other = 1.0 - GROUP_CONSUMPTION_SHARE
    ratio_desc = POP["descendants"] / POP["mexico_born"]
    res = {}
    for arm, a in ARMS.items():
        eps = a["eps"]
        s_first = a["s_first"]
        s_union = s_first * (1.0 + ratio_desc * a["w_desc"])
        g_first = us_gain(info_cuts(s_first), eps) * other
        g_union = us_gain(info_cuts(s_union), eps) * other
        g_avg = us_gain(info_cuts(s_union, scale_all=phi), eps) * other
        vfr = a["vfr_attrib"] * a["vfr_share"] * IN["us_travel_exports_mx"]
        g_vfr_tot = us_gain({(U, M): vfr}, eps) * other
        g_vfr = g_vfr_tot + a["tax"] * vfr * other
        vfr_avg_mx = phi * a["vfr_attrib"] * VFR_SHARE_ALL_INBOUND * IN["us_travel_exports_mx"]
        vfr_avg_row = phi * a["vfr_attrib"] * VFR_SHARE_ALL_INBOUND * (
            IN["us_travel_exports_all"] - IN["us_travel_exports_mx"])
        g_vfr_avg = us_gain({(U, M): vfr_avg_mx, (U, R): vfr_avg_row}, eps) * other + a["tax"] * (
            vfr_avg_mx + vfr_avg_row) * other
        both = info_cuts(s_union)
        both[(U, M)] += vfr
        g_both = us_gain(both, eps) * other
        # holding-company positions are pass-through vehicles, not network-created: excluded on both sides
        pos_mx = IN["usdia_position_mx"] - IN["usdia_holding_mx"]
        pos_all = IN["usdia_position_all"] - IN["usdia_holding_all"]
        fdi = a["fdi_s"] * pos_mx * a["fdi_excess"] * other
        fdi_avg = phi * a["fdi_s"] * pos_all * a["fdi_excess"] * other
        pe_import_side = s_union * (X[M, U] - IN["us_travel_imports_mx"]) / eps * other
        res[arm] = {
            "eps": eps, "s_first": s_first, "s_union": s_union, "trade_first": g_first,
            "trade_union": g_union, "trade_desc": g_union - g_first, "trade_avg": g_avg,
            "vfr_spend_bn": vfr, "vfr_tot": g_vfr_tot, "vfr": g_vfr, "vfr_avg": g_vfr_avg,
            "trade_plus_vfr_joint": g_both, "additivity_gap": g_both - g_union - g_vfr_tot,
            "fdi": fdi, "fdi_avg": fdi_avg, "pe_import_side_check": pe_import_side,
            "created_trade_bn": s_union * (X[U, M] - IN["us_travel_exports_mx"] + X[M, U]
                                           - IN["us_travel_imports_mx"]),
        }
    grid = []
    for s in (0.02, ARMS["central"]["s_first"], ARMS["high"]["s_first"], res["high"]["s_union"]):
        for eps in (4.0, 5.0, 8.0):
            grid.append({"s": round(s, 6), "eps": eps,
                         "gain_other_residents_bn": round(us_gain(info_cuts(s), eps) * other, 4)})

    rows = []

    def add(item, group, measure, key, ev, dc, note, per_member=True):
        lo, ce, hi = (-res[a][key] if isinstance(key, str) else -key(res[a]) for a in ("low", "central", "high"))
        rows.append({"item": item, "group": group, "measure": measure, "low_bn": f"{lo:.4f}",
                     "central_bn": f"{ce:.4f}", "high_bn": f"{hi:.4f}",
                     "per_member_usd": f"{ce * 1e9 / POP['union']:.2f}" if per_member else "",
                     "evidence_level": ev, "double_count_with": dc, "method_note": note})

    ev_trade = "modelled: published network elasticities (marginal) extrapolated to the whole stock; ACR/DEK welfare"
    dc_trade = "none found: production term P is native wages; consumer-price channel is domestic services"
    add("trade_information_channel", "mexico_born", "absolute", "trade_first", ev_trade, dc_trade,
        "3-region DEK/ACR GE; non-travel US-Mexico flows fall by s (0.02 / 1-exp(-0.086) / 1-exp(-0.17)); "
        "eps 8/5/4; x (1 - group consumption share 0.0889); per member = per union member")
    add("trade_information_channel", "us_born_descendants", "absolute", "trade_desc", ev_trade, dc_trade,
        "incremental over the Mexico-born: 0 unless descendants carry weight w (high arm w=0.2 per head)")
    add("trade_information_channel", "union", "absolute", "trade_union", ev_trade, dc_trade,
        "union total = Mexico-born + descendants rows (GE non-additivity < $0.01bn)")
    add("trade_information_channel", "union", "normalized", lambda r: r["trade_union"] - r["trade_avg"],
        ev_trade, dc_trade, "absolute minus 40.9m average residents, who carry 12.15% of every origin's "
        "network and create phi*s of US trade with every partner, same s and eps")
    add("trade_preference_channel", "union", "absolute", lambda r: 0.0,
        "not a gain to others", "the group's own consumption in the account",
        "imports the group buys because it prefers home-country goods leave with the group; excluded")
    ev_vfr = "measured spending and trip shares; assumed attribution; GE terms-of-trade + foreign-paid sales tax"
    add("visitor_spending_vfr", "union", "absolute", "vfr", ev_vfr, "trade line excludes travel",
        "Mexican VFR travel exports = attribution (0.8/0.9/1.0) x VFR share (0.15/0.215/0.25) x $22.2bn; "
        "welfare = GE loss of the export + sales-tax rate (3.0%/3.0%/4.9%) x spending, x 0.911")
    add("visitor_spending_vfr", "union", "normalized", lambda r: r["vfr"] - r["vfr_avg"], ev_vfr,
        "trade line excludes travel", "absolute minus 12.15% of all inbound VFR travel exports "
        "(VFR share 0.229 of $215.0bn, same attribution) priced the same way")
    ev_fdi = "speculative: created position x assumed excess return"
    add("fdi_excess_return", "union", "absolute", "fdi", ev_fdi, "trade line (FDI-linked trade counted there)",
        "US direct investment position in Mexico excluding holding companies $140.6bn x created share (0 / 0.082 / 0.307 from BCH 29% per "
        "doubling) x excess return (0 / 1 / 2 pp) x 0.911")
    add("fdi_excess_return", "union", "normalized", lambda r: r["fdi"] - r["fdi_avg"], ev_fdi,
        "trade line", "absolute minus 12.15% of the $3,504.9bn outward position outside holding companies, same share and return")
    add("total_trade_travel_fdi", "union", "absolute", lambda r: r["trade_union"] + r["vfr"] + r["fdi"],
        "sum of the three lines", "see rows", "stacked: low with low, high with high")
    add("total_trade_travel_fdi", "union", "normalized",
        lambda r: (r["trade_union"] - r["trade_avg"]) + (r["vfr"] - r["vfr_avg"]) + (r["fdi"] - r["fdi_avg"]),
        "sum of the three lines", "see rows", "stacked: low with low, high with high")

    fields = ["item", "group", "measure", "low_bn", "central_bn", "high_bn", "per_member_usd", "evidence_level",
              "double_count_with", "method_note"]
    with open(OUT / "items.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)
    with open(OUT / "grid.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=["s", "eps", "gain_other_residents_bn"], lineterminator="\n")
        wr.writeheader()
        wr.writerows(grid)
    with open(OUT / "inputs.csv", "w", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["name", "value"])
        for k, v in IN.items():
            wr.writerow([k, v])
        for k, v in POP.items():
            wr.writerow([f"pop_{k}", v])
        wr.writerow(["group_consumption_share", GROUP_CONSUMPTION_SHARE])
    calib = {"X_bn": X.round(3).tolist(), "Y_bn": Y.round(3).tolist(), "E_bn": E.round(3).tolist(),
             "D_bn": D.round(3).tolist(), "pi_us_from_mx": float(PI[M, U]), "lambda_us": float(PI[U, U]),
             "phi_average_resident_share": phi, "other_residents_share": other}
    summary = {"calibration": calib,
               "arms": {a: {k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()}
                        for a, r in res.items()}}
    with open(OUT / "summary.json", "w") as f:
        json.dump(summary, f, indent=1)
        f.write("\n")
    for a, r in res.items():
        print(a, {k: round(v, 4) for k, v in r.items()})
    print("pi_MX in US spending", round(PI[M, U], 5), "lambda_US", round(PI[U, U], 5))


if __name__ == "__main__":
    main()
