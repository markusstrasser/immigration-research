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

Revision 2026-09-28 (lead): the non-fatal parts take their own culpability odds ratios, measured in
California's crash records (ccrs_nonfatal_involvement_2026_09_28: CCRS 2022-24 quasi-induced exposure,
Hispanic against all non-Hispanic drivers within county x year, injury and PDO). evaluate_split() carries
them; fatal and single-vehicle parts keep FARS's r_c. The non-fatal multi-vehicle part takes the m
weighted over its injury and PDO cost rows, the non-fatal non-motorist part the injury m, and (b) and
the fault-based normalized figure apply 1 - 1/R per component. evaluate() is unchanged: it is the lane
before the revision, the positive control, and what other lanes import. The grid adds r_nf at three
levels: the CCRS lane's hit-and-run bounds (no unidentified fled driver Hispanic; every one Hispanic)
around its central.

Revision 2026-09-28, later (lead): the volume elasticities x take the levels graded from transferable evidence
(crash_volume_elasticity_2026_09_28: natural experiments, national before-after and panels, weighted toward the
congested metros where the group drives; central by the lane's rule, low and high its bootstrap p10 and p90). The
but-for also carries a composition term (evaluate_split(..., composition=True)): what the group's culpability
excess costs others where crashes do not scale pairwise. FACTORS keeps the first x levels for evaluate() and
importers; evaluate_split's default leaves the term out, so the CCRS positive control and importers are unchanged.
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


# --- non-fatal culpability, measured: California CCRS 2022-24 (ccrs_nonfatal_involvement_2026_09_28, 20755cb),
# (injury, PDO) odds ratios. Central: quasi-induced exposure within county x year against all non-Hispanic
# drivers; low and high: that lane's hit-and-run bounds. [DATA]
CCRS_REVISION = ROOT / "infra/immigration-fiscal/ccrs_nonfatal_involvement_2026_09_28/derived/crash_component_revision.csv"
CCRS_LEVELS = ("hit-and-run: no unidentified fled driver Hispanic, vs_all_non_hispanic",
               "QIE within county x year, vs_all_non_hispanic",
               "hit-and-run: all unidentified fled drivers Hispanic, vs_all_non_hispanic")


def ccrs_nonfatal_or():
    rows = {r["scenario"]: r for r in csv.DictReader(open(CCRS_REVISION))}
    return [(float(rows[k]["or_injury"]), float(rows[k]["or_pdo"])) for k in CCRS_LEVELS]


def pdo_share_of_mv_nonfatal():
    """The PDO row's share of the non-fatal multi-vehicle base: the weight of the PDO odds ratio in its m."""
    parts = {}
    for k in SEV[:-1]:
        econ_keep = ECON[k] - CONG[k] - EMS[k]
        comp = econ_keep + QALY[k]
        price = (econ_keep * CPI_2024 / CPI_2019 + QALY[k] * VSL_2024 / VSL_2019) / comp
        count = PDO_CRASHES[2023] / PDO_CRASHES[2019] if k == "PDO" else INJURED[2023] / INJURED[2019]
        occ = comp - (PED[k] + BIKE[k]) * comp / (ECON[k] + QALY[k])
        parts[k] = occ * (MV_SHARE_PDO if k == "PDO" else MV_SHARE_INJ) * price * count / 1000.0
    assert abs(sum(parts.values()) - BASE["mv_nonfatal"]) < 1e-6
    return parts["PDO"] / BASE["mv_nonfatal"]


W_PDO = pdo_share_of_mv_nonfatal()  # the CCRS levels are read in main(), so importers never need that lane


def evaluate_split(vmt, r_c, q_mult, x_nf, x_f, beta, liab, e_sv, r_nf, composition=False):
    """evaluate() with the non-fatal parts on their own odds ratios r_nf = (injury, PDO); fatal and
    single-vehicle parts keep r_c. r_nf = (r_c, r_c) reproduces evaluate().

    composition=True adds what the group's culpability excess costs others at x < 1 and beta < 1. The volume
    terms scale the group's whole involvement m by x, so at x = 0 a group whose drivers cause more crashes
    than others (r > 1) would add nothing. Removing it lowers others' involvement per mile by
    s (1 - q) M (r - 1) (1 - x) / 2 in multi-vehicle crashes and by F (r - 1) (1 - beta) of the non-motorist
    base in crashes with pedestrians and cyclists [DERIVATION: RESULT.md, x revision]. The term is specific to
    the group, so the normalized figure carries it whole."""
    base = evaluate(vmt, r_c, q_mult, x_nf, x_f, beta, liab, e_sv)
    s, q, v = base["s"], base["q"], base["vmt_vs_avg"]
    h = HISP_PED * MEX_OF_HISP
    kappa, ins_g = liab
    b_nf, b_f = beta
    or_inj, or_pdo = r_nf
    m_f, m_nm = (1 + r_c) / 2, (1 + or_inj) / 2
    m_mv = W_PDO * (1 + or_pdo) / 2 + (1 - W_PDO) * m_nm
    r_mv = 2 * m_mv - 1

    def liab_term(r):
        f = r / (1 + r)
        return kappa * ((1 - f) * INS_OTHER - f * ins_g)

    nm_scale = s * (1 - q) / (1 - s) * (1 - h)
    keep = 1 - kappa * ins_g
    comp = {"mv_nonfatal": m_mv * s * (1 - q) * BASE["mv_nonfatal"] * (x_nf + liab_term(r_mv)),
            "mv_fatal": m_f * s * (1 - q) * BASE["mv_fatal"] * (x_f + liab_term(r_c)),
            "nm_nonfatal": m_nm * nm_scale * b_nf * BASE["nm_nonfatal"],
            "nm_fatal": m_f * nm_scale * b_f * BASE["nm_fatal"],
            "single_vehicle": m_f * s * BASE["sv"] * e_sv}
    extra = dict.fromkeys(comp, 0.0)
    if composition:
        extra["mv_nonfatal"] = s * (1 - q) * BASE["mv_nonfatal"] * (r_mv - 1) * (1 - x_nf) / 2
        extra["mv_fatal"] = s * (1 - q) * BASE["mv_fatal"] * (r_c - 1) * (1 - x_f) / 2
        extra["nm_nonfatal"] = nm_scale * BASE["nm_nonfatal"] * F_DRIVER_PED * (or_inj - 1) * (1 - b_nf)
        extra["nm_fatal"] = nm_scale * BASE["nm_fatal"] * F_DRIVER_PED * (r_c - 1) * (1 - b_f)
    fault = {"mv_nonfatal": m_mv * s * (1 - q) * BASE["mv_nonfatal"] * r_mv / (1 + r_mv) * keep,
             "mv_fatal": m_f * s * (1 - q) * BASE["mv_fatal"] * r_c / (1 + r_c) * keep,
             "nm_nonfatal": nm_scale * BASE["nm_nonfatal"] * F_DRIVER_PED * or_inj * keep,
             "nm_fatal": nm_scale * BASE["nm_fatal"] * F_DRIVER_PED * r_c * keep,
             "single_vehicle": comp["single_vehicle"]}
    m_of = dict(mv_nonfatal=m_mv, mv_fatal=m_f, nm_nonfatal=m_nm, nm_fatal=m_f, single_vehicle=m_f)
    r_of = dict(mv_nonfatal=r_mv, mv_fatal=r_c, nm_nonfatal=or_inj, nm_fatal=r_c, single_vehicle=r_c)
    return {"s": s, "q": q, "m_fatal": m_f, "m_mv_nonfatal": m_mv, "m_nm_nonfatal": m_nm, "vmt_vs_avg": v,
            "mv_nonfatal": comp["mv_nonfatal"] + extra["mv_nonfatal"], "mv_fatal": comp["mv_fatal"] + extra["mv_fatal"],
            "nonmotorist": comp["nm_nonfatal"] + comp["nm_fatal"] + extra["nm_nonfatal"] + extra["nm_fatal"],
            "single_vehicle": comp["single_vehicle"], "composition": sum(extra.values()),
            "total": sum(comp.values()) + sum(extra.values()),
            "normalized": sum(e * (1 - 1 / (v * m_of[k])) for k, e in comp.items()) + sum(extra.values()),
            "fault_total": sum(fault.values()),
            "fault_normalized": sum(e * (1 - 1 / (v * r_of[k])) for k, e in fault.items())}


# --- traffic-volume elasticities, graded from transferable evidence (crash_volume_elasticity_2026_09_28): the
# lane's rule gives the central; its bootstrap p10 and p90 of that central are the low and high levels. FACTORS
# keeps the lane's first levels (0.2/0.6/1.0, -0.3/0/1.0) for evaluate(), the positive control, and importers.
X_BAND = ROOT / "infra/immigration-fiscal/crash_volume_elasticity_2026_09_28/derived/x_band.json"


def x_levels_evidence():
    d = json.loads(X_BAND.read_text())
    boot, band = d["bootstrap_central_p10_p50_p90"], d["band"]
    return {k: [boot[k][0], band[k][1], boot[k][2]] for k in ("x_nonfatal", "x_fatal")}


# Named scenarios (RESULT.md): overrides of the central inputs.
SCENARIOS = {
    "central": {},
    "lane_first_x_levels": {"x_nonfatal": FACTORS["x_nonfatal"][1], "x_fatal": FACTORS["x_fatal"][1]},
    "parry_style_x0_beta_low": {"x_nonfatal": 0.0, "x_fatal": 0.0, "beta": (0.4, 0.0)},
    "covid_face_value": {"x_nonfatal": 0.59, "x_fatal": -1.61, "beta": (0.8, 0.0)},
    "pairwise_all_1": {"x_nonfatal": 1.0, "x_fatal": 1.0, "beta": (1.0, 1.0)},
    "uniform_mixing": {"q_mult": 0.0},
    "mexican_coded_culpability": {"r_c": FACTORS["r_c"][2]},
}


def main():
    keys = list(FACTORS)
    nf_or = ccrs_nonfatal_or()
    x_ev = x_levels_evidence()
    # the grid's nine factors: x at the graded evidence levels; r_nf enters evaluate_split by keyword
    levels = {**FACTORS, **x_ev, "r_nf": nf_or}

    def run(idx):
        """idx: level index (0 low, 1 central, 2 high) per factor in `levels`."""
        return evaluate_split(*[levels[k][idx[k]] for k in keys], r_nf=nf_or[idx["r_nf"]], composition=True)

    grid = []
    for combo in itertools.product(*[range(3) for _ in levels]):
        idx = dict(zip(levels, combo))
        grid.append({**idx, **run(idx)})
    central = run({k: 1 for k in levels})
    low_e = run({k: 0 for k in levels})
    high_e = run({k: 2 for k in levels})
    before = evaluate(*[FACTORS[k][1] for k in keys])  # the lane before the CCRS revision
    control = evaluate_split(*[FACTORS[k][1] for k in keys], r_nf=(FACTORS["r_c"][1],) * 2)
    for c in ("total", "normalized", "fault_total", "fault_normalized", "mv_nonfatal", "nonmotorist"):
        assert abs(control[c] - before[c]) < 1e-9, (c, control[c], before[c])
    # the lane after the CCRS revision and before the x revision: first x levels, no composition term
    before_x = evaluate_split(*[FACTORS[k][1] for k in keys], r_nf=nf_or[1])
    # the composition term vanishes when the group's culpability equals others' at every severity
    ev_c = {k: levels[k][1] for k in keys}
    for comp_on in (False, True):
        even = evaluate_split(*[1.0 if k == "r_c" else ev_c[k] for k in keys], r_nf=(1.0, 1.0), composition=comp_on)
        assert abs(even["composition"]) < 1e-12, even["composition"]
    assert abs(evaluate_split(*[ev_c[k] for k in keys], r_nf=nf_or[1])["total"]
               + central["composition"] - central["total"]) < 1e-9
    assert central["fault_total"] == before_x["fault_total"]  # the fault-based row uses neither x nor the term

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
    for k in levels:
        lo = run({j: 0 if j == k else 1 for j in levels})["total"]
        hi = run({j: 2 if j == k else 1 for j in levels})["total"]
        swings[k] = [lo, hi]
    scenarios = {}
    for name, over in SCENARIOS.items():
        a = {k: over.get(k, levels[k][1]) for k in keys}
        scenarios[name] = evaluate_split(*[a[k] for k in keys], r_nf=nf_or[1], composition=True)
    (OUT / "scenarios.json").write_text(json.dumps(scenarios, indent=1))

    vmt_total = VMT_M[2023] * 1e6
    avg_ext_per_mile = {lvl: (levels["x_nonfatal"][i] * BASE["mv_nonfatal"] + levels["x_fatal"][i] * BASE["mv_fatal"]
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
             "nonfatal_or_ccrs": {"levels_injury_pdo": nf_or, "scenarios": CCRS_LEVELS, "w_pdo": W_PDO,
                                  "source": str(CCRS_REVISION.relative_to(ROOT))},
             "central_before_ccrs_revision": before,
             "x_levels": {"evidence": x_ev, "first": {k: FACTORS[k] for k in ("x_nonfatal", "x_fatal")},
                          "source": str(X_BAND.relative_to(ROOT))},
             "central_before_x_revision": before_x,
             "spans": {c: span(c) for c in ("total", "normalized", "fault_total", "fault_normalized",
                                             "mv_nonfatal", "mv_fatal", "nonmotorist", "single_vehicle",
                                             "composition")},
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
            "Blincoe comprehensive costs (measured + VSL); FARS fatal and CCRS non-fatal culpability; volume "
            "elasticity x graded from transferable evidence, its sign unsettled in dense traffic",
            dc, "but-for: outsider losses the group's traffic adds, with and without it; x/beta = crash-volume "
                "elasticities; plus the composition term (culpability excess at x < 1)"),
        row("road_crash_externality", "normalized", "normalized",
            "as absolute; plus NHTS Hispanic VMT ratio",
            dc, "volume terms x (1 - 1/R) per component, R = VMT per person vs average resident x involvement per "
                "mile; the composition term whole"),
        row("road_crash_externality_fault_based", "absolute", "fault_total",
            "Blincoe + FARS fatal and CCRS non-fatal culpability; attribution convention, not a counterfactual "
            "[FRAMING-SENSITIVE]",
            dc + "; alternative to road_crash_externality, never add both",
            "outsider losses in crashes group drivers cause, less their liability payments"),
        row("road_crash_externality_fault_based", "normalized", "fault_normalized",
            "as fault-based absolute", dc + "; alternative, never add both",
            "fault-based absolute x (1 - 1/R') per component, R' = VMT ratio x culpability odds ratio"),
        row("component_multivehicle_nonfatal", "absolute", "mv_nonfatal", "component of road_crash_externality",
            "component; do not add to total",
            "x_nonfatal {:.2f}/{:.2f}/{:.2f} (graded evidence; first levels 0.2/0.6/1.0)".format(*x_ev["x_nonfatal"])),
        row("component_multivehicle_fatal", "absolute", "mv_fatal", "component of road_crash_externality",
            "component; do not add to total",
            "x_fatal {:.2f}/{:.2f}/{:.2f} (graded evidence; first levels -0.3/0/1.0)".format(*x_ev["x_fatal"])),
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
