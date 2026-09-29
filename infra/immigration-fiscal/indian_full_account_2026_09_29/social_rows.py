"""The fiscal-plus-social rows for the Indian-origin group, the India-born, the Mexican-origin union and third-plus NH
whites, at own ages and at third-plus white ages, on one footing, and the combined table. Not the engine.

The union's social rows are the pairing's, on the 39.71M the account prices with the NHTS 5+ basis
(population_basis_2026_09_29/derived/restated_pairing.csv, sections row and row_5plus). Every other group's row is
the union's per-member row times the ratio of the item's driver, measured for both groups by the same code, unless the
item is recomputed with its lane's own function (PM2.5, scale spillovers) or formula (security, school disruption,
trade). Rules per item (DEGRADED where the Indian-specific input does not exist):
  victims, property crime, fear   offending per member: ACS 2023 institutionalized 18-64 per member over the union
                                  proxy's (acs_custody.py) x the NCVS age factor at white ages [DEGRADED proxy]; whites:
                                  the white lane's measured like-for-like NCVS ratio, non-white over non-Hispanic
                                  victims, 11.4964 / 23.4535 (victim_cost_white_summary.csv, the union's arms.csv)
  private security                the lane's formula: $74.438bn crime-driven spending x population share x (relative
                                  offending - 1); relative offending as above (whites: the white lane's custody key)
  school disruption               the lane's formula's two group terms: the CRDC suspension gap and pupils per member;
                                  Indian: Asian pupils, 6% of enrollment and about 1% of suspensions (each printed
                                  '<1%'; range 0.4-1.9%) [DEGRADED: Asian for Indian]; whites 45% / 32%
  unreimbursed care               uninsured person-years per member (NOCOV_CYR), the lane's own driver
  housing net                     renters' consumption per member [DEGRADED: the housing lane is not re-run]
  congestion                      per member as the union's: the lane's central is a population-share city-size
                                  elasticity [DEGRADED: metro mix not re-run]; the driver-miles ratio beside
  PM2.5                           air_pollution_2026_09_28 pm_grid on the group's count and the row-4 frame, caused
                                  exposure r scaled by consumption per member; own-group share iota assumed (Indian
                                  0.15 / 0.10 / 0.05; a white slice 0.15 / 0.12 / 0.10) [ASSUMPTION]; gate: the union
                                  reproduces the priced lane's 68.092104
  crashes                         driver miles share (NHTS 5+ rates by band, the re-key's rule 4 terms) [DEGRADED:
                                  equal crash cost per mile]
  scale net                       scale_spillovers' central joint formula on the CPS, nationally (rekey_indian.py
                                  drivers()), each part carried to the lane's CZ level by the union's CZ / national
                                  ratio (the parts rescaled by 13.93 / 13.72 to the joint fit's central) [DEGRADED: national transfer]
  restaurants, consumer scale     consumption per member
  volunteering                    persons 16+ per member x the formal volunteering rate over the Hispanic 16.9%: no
                                  Asian rate was found, so the all-resident 28.3% (CEV 2023) is the central for Indians
                                  and whites, the Hispanic rate the low [UNVERIFIED]
  trade, visits, FDI              (a subgroup takes its share of the India-born) trade: the union's central x US-India over US-Mexico non-travel trade (Census c5330 goods
                                  2024: $41.58bn exports, $87.28bn imports; USTR services 2024: $41.8bn exports, $43.1bn
                                  imports, of which 75% non-travel central, 50-100%) [ASSUMPTION on travel];
                                  visits: x India-born / Mexico-born persons; FDI: x the BEA USDIA position in India
                                  ($63.64bn, holding companies not netted) over Mexico's net ($140.61bn); whites 0
Ends: low and high follow the pairing (victims, property crime, care, congestion and housing have two ends); every
other row is its central. Disease and food safety are outside the total, as for the union, and are not priced here.
Outputs: derived/social_rows.csv (item x group: low, high, per member), derived/combined.csv (the main table).
Run from the repository root after rekey_indian.py and acs_custody.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/indian_full_account_2026_09_29/social_rows.py
"""
from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True   # read-only imports from other lanes: write nothing beside them

import pandas as pd  # noqa: E402

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
DER = LANE / "derived"
_spec = importlib.util.spec_from_file_location("air_items", FISCAL / "air_pollution_2026_09_28/air_items.py")
AIR = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(AIR)

FAILS: list[str] = []


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


PAIR = pd.read_csv(FISCAL / "population_basis_2026_09_29/derived/restated_pairing.csv")
FRAME = pd.read_csv(FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv").set_index("count")
N_U = float(FRAME.loc["union|all", "row4"])
N_ALL = float(FRAME.loc["cps_all_civilian|all", "row4"])
DRV = pd.read_csv(DER / "drivers.csv").set_index("group")
KEYS = pd.read_csv(DER / "keys.csv").set_index(["group", "key"]).value
INST = pd.read_csv(DER / "acs_institutional.csv").set_index("group")
FIS = pd.read_csv(DER / "rekey_summary.csv")

ITEMS = ["victims", "property_crime", "unreimbursed_care", "congestion", "housing_gain", "fear_avoidance",
         "private_security", "school_disruption", "pm25_consumption", "road_crash_externality", "scale_net_earnings",
         "restaurant_variety_market_size", "formal_volunteering_outside_group", "total_consumer_scale",
         "total_trade_travel_fdi"]
GROUPS = ["mexican_origin_rough", "mexican_origin_rough_white_ages", "indian_origin", "indian_origin_white_ages",
          "india_born", "india_born_white_ages", "A1_third_plus_nh_white",
          "indian_origin_g2_pooled", "indian_origin_g2_pooled_white_ages", "india_born_self_employed_adults",
          "india_born_wage_salary_adults", "india_born_other", "indian_origin_self_employed_households",
          "indian_origin_wage_salary_households"]
LABEL = {"mexican_origin_rough": "mexican_origin", "mexican_origin_rough_white_ages": "mexican_origin_white_ages"}

S_SECURITY = 74.438                        # social_costs_unpriced components.csv security_crime_driven_bn_central
OSS_RATE = 0.05                            # CRDC 2021-22 First Look p.22
CRDC = {"hisp": (0.24, 0.29), "asian": (0.01, 0.06), "asian_lo": (0.004, 0.06), "asian_hi": (0.019, 0.06),
        "white": (0.32, 0.45)}             # (suspension share, enrollment share), Figure 12 boys + girls
WHITE_VICTIM_RATIO = 11.4964 / 23.4535     # white lane non-white victims over the union's non-Hispanic-victims arm
VOL_RATE = {"hisp": 0.169, "all": 0.283}   # CEV 2023, benefits_inventory_2026_09_28
SCALE_CZ = {"scale": 38.64683303419723, "composition": -24.92909982784804}   # scale_spillovers summary.csv, CZ 1990
SCALE_ROW4 = 0.981827                      # restated_pairing.csv scale_net_earnings factor
SCALE_JOINT = 13.927466764218613           # summary.csv joint_grid CZ 1990 central: the joint fit, not the parts' sum
# trade_networks_2026_09_28 items.csv centrals and inputs
TRADE_U = {"trade": -6.1951, "vfr": -0.4682, "fdi": -0.1056}
MX_NONTRAVEL = 334.4921 + 50.4 - 22.2 + 503.1101 + 45.1 - 26.3
IN_GOODS = 41.5812 + 87.2848               # Census c5330, 2024 [SOURCE: census.gov/foreign-trade/balance/c5330.html]
IN_SERV = 41.8 + 43.1                      # USTR India page: 2025 $42.9bn / $47.6bn less the stated 2024-25 changes
NONTRAVEL = {"low": 0.5, "central": 0.75, "high": 1.0}   # [ASSUMPTION] non-travel part of US-India services
USDIA = {"india": 63.640, "mexico_net": 155.901 - 15.294}   # BEA usdia detailedcountry 2024; Mexico net of holding
MEXBORN = 12_220_781.9                     # trade lane POP mexico_born


def pair_value(item, end):
    """The union's row on row 4 (the 5+ basis for traffic rows), low or high end."""
    for sec in ("row_5plus", "row"):
        r = PAIR[(PAIR.section == sec) & (PAIR["item"] == item)]
        if len(r):
            r = r.set_index("end").restated
            return float(r["both"] if "both" in r.index else r[end])
    raise KeyError(item)


def crime_ratio(g):
    """Offending per member over the union's."""
    if g == "A1_third_plus_nh_white":
        return WHITE_VICTIM_RATIO
    if g.startswith("mexican_origin"):
        return 1.0 if g == "mexican_origin_rough" else float(KEYS[(g, "crime_age_factor")])
    base = "indian_origin" if g.startswith("indian") else "india_born"
    return float(INST.loc[base, "per_member_over_union_proxy"]) * float(KEYS[(g, "crime_age_factor")])


def relative_offending_all(g):
    """Offending per member over all residents' (the security formula)."""
    if g == "A1_third_plus_nh_white":
        return float(KEYS[(g, "custody")]) / (DRV.loc[g, "population"] / N_ALL)
    if g.startswith("mexican_origin"):
        pop = N_U / N_ALL
        off = pop + pair_value("private_security", "low") / S_SECURITY
        return off / pop * (1.0 if g == "mexican_origin_rough" else float(KEYS[(g, "crime_age_factor")]))
    base = "indian_origin" if g.startswith("indian") else "india_born"
    return float(INST.loc[base, "per_member_over_all"]) * float(KEYS[(g, "crime_age_factor")])


def gap(oss, enr):
    return OSS_RATE * oss / enr - OSS_RATE * (1 - oss) / (1 - enr)


def pm25(g, n, cons_ratio):
    """The air lane's grid for a group: its count on the row-4 frame, r scaled by consumption per member."""
    AIR.POP_ALL = N_ALL
    base = "mexican_origin"
    AIR.GROUPS[g] = dict(n=n, n_mexico_born=0.0, income_pc=0.0)
    AIR.ARMS["r"][g] = [x * cons_ratio for x in AIR.ARMS["r"][base]]
    AIR.ARMS["E"][g] = AIR.ARMS["E"][base]
    if g.startswith("indian") or g.startswith("india"):
        AIR.ARMS["iota"][g] = [0.15, 0.10, 0.05]
    elif g.startswith("A1"):
        AIR.ARMS["iota"][g] = [0.15, 0.12, 0.10]
    else:
        AIR.ARMS["iota"][g] = AIR.ARMS["iota"][base]
    grid, _ = AIR.pm_grid(g)
    vals = grid.others * grid.morb * AIR.VSL_DOT_2024 / 1e9
    cen = grid[(grid[[c for c in grid.columns if c.startswith("i_")]] == 1).all(axis=1)].iloc[0]
    return float(cen.others * cen.morb * AIR.VSL_DOT_2024 / 1e9), float(vals.min()), float(vals.max())


def main():
    u = DRV.loc["mexican_origin_rough"]
    uni = {it: {e: pair_value(it, e) for e in ("low", "high")} for it in ITEMS}
    print("[gates]", flush=True)
    c, lo, hi = pm25("mexican_origin_check", N_U, 1.0)
    gate("PM2.5: the air lane's grid on the row-4 union reproduces the priced central 68.092104 (1e-6)",
         abs(c - 68.092103594) < 1e-6, f"{c:.9f} ({lo:.4f}-{hi:.4f})")
    fiscal27 = PAIR[(PAIR.section == "row") & (PAIR["item"] == "fiscal")].set_index("end").restated
    tot = PAIR[PAIR.section == "pairing_5plus"].set_index("end").restated
    for e in ("low", "high"):
        s = sum(uni[it][e] for it in ITEMS)
        gate(f"{e}: the union's rows plus the September 27 fiscal row give the pairing's {tot[e]:.6f} (1e-6)",
             abs(s + float(fiscal27[e]) - float(tot[e])) < 1e-6, f"{s + float(fiscal27[e]):.6f}")
    nat = DRV.loc["mexican_origin_rough"]
    joint = SCALE_JOINT / (SCALE_CZ["scale"] + SCALE_CZ["composition"])   # parts rescaled to the joint central
    k_s = SCALE_CZ["scale"] * joint * SCALE_ROW4 / float(nat.scale_gain_national_bn)
    k_c = SCALE_CZ["composition"] * joint * SCALE_ROW4 / float(nat.composition_gain_national_bn)
    gate("scale net: the union's parts at the CZ level and row-4 factor give the pairing's row (1e-3)",
         abs(-(k_s * nat.scale_gain_national_bn + k_c * nat.composition_gain_national_bn) - uni["scale_net_earnings"]["low"]) < 1e-3)
    if FAILS:
        print(f"FAIL: {FAILS}")
        sys.exit(1)

    rows = []
    in_nt = {k: IN_GOODS + v * IN_SERV for k, v in NONTRAVEL.items()}
    for g in GROUPS:
        dg = DRV.loc[g]
        n = float(dg.population)
        per = n / N_U                                    # the union's per-member row scaled to the group's count
        ratio = {"victims": crime_ratio(g), "property_crime": crime_ratio(g), "fear_avoidance": crime_ratio(g),
                 "unreimbursed_care": dg.uninsured_py_pm / u.uninsured_py_pm, "congestion": 1.0,
                 "housing_gain": dg.renter_consumption_pm / u.renter_consumption_pm,
                 "road_crash_externality": (dg.miles_share / n) / (u.miles_share / N_U),
                 "restaurant_variety_market_size": dg.consumption_pm / u.consumption_pm,
                 "total_consumer_scale": dg.consumption_pm / u.consumption_pm}
        rate = VOL_RATE["hisp"] if g.startswith("mexican") else VOL_RATE["all"]
        ratio["formal_volunteering_outside_group"] = dg.persons_16plus_pm / u.persons_16plus_pm * rate / VOL_RATE["hisp"]
        val, note = {}, {}
        for it, r in ratio.items():
            val[it] = {e: uni[it][e] * per * r for e in ("low", "high")}
            note[it] = f"x{r:.4f} per member"
        # security: the lane's formula
        rel = relative_offending_all(g)
        v = S_SECURITY * (n / N_ALL) * (rel - 1)
        val["private_security"] = {"low": v, "high": v}
        note["private_security"] = f"74.438 x {n / N_ALL:.5f} x ({rel:.4f} - 1)"
        # school: the group's suspension gap and pupils per member
        crdc = "hisp" if g.startswith("mexican") else ("white" if g.startswith("A1") else "asian")
        rs = gap(*CRDC[crdc]) / gap(*CRDC["hisp"]) * dg.pupils_5_17_pm / u.pupils_5_17_pm
        val["school_disruption"] = {e: uni["school_disruption"][e] * per * rs for e in ("low", "high")}
        note["school_disruption"] = f"gap {gap(*CRDC[crdc]):.4f} vs Hispanic {gap(*CRDC['hisp']):.4f}; x{rs:.4f} per member"
        # PM2.5
        c, lo, hi = pm25(g, n, dg.consumption_pm / u.consumption_pm)
        val["pm25_consumption"] = {"low": c, "high": c}
        note["pm25_consumption"] = f"grid {lo:.3f}-{hi:.3f}; r x{dg.consumption_pm / u.consumption_pm:.4f}"
        # scale net
        v = -(k_s * dg.scale_gain_national_bn + k_c * dg.composition_gain_national_bn)
        val["scale_net_earnings"] = {"low": v, "high": v}
        note["scale_net_earnings"] = (f"scale {-k_s * dg.scale_gain_national_bn:.3f}, composition "
                                      f"{-k_c * dg.composition_gain_national_bn:.3f}")
        # trade
        if g.startswith("mexican"):
            v = uni["total_trade_travel_fdi"]["low"]
            note["total_trade_travel_fdi"] = "the union's row (ties do not move with age)"
        elif g.startswith("A1"):
            v = 0.0
            note["total_trade_travel_fdi"] = "no origin-country ties"
        else:
            g1 = float(DRV.loc["india_born", "population"])
            t = {k: TRADE_U["trade"] * x / MX_NONTRAVEL for k, x in in_nt.items()}
            v = t["central"] + TRADE_U["vfr"] * g1 / MEXBORN + TRADE_U["fdi"] * USDIA["india"] / USDIA["mexico_net"]
            v *= float(dg.india_born_persons) / g1      # a subgroup carries its India-born members' part
            note["total_trade_travel_fdi"] = (f"trade {t['central']:.3f} ({t['high']:.3f} to {t['low']:.3f} over the travel "
                                              f"share); visits {TRADE_U['vfr'] * g1 / MEXBORN:.3f}; FDI "
                                              f"{TRADE_U['fdi'] * USDIA['india'] / USDIA['mexico_net']:.3f}")
        val["total_trade_travel_fdi"] = {"low": v, "high": v}
        cong_alt = uni["congestion"]["low"] * per * ratio["road_crash_externality"]
        note["congestion"] = f"per member as the union; by driver miles {cong_alt:.3f} at the low end"
        for it in ITEMS:
            rows.append({"group": LABEL.get(g, g), "item": it, "population": f"{n:.0f}",
                         "low_bn": f"{val[it]['low']:.4f}", "high_bn": f"{val[it]['high']:.4f}",
                         "low_per_member": f"{val[it]['low'] * 1e9 / n:.0f}",
                         "high_per_member": f"{val[it]['high'] * 1e9 / n:.0f}", "rule": note.get(it, "")})
    soc = pd.DataFrame(rows)
    for c in ("low_bn", "high_bn"):
        soc[c] = soc[c].astype(float)
    u_rows = soc[soc.group == "mexican_origin"].set_index("item")
    for it in ITEMS:
        if it not in ("private_security", "school_disruption", "pm25_consumption", "scale_net_earnings"):
            continue
        gate(f"the union's own-age {it} rebuilds its pairing row (1e-3)",
             abs(u_rows.loc[it, "low_bn"] - uni[it]["low"]) < 1e-3, f"{u_rows.loc[it, 'low_bn']:.4f} vs {uni[it]['low']:.4f}")
    for it in ITEMS:
        gate(f"the union's own-age {it} equals the pairing (1e-3)",
             max(abs(u_rows.loc[it, "low_bn"] - uni[it]["low"]), abs(u_rows.loc[it, "high_bn"] - uni[it]["high"])) < 1e-3)
    if FAILS:
        print(f"FAIL: {FAILS}")
        sys.exit(1)

    # combined: fiscal (accrual: the case; cash beside) + social
    comb = []
    eng = FIS[(FIS.group == "mexican_origin_engine")].set_index(["basis", "end"])
    rough = FIS[(FIS.group == "mexican_origin_rough")].set_index(["basis", "end"])
    for g in GROUPS + ["mexican_origin_engine"]:
        sg = "mexican_origin" if g == "mexican_origin_engine" else LABEL.get(g, g)
        s = soc[soc.group == sg]
        for b in ("accrual", "cash"):
            for e in ("low", "high"):
                f = FIS[(FIS.group == g) & (FIS.basis == b) & (FIS.end == e)].iloc[0]
                fis = float(f.cost_bn)
                if g == "mexican_origin_rough_white_ages":   # the engine's level plus the rough method's age effect
                    fis_cal = float(eng.loc[(b, e), "cost_bn"]) + fis - float(rough.loc[(b, e), "cost_bn"])
                else:
                    fis_cal = fis
                social = float(s[f"{e}_bn"].sum())
                n = float(f.population)
                comb.append({"group": g, "basis": b, "end": e, "population": f"{n:.0f}",
                             "fiscal_bn": f"{fis_cal:.4f}", "fiscal_rough_bn": f"{fis:.4f}", "social_bn": f"{social:.4f}",
                             "total_bn": f"{fis_cal + social:.4f}",
                             "fiscal_per_member": f"{fis_cal * 1e9 / n:.0f}",
                             "fiscal_per_member_se": "" if pd.isna(f.cost_per_member_se) else f"{f.cost_per_member_se:.0f}",
                             "social_per_member": f"{social * 1e9 / n:.0f}",
                             "total_per_member": f"{(fis_cal + social) * 1e9 / n:.0f}",
                             "fiscal_top_tail_proportional_per_member": f"{float(f.cost_top_tail_proportional_bn) * 1e9 / n:.0f}"})
    for name, data in (("social_rows.csv", soc.assign(low_bn=soc.low_bn.map("{:.4f}".format),
                                                        high_bn=soc.high_bn.map("{:.4f}".format)).to_dict("records")),
                       ("combined.csv", comb)):
        with open(DER / name, "w", newline="") as fh:
            wr = csv.DictWriter(fh, fieldnames=list(data[0]), lineterminator="\n")
            wr.writeheader()
            wr.writerows(data)
    print(soc.pivot(index="item", columns="group", values="low_per_member").to_string())
    print(pd.DataFrame(comb).query("basis == 'accrual'")[["group", "end", "fiscal_bn", "social_bn", "total_bn",
                                                          "fiscal_per_member", "social_per_member",
                                                          "total_per_member"]].to_string(index=False))


if __name__ == "__main__":
    main()
