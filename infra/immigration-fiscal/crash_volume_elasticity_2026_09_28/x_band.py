"""Evidence band for x = eps - 1 (per-mile crash-rate elasticity to traffic on a fixed network), by
severity, and the crash lane's but-for re-run with it.

Rule (fixed before looking at the result):
1. Each estimate gets a design weight: natural experiment 3 (2 when x is derived by combining two
   specifications or the estimate is very imprecise), national 2019->2020 before-after 1 (a volume
   shock confounded by behaviour), panel 1, handbook assumption 0.5, cross-section 0 (reported only).
2. Setting weight follows the group's exposure (congestion lane ua_exposure.csv): dense congested
   metro evidence carries the group's share of commute vehicle-minutes in urban areas with TTI >= 1.30
   plus half of those at 1.20-1.30; mixed/national/sparse evidence carries the rest. Within a
   (severity, setting) bin, weights are proportional to design weight.
3. Per severity class: weighted median (central) and weighted quartiles (band).
4. x_nonfatal = cost-weighted mean of the PDO, minor-injury (MAIS1-2) and serious-injury (MAIS3-5)
   class values, with the multi-vehicle non-fatal cost shares of the crash lane's own Blincoe base.
   x_fatal = the fatal class, with serious-or-fatal estimates at half weight.
Outputs: derived/evidence.csv, derived/x_band.json, derived/butfor_recomputed.json
"""
import csv
import importlib.util
import itertools
import json
import math
from pathlib import Path

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]
OUT = LANE / "derived"
CRASH = ROOT / "infra/immigration-fiscal/road_crash_externality_2026_09_28/crash_model.py"
UA = ROOT / "infra/immigration-fiscal/congestion_2026_09_23/derived/ua_exposure.csv"

spec = importlib.util.spec_from_file_location("crash_model_lane", CRASH)
cm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cm)

L = math.log
DESIGN_W = {"natural": 3.0, "natural-": 2.0, "national2020": 1.0, "panel": 1.0, "assumption": 0.5, "cross": 0.0}


def x_from(count_ratio, volume_ratio):
    return L(count_ratio) / L(volume_ratio) - 1


# --- derived inputs [CALCULATION]
us_vmt = cm.VMT_M[2020] / cm.VMT_M[2019]
ghn_miles = 0.65 / 0.78  # count -35%, per-mile rate -22% (Green, Heywood & Navarro WP, pp. with Tables 1, 4)
nyc_vmt = 1 - 0.071  # MTA: CRZ VMT -7.1%
gb_traffic = 1 - 0.21  # DfT RRCGB 2020 Table 1
bhr_cars = (1.025, 1.043)  # Bauernschuster et al.: cars on roads +2.5 to 4.3% (am peak)


def bhr(effect, base):
    r = 1 + effect / base
    return x_from(r, bhr_cars[1]), x_from(r, bhr_cars[0])  # (low x at +4.3% cars, high x at +2.5%)


def us_states():
    rows = list(csv.DictReader(open(OUT / "state_2020.csv")))
    rows = [r for r in rows if r["urban_share_2019"]]
    rows.sort(key=lambda r: float(r["urban_share_2019"]))
    n = len(rows)
    dense, rest = rows[2 * n // 3:], rows[: 2 * n // 3]

    def el(g):
        v = sum(float(r["vmt2020_m"]) for r in g) / sum(float(r["vmt2019_m"]) for r in g)
        d = sum(float(r["deaths2020"]) for r in g) / sum(float(r["deaths2019"]) for r in g)
        return x_from(d, v)
    return el(dense), el(rest)


US_DENSE_FATAL_X, US_REST_FATAL_X = us_states()
bhr_crash, bhr_slight, bhr_serious = bhr(0.607, 4.280), bhr(0.790, 3.940), bhr(-0.013, 0.354)

# (study, setting description, setting bin, design, severity class, x_low, x_high, source tag)
E = [
    # --- PDO / non-injury crashes
    ("NYC Congestion Relief Zone 2025 (Morrison et al. AJE 2026; MTA VMT)", "Manhattan CBD cordon", "dense",
     "natural", "pdo", x_from(0.89, nyc_vmt), None, "IRR 0.89 non-injury crashes; CRZ VMT -7.1%"),
    ("Bauernschuster, Hener & Rainer 2017", "5 largest German cities, am peak, transit strikes", "dense",
     "natural", "pdo", *bhr_crash, "police-recorded crashes +14.2% on cars +2.5-4.3%; mostly PDO"),
    ("Edlin & Karaca-Mandic 2006 (California)", "densest US state, 1987-95", "dense",
     "panel", "pdo", 2.3, 4.4, "insured costs +3.3-5.4% per 1% driving; liability + collision"),
    ("Edlin & Karaca-Mandic 2006 (low-density states)", "e.g. South Dakota", "mixed",
     "panel", "pdo", 0.0, 0.0, "externality 'small ... statistically insignificant'; x ~ 0 [INFERENCE]"),
    ("US 2019->2020 PDO crashes (TSF 2023 Tables 1-2)", "US national", "mixed",
     "national2020", "pdo", x_from(cm.PDO_CRASHES[2020] / cm.PDO_CRASHES[2019], us_vmt), None,
     "PDO crashes -24.6% on VMT -11.0%"),
    # --- minor injury (slight / all-injury crashes)
    ("Tang & van Ommeren 2022", "Central London congestion charge, IV", "dense",
     "natural", "minor", -0.19, None, "slight-injury rate elasticity -0.19 (accidents -0.36)"),
    ("Green, Heywood & Navarro 2016", "Central London congestion charge, DiD vs 20 cities", "dense",
     "natural-", "minor", x_from(0.65, ghn_miles), None,
     "injury accidents -35%, per-mile rate -22%; x combines two specifications"),
    ("NYC Congestion Relief Zone 2025", "Manhattan CBD cordon", "dense",
     "natural", "minor", x_from(0.96, nyc_vmt), None, "IRR 0.96 (0.88-1.06) injury-or-fatal crashes"),
    ("Bauernschuster, Hener & Rainer 2017", "German cities am peak", "dense",
     "natural", "minor", *bhr_slight, "slightly injured +20.1% on cars +2.5-4.3%"),
    ("CE Delft 2019 Handbook (urban roads)", "EU urban roads", "dense",
     "assumption", "minor", 0.0, None, "recommended risk elasticity 0, urban"),
    ("US 2019->2020 injury crashes (TSF 2023)", "US national", "mixed",
     "national2020", "minor", x_from(cm.INJ_CRASHES[2020] / cm.INJ_CRASHES[2019], us_vmt), None,
     "injury crashes -16.9% on VMT -11.0%"),
    ("GB 2020 slight casualties (DfT RRCGB 2020)", "Great Britain national", "mixed",
     "national2020", "minor", x_from(0.75, gb_traffic), None, "slight -25% on traffic -21%"),
    ("Fridstrom (TOI 402/1998), fixed network", "Norway counties, monthly 1974-94", "mixed",
     "panel", "minor", 0.50 - 1, None, "injury accidents: 0.911 - 0.414 = 0.50 on a fixed network"),
    ("CE Delft 2019 Handbook (motorways, other)", "EU non-urban roads", "mixed",
     "assumption", "minor", -0.25, None, "recommended risk elasticity -0.25"),
    # --- serious injury (serious, or serious-or-fatal)
    ("Tang & van Ommeren 2022", "Central London congestion charge, IV", "dense",
     "natural", "serious", -1.65, None, "serious injuries/fatalities +6.5% on flow -9.4%"),
    ("Green, Heywood & Navarro 2016", "Central London congestion charge", "dense",
     "natural-", "serious", x_from(0.75, ghn_miles), None, "serious+fatal accidents -25%"),
    ("Bauernschuster, Hener & Rainer 2017", "German cities am peak", "dense",
     "natural-", "serious", *bhr_serious, "seriously/fatally injured -0.013 (s.e. 0.055) on 0.354: imprecise"),
    ("NYC Congestion Relief Zone 2025", "Manhattan CBD cordon", "dense",
     "natural", "serious", x_from(0.94, nyc_vmt), None,
     "IRR 0.94 (0.71-1.24) crashes with serious injury or fatality (AJE Table 1; Jan-Jun 2025)"),
    ("CE Delft 2019 Handbook (urban roads)", "EU urban roads", "dense", "assumption", "serious", 0.0, None,
     "risk elasticity 0, urban"),
    ("GB 2020 serious casualties (DfT RRCGB 2020)", "Great Britain national", "mixed",
     "national2020", "serious", x_from(0.78, gb_traffic), None, "serious -22% on traffic -21%"),
    ("CE Delft 2019 Handbook (motorways, other)", "EU non-urban roads", "mixed", "assumption", "serious",
     -0.25, None, "risk elasticity -0.25"),
    # --- fatal
    ("Green, Heywood & Navarro 2016", "Central London congestion charge", "dense",
     "natural-", "fatal", x_from(0.65, ghn_miles), None, "fatalities -35% (4.3 a year)"),
    ("US 2019->2020, most urban tercile of states (FHWA VM-2, FI-20)", "17 most urbanised states", "dense",
     "national2020", "fatal", US_DENSE_FATAL_X, None, "deaths +7.2% on VMT -11.8%"),
    ("CE Delft 2019 Handbook (urban roads)", "EU urban roads", "dense", "assumption", "fatal", 0.0, None,
     "risk elasticity 0, urban"),
    ("US 2019->2020, other 33 states (FHWA)", "less urbanised states", "mixed",
     "national2020", "fatal", US_REST_FATAL_X, None, "deaths about +7% on VMT about -10%"),
    ("GB 2020 fatalities (DfT RRCGB 2020)", "Great Britain national", "mixed",
     "national2020", "fatal", x_from(0.83, gb_traffic), None, "deaths -17% on traffic -21%"),
    ("ITF/IRTAD 2021, eleven countries with vkm", "AU CA DK FI FR GB DE JP NL SI SE", "mixed",
     "national2020", "fatal", 0.0, 0.2, "vkm -12.2%, deaths per vkm 'slightly decreased' [INFERENCE on size]"),
    ("Fridstrom (TOI 402/1998), constant density", "Norway counties", "mixed",
     "panel", "fatal", 0.761 - 1, None, "fatalities 0.761 at constant density; fixed network lower"),
    ("CE Delft 2019 Handbook (motorways, other)", "EU non-urban roads", "mixed", "assumption", "fatal",
     -0.25, None, "risk elasticity -0.25"),
]
# serious-or-fatal estimates also inform the fatal class at half weight
HALF_TO_FATAL = {("Tang & van Ommeren 2022", "serious"), ("Bauernschuster, Hener & Rainer 2017", "serious"),
                 ("NYC Congestion Relief Zone 2025", "serious")}
# cross-sections, reported and never weighted [SOURCE: HSM Table 12-6 via NCHRP 17-54 excerpt; TOI example]
CROSS = [
    ("HSM urban/suburban arterials, single-vehicle SPF (Table 12-6)", "US arterial segments", "cross", "cross", "sv",
     0.47 - 1, 0.81 - 1, "AADT exponents 0.47-0.81 (total crashes); roads are built for their traffic"),
    ("HSM rural divided segment SPF (Table 11-5 example)", "US rural multilane", "cross", "cross", "all",
     1.049 - 1, None, "b = 1.049"),
]


def exposure_shares():
    num = {"hi": 0.0, "mid": 0.0, "lo": 0.0}
    for r in csv.DictReader(open(UA)):
        if r.get("in_scope") != "True":
            continue
        try:
            t, w = float(r["tti"]), float(r["acs_group_vehicle_minutes"])
        except ValueError:
            continue
        num["hi" if t >= 1.30 else "mid" if t >= 1.20 else "lo"] += w
    tot = sum(num.values())
    dense = (num["hi"] + 0.5 * num["mid"]) / tot
    return {"dense": dense, "mixed": 1 - dense, "tti_ge_1.30": num["hi"] / tot, "tti_1.20_1.30": num["mid"] / tot}


def wquant(pairs, p):
    pairs = sorted(pairs)
    tot = sum(w for _, w in pairs)
    acc = 0.0
    for v, w in pairs:
        acc += w
        if acc >= p * tot - 1e-12:
            return v
    return pairs[-1][0]


def class_stats(rows, cls, shares, drop=None):
    pairs = []
    for bin_ in ("dense", "mixed"):
        members = []
        for r in rows:
            if drop and r["study"].startswith(drop):
                continue
            w = DESIGN_W[r["design"]]
            if r["class"] == cls and r["bin"] == bin_:
                members.append((r["x_mid"], w))
            elif cls == "fatal" and r["class"] == "serious" and r["bin"] == bin_ and \
                    (r["study"], "serious") in HALF_TO_FATAL:
                members.append((r["x_mid"], 0.5 * w))
        members = [m for m in members if m[1] > 0]
        tw = sum(w for _, w in members)
        if tw:
            pairs += [(v, shares[bin_] * w / tw) for v, w in members]
    return {"q25": wquant(pairs, 0.25), "median": wquant(pairs, 0.5), "q75": wquant(pairs, 0.75),
            "min": min(v for v, _ in pairs), "max": max(v for v, _ in pairs), "n": len(pairs)}


def nonfatal_cost_shares():
    """Multi-vehicle non-fatal 2024 cost by class, same arithmetic as crash_model.cost_base()."""
    cls = {"PDO": "pdo", "MAIS0": "pdo", "MAIS1": "minor", "MAIS2": "minor", "MAIS3": "serious",
           "MAIS4": "serious", "MAIS5": "serious"}
    out = {"pdo": 0.0, "minor": 0.0, "serious": 0.0}
    for k, c in cls.items():
        econ_keep = cm.ECON[k] - cm.CONG[k] - cm.EMS[k]
        comp = econ_keep + cm.QALY[k]
        price = (econ_keep * cm.CPI_2024 / cm.CPI_2019 + cm.QALY[k] * cm.VSL_2024 / cm.VSL_2019) / comp
        count = cm.PDO_CRASHES[2023] / cm.PDO_CRASHES[2019] if k == "PDO" else cm.INJURED[2023] / cm.INJURED[2019]
        nm = (cm.PED[k] + cm.BIKE[k]) * comp / (cm.ECON[k] + cm.QALY[k])
        mv = cm.MV_SHARE_PDO if k == "PDO" else cm.MV_SHARE_INJ
        out[c] += (comp - nm) * mv * price * count / 1000.0
    tot = sum(out.values())
    assert abs(tot - cm.BASE["mv_nonfatal"]) < 1e-6, (tot, cm.BASE["mv_nonfatal"])
    return {k: v / tot for k, v in out.items()}


def band(rows, shares, cost, drop=None):
    st = {c: class_stats(rows, c, shares, drop) for c in ("pdo", "minor", "serious", "fatal")}
    nf = {q: sum(cost[c] * st[c][q] for c in cost) for q in ("q25", "median", "q75")}
    return st, {"x_nonfatal": (nf["q25"], nf["median"], nf["q75"]),
                "x_fatal": (st["fatal"]["q25"], st["fatal"]["median"], st["fatal"]["q75"])}


def bootstrap(rows, shares, cost, draws=2000, seed=20260928):
    """Uncertainty of the central: resample estimates within each (class, bin), recompute the rule."""
    import random
    rng = random.Random(seed)
    groups = {}
    for r in rows:
        if DESIGN_W.get(r["design"], 0) > 0:
            groups.setdefault((r["class"], r["bin"]), []).append(r)
    nf, f = [], []
    for _ in range(draws):
        sample = [rng.choice(g) for g in groups.values() for _ in g]
        b = band(sample, shares, cost)[1]
        nf.append(b["x_nonfatal"][1])
        f.append(b["x_fatal"][1])
    q = lambda v, p: sorted(v)[int(p * (len(v) - 1))]
    return {"x_nonfatal": (q(nf, 0.10), q(nf, 0.50), q(nf, 0.90)), "x_fatal": (q(f, 0.10), q(f, 0.50), q(f, 0.90))}


def rerun(xnf, xf):
    keys = list(cm.FACTORS)
    lv = {**cm.FACTORS, "x_nonfatal": list(xnf), "x_fatal": list(xf)}
    res = {}
    for name, fn in (("evaluate", None), ("evaluate_split", "split")):
        if fn and not hasattr(cm, "evaluate_split"):
            continue
        nf_or = cm.ccrs_nonfatal_or() if fn else None
        levels = {**lv, "r_nf": nf_or} if fn else lv

        def run(idx):
            args = [lv[k][idx[k]] for k in keys]
            return cm.evaluate_split(*args, r_nf=nf_or[idx["r_nf"]]) if fn else cm.evaluate(*args)
        grid = [run(dict(zip(levels, c))) for c in itertools.product(*[range(3) for _ in levels])]
        cen = run({k: 1 for k in levels})
        oneway = {f"xnf={a:.2f},xf={b:.2f}": run({**{k: 1 for k in levels},
                                                  "x_nonfatal": i, "x_fatal": j})["total"]
                  for i, a in enumerate(xnf) for j, b in enumerate(xf)}
        res[name] = {"central_total": cen["total"], "grid_total": [min(g["total"] for g in grid),
                                                                   max(g["total"] for g in grid)],
                     "central_fault": cen["fault_total"], "grid_fault": [min(g["fault_total"] for g in grid),
                                                                         max(g["fault_total"] for g in grid)],
                     "central_normalized": cen["normalized"],
                     "x_table_others_central": oneway, "n_grid": len(grid)}
    return res


def central_butfor(xnf, xf):
    """But-for total ($bn) with only the two x values changed, other inputs at the lane's central."""
    a = [cm.FACTORS[k][1] for k in cm.FACTORS]
    a[list(cm.FACTORS).index("x_nonfatal")], a[list(cm.FACTORS).index("x_fatal")] = xnf, xf
    out = {"evaluate": cm.evaluate(*a)["total"]}
    if hasattr(cm, "evaluate_split"):
        out["evaluate_split"] = cm.evaluate_split(*a, r_nf=cm.ccrs_nonfatal_or()[1])["total"]
    return out


def main():
    rows = []
    for study, setting, bin_, design, cls, xlo, xhi, note in E + CROSS:
        xhi = xlo if xhi is None else xhi
        lo, hi = min(xlo, xhi), max(xlo, xhi)
        rows.append({"study": study, "setting": setting, "bin": bin_, "design": design, "class": cls,
                     "eps_low": round(lo + 1, 3), "eps_high": round(hi + 1, 3), "x_low": round(lo, 3),
                     "x_high": round(hi, 3), "x_mid": (lo + hi) / 2, "design_weight": DESIGN_W.get(design, 0.0),
                     "note": note})
    shares = exposure_shares()
    cost = nonfatal_cost_shares()
    stats, xb = band(rows, shares, cost)
    sens = {"dense_only": band(rows, {"dense": 1.0, "mixed": 0.0}, cost)[1],
            "mixed_only": band(rows, {"dense": 0.0, "mixed": 1.0}, cost)[1],
            "uniform_exposure_0.5": band(rows, {"dense": 0.5, "mixed": 0.5}, cost)[1]}
    boot = bootstrap(rows, shares, cost)
    saved = DESIGN_W["assumption"]
    DESIGN_W["assumption"] = 0.0
    sens["assumptions_weight_0"] = band(rows, shares, cost)[1]
    DESIGN_W["assumption"] = saved
    loo = {}
    for s in sorted({r["study"].split(" (")[0].split(",")[0] for r in rows if r["design"] != "cross"}):
        loo[s] = band(rows, shares, cost, drop=s)[1]
    OUT.mkdir(exist_ok=True)
    with open(OUT / "evidence.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[k for k in rows[0] if k != "x_mid"], lineterminator="\n")
        w.writeheader()
        w.writerows({k: v for k, v in r.items() if k != "x_mid"} for r in rows)
    out = {"exposure_shares": shares, "nonfatal_cost_shares": cost, "class_stats": stats, "band": xb,
           "sensitivity": sens, "bootstrap_central_p10_p50_p90": boot, "leave_one_study_out": loo,
           "us_states_fatal_x": {"dense_tercile": US_DENSE_FATAL_X, "other_two_terciles": US_REST_FATAL_X},
           "butfor_at_sensitivity_centrals": {k: central_butfor(v["x_nonfatal"][1], v["x_fatal"][1])
                                              for k, v in {**sens, **{f"drop {s}": b for s, b in loo.items()}}.items()},
           "butfor_slope_per_0.1": {
               "x_nonfatal": {k: v - central_butfor(xb["x_nonfatal"][1], xb["x_fatal"][1])[k] for k, v in
                              central_butfor(xb["x_nonfatal"][1] + 0.1, xb["x_fatal"][1]).items()},
               "x_fatal": {k: v - central_butfor(xb["x_nonfatal"][1], xb["x_fatal"][1])[k] for k, v in
                           central_butfor(xb["x_nonfatal"][1], xb["x_fatal"][1] + 0.1).items()}}}
    (OUT / "x_band.json").write_text(json.dumps(out, indent=1))
    rr = {"setting_iqr_band": rerun(xb["x_nonfatal"], xb["x_fatal"]),
          "bootstrap_band": rerun((boot["x_nonfatal"][0], xb["x_nonfatal"][1], boot["x_nonfatal"][2]),
                                  (boot["x_fatal"][0], xb["x_fatal"][1], boot["x_fatal"][2])),
          "lane_levels": rerun(tuple(cm.FACTORS["x_nonfatal"]), tuple(cm.FACTORS["x_fatal"]))}
    (OUT / "butfor_recomputed.json").write_text(json.dumps(rr, indent=1))
    print("bootstrap p10/p50/p90:", json.dumps(boot))
    print(json.dumps({"exposure_shares": shares, "cost": cost, "band": xb,
                      "class_stats": {c: {k: round(v, 3) for k, v in s.items()} for c, s in stats.items()},
                      "sensitivity": sens}, indent=1))
    print("LOO x_nonfatal central / x_fatal central:")
    for s, b in loo.items():
        print(f"  drop {s}: {b['x_nonfatal'][1]:+.3f} / {b['x_fatal'][1]:+.3f}")
    for k, v in rr.items():
        for fn, d in v.items():
            print(k, fn, {kk: (round(vv, 2) if isinstance(vv, float) else
                               [round(z, 2) for z in vv] if isinstance(vv, list) else vv)
                          for kk, vv in d.items() if kk != "x_table_others_central"})
            print("   ", {kk: round(vv, 1) for kk, vv in d["x_table_others_central"].items()})


if __name__ == "__main__":
    main()
