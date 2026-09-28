"""Crash costs that the Mexican-origin union's driving imposes on other US residents, 2024 $.

Cost base: Blincoe et al. (2023), NHTSA DOT HS 813 403, comprehensive costs of 2019 crashes,
less crash congestion (priced by congestion_2026_09_23) and EMS (inside the account's public
safety lines). Economic parts move with CPI-U, quality-of-life parts with the USDOT VSL, and
counts to 2023 (latest FARS/CRSS year, Traffic Safety Facts 2023 Tables 1-2).

(a) absolute, with the group's driving against without it (but-for). For each crash class the
    outsider losses the group's traffic adds are
      multi-vehicle:  x * m * s * (1 - q) * M  + liability flows between the two sides
      non-motorist:   beta * m * [s (1 - q) / (1 - s)] * (1 - h) * P
      single-vehicle: m * s * S * e_sv
    x is the elasticity of the per-mile multi-vehicle crash rate with respect to traffic (0: the
    group's crashes replace crashes others would have had with each other; 1: Vickrey pairwise),
    beta the elasticity of non-motorist crashes with respect to motor traffic, m the group's
    involvement per mile relative to the average driver, s its share of traffic, q the chance
    that the other party is a group member, h the group's share of non-motorist victims.
(b) normalized: E_a * (1 - 1/R), R = the group's VMT per person relative to the average
    resident times m. It is what the group's driving costs others beyond what the same number
    of average residents' driving would.
Variant: fault-based attribution (outsider losses in crashes the group's drivers cause, less
their liability payments), which does not depend on x or beta.
"""
import csv
import itertools
import json
from pathlib import Path

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]
OUT = LANE / "derived"

# --- Blincoe et al. 2023, 2019 $ millions. Table 1-8 rows by severity. [SOURCE]
SEV = ["PDO", "MAIS0", "MAIS1", "MAIS2", "MAIS3", "MAIS4", "MAIS5", "Fatal"]
ECON = dict(zip(SEV, [101282, 14718, 74963, 30504, 39629, 13031, 7039, 58643]))
QALY = dict(zip(SEV, [0, 0, 159320, 171847, 249002, 56658, 36432, 352293]))
CONG = dict(zip(SEV, [25595, 4562, 4677, 572, 239, 35, 13, 260]))
EMS = dict(zip(SEV, [598, 109, 411, 97, 69, 19, 7, 39]))
# Tables 12-2 and 12-8: comprehensive costs of pedestrian and bicyclist injuries [SOURCE]
PED = dict(zip(SEV, [34, 411, 5445, 10061, 18218, 3250, 3618, 71506]))
BIKE = dict(zip(SEV, [44, 257, 3666, 6046, 9492, 1496, 1495, 9734]))
PAYER_OTHER_NONCONG = 48617 - 35954  # Table 15-5, "Other" less congestion [CALCULATION]

# --- prices: CPI-U annual averages (BLS CUUR0000SA0) [TRAINING-DATA; 2024 value as used in
# disease_food_2026_09_28/price_items.py]; USDOT VSL $10.9m (2019) and $13.7m (2024) [SOURCE:
# transportation.gov VSL guidance table]
CPI_2019, CPI_2024 = 255.657, 313.689
VSL_2019, VSL_2024 = 10.9, 13.7
# --- counts, Traffic Safety Facts 2023 (DOT HS 813 738) Tables 1-2 [SOURCE]
KILLED = {2019: 36355, 2020: 39007, 2023: 40901}
INJURED = {2019: 2740141, 2020: 2282209, 2023: 2442581}
PDO_CRASHES = {2019: 4806253, 2020: 3621681, 2023: 4403453}
INJ_CRASHES = {2019: 1916344, 2020: 1593390, 2023: 1697252}
VMT_M = {2019: 3261772, 2020: 2903622, 2023: 3246817}
# TSF 2023 Tables 28-29: multi-vehicle share of crashes that involve no non-motorist [SOURCE]
MV_SHARE_INJ = 1197812 / (1197812 + 499440 - 60848 - 49361)
MV_SHARE_PDO = 3132342 / (3132342 + 1271111 - 1416 - 5737)

fars = json.loads((OUT / "fars_group_2023.json").read_text())
MV_SHARE_FATAL = fars["occupant_deaths_multivehicle_share"]  # FARS 2023 occupant deaths [CALCULATION]
PAX_OUT = 1 - fars["passengers_killed_with_killed_hispanic_driver_hispanic_share"]
SV_PAX = fars["single_vehicle_passenger_share_of_occupant_deaths"]
HISP_PED = fars["hispanic_share_of_known_origin_pedestrian_deaths"]
MH = fars["within_state_mh_culpability_or"]


def cps():
    rows = {r["group"]: r for r in csv.DictReader(open(
        ROOT / "infra/immigration-fiscal/crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv"))}
    return (float(rows["union"]["all_ages"]), float(rows["cps_all_civilian"]["all_ages"]),
            float(rows["union_hispanic"]["all_ages"]) / float(rows["cps_hispanic_civilian"]["all_ages"]))


N_GROUP, N_ALL, MEX_OF_HISP = cps()
P_SHARE = N_GROUP / N_ALL


def self_exposure():
    """Group-traffic-weighted group share of traffic across the congestion lane's urban areas."""
    num = den = 0.0
    for r in csv.DictReader(open(ROOT / "infra/immigration-fiscal/congestion_2026_09_23/derived/ua_exposure.csv")):
        try:
            phi = float(r["phi_commute_route"])
            w = float(r["acs_group_vehicle_minutes"])
        except (ValueError, KeyError):
            continue
        num += w * phi
        den += w
    return num / den


Q_METRO = self_exposure()


def cost_base():
    """2024 $bn by class: multi-vehicle fatal / nonfatal, single-vehicle, non-motorist."""
    out = {"mv_fatal": 0.0, "mv_nonfatal": 0.0, "sv": 0.0, "nm_fatal": 0.0, "nm_nonfatal": 0.0,
           "excluded_congestion": 0.0, "excluded_ems": 0.0, "gov_share_econ": 29546 / 339809}
    for k in SEV:
        econ_keep = ECON[k] - CONG[k] - EMS[k]
        comp = econ_keep + QALY[k]
        price = (econ_keep * CPI_2024 / CPI_2019 + QALY[k] * VSL_2024 / VSL_2019) / comp
        count = (KILLED[2023] / KILLED[2019] if k == "Fatal" else
                 PDO_CRASHES[2023] / PDO_CRASHES[2019] if k == "PDO" else INJURED[2023] / INJURED[2019])
        f = price * count / 1000.0
        keep_frac = comp / (ECON[k] + QALY[k])
        nm = (PED[k] + BIKE[k]) * keep_frac
        occ = comp - nm
        mv = MV_SHARE_FATAL if k == "Fatal" else MV_SHARE_PDO if k == "PDO" else MV_SHARE_INJ
        if k == "Fatal":
            out["mv_fatal"] += occ * mv * f
            out["nm_fatal"] += nm * f
        else:
            out["mv_nonfatal"] += occ * mv * f
            out["nm_nonfatal"] += nm * f
        out["sv"] += occ * (1 - mv) * f
        out["excluded_congestion"] += CONG[k] * CPI_2024 / CPI_2019 * count / 1000.0
        out["excluded_ems"] += EMS[k] * CPI_2024 / CPI_2019 * count / 1000.0
    out["total_kept"] = sum(out[c] for c in ("mv_fatal", "mv_nonfatal", "sv", "nm_fatal", "nm_nonfatal"))
    return out


BASE = cost_base()

# --- factor levels, ordered (low-E, central, high-E) [see RESULT.md for sources]
VMT_RATIO_OTHERS = {"low": 0.692, "central": 0.874, "high": 0.893}  # NHTS 2022 nat / 2017 SW / 2017 nat
FACTORS = {
    "vmt": ["low", "central", "high"],
    "r_c": [MH["hispanic_any_crude_or"], MH["hispanic_any_vs_non_hispanic"], MH["mexican_vs_non_hispanic"]],
    "q_mult": [1.3, 1.0, 0.0],  # 0.0 flags uniform national mixing (q = s)
    "x_nonfatal": [0.2, 0.6, 1.0],
    "x_fatal": [-0.3, 0.0, 1.0],
    "beta": [(0.4, 0.0), (0.8, 0.4), (1.2, 1.0)],  # (nonfatal, fatal) non-motorist elasticities
    "liab": [(0.10, 0.80), (0.15, 0.72), (0.25, 0.60)],  # (kappa, insured share of group drivers)
    "e_sv": [0.02, 0.04, 0.08],
}
INS_OTHER = 1 - 0.154  # IRC: 15.4% of drivers uninsured in 2023 [SOURCE]
F_DRIVER_PED = 0.5  # share of non-motorist crashes attributed to the driver [ASSUMPTION]


def evaluate(vmt, r_c, q_mult, x_nf, x_f, beta, liab, e_sv):
    r = VMT_RATIO_OTHERS[vmt]
    s = P_SHARE * r / (P_SHARE * r + 1 - P_SHARE)
    vmt_vs_avg = r / (P_SHARE * r + 1 - P_SHARE)
    q = s if q_mult == 0.0 else min(Q_METRO * q_mult, 0.95)
    h = HISP_PED * MEX_OF_HISP
    m = (1 + r_c) / 2
    f_g = r_c / (1 + r_c)
    kappa, ins_g = liab
    b_nf, b_f = beta
    mv = BASE["mv_fatal"] + BASE["mv_nonfatal"]
    liab_term = kappa * ((1 - f_g) * INS_OTHER - f_g * ins_g)
    e = {
        "mv_nonfatal": m * s * (1 - q) * BASE["mv_nonfatal"] * (x_nf + liab_term),
        "mv_fatal": m * s * (1 - q) * BASE["mv_fatal"] * (x_f + liab_term),
        "nonmotorist": m * s * (1 - q) / (1 - s) * (1 - h) * (b_nf * BASE["nm_nonfatal"] + b_f * BASE["nm_fatal"]),
        "single_vehicle": m * s * BASE["sv"] * e_sv,
    }
    e["total"] = sum(e.values())
    fault = (m * s * (1 - q) * mv * f_g * (1 - kappa * ins_g)
             + m * s * (1 - q) / (1 - s) * (1 - h) * (BASE["nm_nonfatal"] + BASE["nm_fatal"])
             * F_DRIVER_PED * (r_c / ((1 + r_c) / 2)) * (1 - kappa * ins_g)
             + e["single_vehicle"])
    R = vmt_vs_avg * m
    R_fault = vmt_vs_avg * r_c
    return {"s": s, "q": q, "m": m, "vmt_vs_avg": vmt_vs_avg, "R": R, **e,
            "normalized": e["total"] * (1 - 1 / R),
            "fault_total": fault, "fault_normalized": fault * (1 - 1 / R_fault)}


def main():
    keys = list(FACTORS)
    grid = []
    for combo in itertools.product(*[range(3) for _ in keys]):
        args = [FACTORS[k][i] for k, i in zip(keys, combo)]
        res = evaluate(*args)
        grid.append({**{k: i for k, i in zip(keys, combo)}, **res})
    central = evaluate(*[FACTORS[k][1] for k in keys])
    low_e = evaluate(*[FACTORS[k][0] for k in keys])
    high_e = evaluate(*[FACTORS[k][2] for k in keys])

    def span(col):
        vals = [g[col] for g in grid]
        return min(vals), central[col], max(vals)

    OUT.mkdir(exist_ok=True)
    with open(OUT / "grid.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(grid[0]), lineterminator="\n")
        w.writeheader()
        w.writerows({k: (round(v, 6) if isinstance(v, float) else v) for k, v in g.items()} for g in grid)

    # one-at-a-time swings from the central
    swings = {}
    for k in keys:
        lo = evaluate(*[FACTORS[j][0 if j == k else 1] for j in keys])["total"]
        hi = evaluate(*[FACTORS[j][2 if j == k else 1] for j in keys])["total"]
        swings[k] = [lo, hi]

    vmt_total = VMT_M[2023] * 1e6
    avg_ext_per_mile = {lvl: (FACTORS["x_nonfatal"][i] * BASE["mv_nonfatal"] + FACTORS["x_fatal"][i] * BASE["mv_fatal"]
                              + FACTORS["beta"][i][0] * BASE["nm_nonfatal"] + FACTORS["beta"][i][1] * BASE["nm_fatal"]
                              + FACTORS["e_sv"][i] * BASE["sv"]) * 1e9 / vmt_total * 100
                        for i, lvl in enumerate(["low", "central", "high"])}
    covid = {"vmt_log_change": __import__("math").log(VMT_M[2020] / VMT_M[2019])}
    for name, series in (("injury_crashes", INJ_CRASHES), ("pdo_crashes", PDO_CRASHES),
                         ("injured", INJURED), ("killed", KILLED)):
        covid[f"elasticity_{name}"] = __import__("math").log(series[2020] / series[2019]) / covid["vmt_log_change"]
    gov_part = central["total"] * BASE["gov_share_econ"] * 0.25  # economic ~25% of comprehensive [INFERENCE]

    model = {"base_2024_bn": BASE, "p_share": P_SHARE, "q_metro": Q_METRO, "mex_of_hisp": MEX_OF_HISP,
             "hisp_ped_share": HISP_PED, "mv_share": {"fatal": MV_SHARE_FATAL, "injury": MV_SHARE_INJ,
                                                     "pdo": MV_SHARE_PDO},
             "pax_outsider_share": PAX_OUT, "sv_passenger_share": SV_PAX,
             "central": central, "all_low": low_e, "all_high": high_e,
             "spans": {c: span(c) for c in ("total", "normalized", "fault_total", "fault_normalized",
                                             "mv_nonfatal", "mv_fatal", "nonmotorist", "single_vehicle")},
             "one_at_a_time_total_bn": swings,
             "average_vehicle_external_cents_per_mile_q0": avg_ext_per_mile,
             "covid_2019_2020": covid,
             "gov_paid_part_of_central_bn_approx": gov_part,
             "per_member_usd_central": central["total"] * 1e9 / N_GROUP}
    (OUT / "model.json").write_text(json.dumps(model, indent=1))

    def row(item, measure, col, evidence, dc, note):
        lo, c, hi = span(col)
        return {"item": item, "group": "mexican_origin", "measure": measure, "low_bn": f"{lo:.2f}",
                "central_bn": f"{c:.2f}", "high_bn": f"{hi:.2f}",
                "per_member_usd": f"{c * 1e9 / N_GROUP:.0f}", "evidence_level": evidence,
                "double_count_with": dc, "method_note": note}

    dc = ("congestion lane (crash delay removed: Blincoe congestion excluded); account public-safety "
          "lines (EMS excluded); group's own public medical and lost taxes (account)")
    rows = [
        row("road_crash_externality", "absolute", "total",
            "Blincoe comprehensive costs (measured + VSL); FARS culpability; volume elasticity x contested",
            dc, "but-for: outsider losses in crashes the group's traffic adds; x/beta = crash-volume elasticities"),
        row("road_crash_externality", "normalized", "normalized",
            "as absolute; plus NHTS Hispanic VMT ratio",
            dc, "absolute x (1 - 1/R), R = VMT per person vs average resident x involvement per mile"),
        row("road_crash_externality_fault_based", "absolute", "fault_total",
            "Blincoe + FARS culpability; attribution convention, not a counterfactual [FRAMING-SENSITIVE]",
            dc + "; alternative to road_crash_externality, never add both",
            "outsider losses in crashes group drivers cause, less their liability payments"),
        row("road_crash_externality_fault_based", "normalized", "fault_normalized",
            "as fault-based absolute", dc + "; alternative, never add both",
            "fault-based absolute x (1 - 1/R'), R' = VMT ratio x culpability odds ratio"),
        row("component_multivehicle_nonfatal", "absolute", "mv_nonfatal", "component of road_crash_externality",
            "component; do not add to total", "x_nonfatal 0.2/0.6/1.0 (2020: injury crashes 1.6, PDO 2.4 elasticity)"),
        row("component_multivehicle_fatal", "absolute", "mv_fatal", "component of road_crash_externality",
            "component; do not add to total", "x_fatal -0.3/0/1.0 (2020 deaths rose as VMT fell)"),
        row("component_nonmotorist", "absolute", "nonmotorist", "component of road_crash_externality",
            "component; do not add to total", "pedestrians and cyclists outside the group"),
        row("component_single_vehicle", "absolute", "single_vehicle", "component of road_crash_externality",
            "component; do not add to total", "outsider passengers, others' property, employers"),
    ]
    with open(OUT / "items.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(json.dumps({k: model[k] for k in ("base_2024_bn", "q_metro", "p_share", "mv_share", "spans",
                                             "one_at_a_time_total_bn", "average_vehicle_external_cents_per_mile_q0",
                                             "covid_2019_2020", "per_member_usd_central",
                                             "gov_paid_part_of_central_bn_approx")}, indent=1))
    print("central", json.dumps(central, indent=1))


if __name__ == "__main__":
    main()
