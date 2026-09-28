"""Four unpriced social costs, Mexican-origin union vs non-Hispanic Black residents, 2024 $.

One method per item, applied to both groups. Every constant carries its source tag in INPUTS
(written to derived/inputs.csv). Outputs: derived/items.csv, derived/components.csv.
Frame: annual cost to residents outside the group; negative = a gain to them.
"""
import csv
from pathlib import Path

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
DER = LANE / "derived"
VICTIM = FISCAL / "crime_victim_cost_2026_09_23" / "derived"
COMP = FISCAL / "black_comparator_rough_2026_09_28" / "derived"

INPUTS = {}


def inp(name, value, source):
    INPUTS[name] = (value, source)
    return value


# ---- price levels (CPI-U annual averages) ---------------------------------------------------
CPI = {y: inp(f"cpi_{y}", v, "[TRAINING-DATA] BLS CPI-U annual average") for y, v in
       {1990: 130.7, 2000: 172.2, 2022: 292.655, 2024: 313.689}.items()}


def to2024(x, year):
    return x * CPI[2024] / CPI[year]


# ---- groups ---------------------------------------------------------------------------------
POP_ALL = inp("pop_cps_civilian", 336_727_803, "[DATA] crime_victim_cost target_population_cps2025.csv")
with open(COMP / "cps_profile.csv") as f:
    _n_blk = next(float(r["population"]) for r in csv.DictReader(f) if r["group"] == "nh_black")
N = {"mexican_origin": inp("n_mexican_origin", 40_896_574, "[DATA] same file, union all ages"),
     "nh_black": inp("n_nh_black", _n_blk, "[DATA] black_comparator cps_profile.csv: CPS ASEC 2025 PRDTRACE==2 & PEHSPNON==2")}
SHARE = {g: n / POP_ALL for g, n in N.items()}

# ---- victim cost to other residents, full (Miller 2021 victim-only), $bn --------------------
UNIT_FULL = {}
with open(VICTIM / "unit_costs_victim_only_2024usd.csv") as f:
    for r in csv.DictReader(f):
        if r["price_set"] == "miller2021":
            UNIT_FULL[r["offence"]] = float(r["full"])
OFFENCES = ["Murder", "Rape/sexual assault", "Robbery", "Aggravated assault", "Simple assault"]
V = {"mexican_origin": {o: 0.0 for o in OFFENCES}}
with open(VICTIM / "cost_by_victim_and_offence_central.csv") as f:
    for r in csv.DictReader(f):
        V["mexican_origin"][r["offence"]] += float(r["cost_full"]) / 1e9
v_mex_total = sum(V["mexican_origin"].values())
assert abs(v_mex_total - 28.9229) < 0.01, v_mex_total  # arms.csv central
# Black: the comparator lane's NCVS 2022-24 x SHR 2024 x CDC WONDER run on the same Miller prices, non-Black victims
V["nh_black"] = {o: 0.0 for o in OFFENCES}
with open(COMP / "victim_cost_by_offence.csv") as f:
    for r in csv.DictReader(f):
        if r["arm"] == "ncvs_pooled_2022_2024" and r["victim"] != "Black":
            V["nh_black"][r["offence"]] += float(r["full_bn"])
inp("v_black_nonblack_full_bn", round(sum(V["nh_black"].values()), 4),
    "[DATA] black_comparator victim_cost_by_offence.csv, arm ncvs_pooled_2022_2024, non-Black victims")

# ---- item 1: fear and avoidance (non-victims) -----------------------------------------------
# Cohen, Rust, Steen & Tidd 2004 WTP per crime prevented, 2000 $ (Criminology 42(1), OJP abstract)
WTP2000 = {"Murder": 9.7e6, "Rape/sexual assault": 237e3, "Aggravated assault": 70e3, "Armed robbery": 232e3}
for k, v in WTP2000.items():
    inp(f"wtp2000_{k}", v, "[SOURCE] Cohen et al. 2004 via ojp.gov abstract")
ARMED_SHARE = inp("robbery_armed_share", 0.45, "[UNVERIFIED] share of robberies with a weapon")
excess = {}
for o in ["Murder", "Rape/sexual assault", "Aggravated assault"]:
    excess[o] = to2024(WTP2000[o], 2000) / UNIT_FULL[o] - 1
rob_uncapped = ARMED_SHARE * (to2024(WTP2000["Armed robbery"], 2000) / UNIT_FULL["Robbery"] - 1)
PHI = {"low": 0.25, "central": 0.5, "high": 1.0}  # [ASSUMPTION] fear/avoidance share of WTP excess
inp("phi_low_central_high", "0.25/0.5/1.0", "[ASSUMPTION] share of WTP-minus-victim-cost that is non-victim fear/avoidance")


def fear(g, arm):
    ex = dict(excess)
    ex["Robbery"] = rob_uncapped if arm == "high" else min(rob_uncapped, 1.0)
    ex["Simple assault"] = excess["Aggravated assault"] if arm == "high" else 0.0
    return PHI[arm] * sum(ex[o] * V[g][o] for o in OFFENCES)


# ---- item 2: private security ---------------------------------------------------------------
# Census SAS employer revenue 2022 ($m, FRED REVEF5616xxALLEST) and BLS OES May 2025 (API)
REV22 = {"guards_contract_561612": 32_222, "systems_561621": 28_295, "locksmiths_561622": 2_701,
         "armored_561613": 4_162, "investigation_561611": 7_850}
for k, v in REV22.items():
    inp(f"rev2022_m_{k}", v, "[SOURCE] Census SAS via FRED fredgraph.csv (_cache/fred_*.csv)")
OES_ALL = (inp("oes_33_9032_emp", 1_283_470, "[SOURCE] BLS OES May 2025 API series OEUN000000000000033903201"),
           inp("oes_33_9032_wage", 42_470, "[SOURCE] BLS OES May 2025 API ...04"))
OES_5616 = (inp("oes_33_9032_emp_5616", 768_900, "[SOURCE] BLS OES May 2025 API OEUN000000056160033903201"),
            inp("oes_33_9032_wage_5616", 41_380, "[SOURCE] BLS OES May 2025 API ...04"))
LOAD = inp("comp_per_wage", 1.40, "[TRAINING-DATA] BLS ECEC: benefits ~29% of private compensation")
PRIVATE = inp("inhouse_private_share", 0.85, "[ASSUMPTION] excludes government-employed guards (in fiscal account)")
DEFL25 = inp("deflate_2025_to_2024", 0.975, "[ASSUMPTION] ~2.5% CPI 2024->2025")
EQUIP = {"low": 5.0, "central": 10.0, "high": 20.0}
inp("equipment_bn", "5/10/20", "[UNVERIFIED] direct purchases of locks, cameras, alarms, anti-theft; no primary total")
inhouse_bn = (OES_ALL[0] * OES_ALL[1] - OES_5616[0] * OES_5616[1]) / 1e9 * LOAD * PRIVATE * DEFL25
CRIME_SHARE = {  # [ASSUMPTION] share of each line that exists because of crime
    "guards": (0.5, 0.7, 0.9), "systems": (0.4, 0.6, 0.8), "locksmiths": (0.3, 0.5, 0.7),
    "armored": (0.5, 0.75, 1.0), "investigation": (0.0, 0.1, 0.3), "equipment": (0.8, 0.8, 0.8)}
inp("crime_shares", str(CRIME_SHARE), "[ASSUMPTION]")


def s_total(i):
    arm = ["low", "central", "high"][i]
    r = {k: to2024(v / 1e3, 2022) for k, v in REV22.items()}
    lines = {"guards": r["guards_contract_561612"] + inhouse_bn, "systems": r["systems_561621"],
             "locksmiths": r["locksmiths_561622"], "armored": r["armored_561613"],
             "investigation": r["investigation_561611"], "equipment": EQUIP[arm]}
    return sum(lines[k] * CRIME_SHARE[k][i] for k in lines), lines


# offending shares: property = FBI 2019 Table 43A arrests (Black 29.8% of race-reported property
# arrests); Mexican property = lane's group offences / victimisations (cost- and count-weighted);
# violent = victim-cost share of the national total (comparator lane; Mexican from lane rows)
with open(COMP / "victim_cost_summary.csv") as f:
    _vs = {(r["arm"], r["victims"]): float(r["full_bn"]) for r in csv.DictReader(f)}
NAT_VIOLENT_BN = inp("national_violent_victim_cost_bn", _vs[("national_all_offenders", "all victims")],
                     "[DATA] black_comparator victim_cost_summary.csv: 2024 NCVS + WONDER x Miller full")
BLK_PROP = inp("black_share_property_arrests_2019", 0.298, "[SOURCE] FBI CIUS 2019 Table 43A")
BLK_VIOL = inp("black_offender_violent_cost_bn", _vs[("ncvs_pooled_2022_2024", "all victims")],
               "[DATA] black_comparator victim_cost_summary.csv, all victims") / NAT_VIOLENT_BN
prop = []
with open(VICTIM / "property_proxy.csv") as f:
    prop = [r for r in csv.DictReader(f) if r["price_set"] == "miller2021"]
mex_prop_cost = sum(float(r["group_offences"]) * float(r["unit_victim_cost"]) for r in prop) / \
    sum(float(r["victimisations_2024"]) * float(r["unit_victim_cost"]) for r in prop)
mex_prop_count = sum(float(r["group_offences"]) for r in prop) / sum(float(r["victimisations_2024"]) for r in prop)
grp_total = 0.0
with open(VICTIM / "cost_by_victim_and_offence_central.csv") as f:
    for r in csv.DictReader(f):
        n = r["group_victimisations"] or r["group_incidents"]
        grp_total += float(n) * float(r["unit_full"]) / 1e9
mex_viol_ncvs = grp_total / NAT_VIOLENT_BN
mex_viol_arrest = grp_total * (43.1199 / 28.9229) / NAT_VIOLENT_BN  # lane's arrest-share arm, scaled
W_PROP = inp("security_weight_property", 0.75, "[ASSUMPTION] most security spend targets theft")
EXC = {
    "nh_black": {"low": BLK_PROP - SHARE["nh_black"],
                 "central": W_PROP * BLK_PROP + (1 - W_PROP) * BLK_VIOL - SHARE["nh_black"],
                 "high": BLK_VIOL - SHARE["nh_black"]},
    "mexican_origin": {"low": W_PROP * mex_prop_count + (1 - W_PROP) * mex_viol_ncvs - SHARE["mexican_origin"],
                       "central": W_PROP * mex_prop_cost + (1 - W_PROP) * mex_viol_ncvs - SHARE["mexican_origin"],
                       "high": W_PROP * mex_prop_cost + (1 - W_PROP) * mex_viol_arrest - SHARE["mexican_origin"]},
}


GUARD_MEAN = inp("guard_share_popweighted_pct", 0.6083, "[CALCULATION] guard_black.py on guard_labor panel")
REG_SHARE_PP = {"nh_black": inp("black_share_popweighted_pct", 12.024, "[CALCULATION] guard_black.py"),
                "mexican_origin": 100 * 0.11325}  # Mexican-origin national share (exposure.csv)
REG_B = {}
with open(DER / "guard_share_coefficients.csv") as f:
    for r in csv.DictReader(f):
        if r["sample"] == "all 51" and r["spec"].startswith("lane spec") and r["term"] in ("black_share", "hisp_share"):
            if (r["term"] == "black_share" and "fb +" in r["spec"]) or r["term"] == "hisp_share":
                REG_B["nh_black" if r["term"] == "black_share" else "mexican_origin"] = float(r["b_pp_per_pp"])


def reg_fraction(g):
    """Share of guard employment the lane's controlled state regression attributes to the group."""
    return REG_B[g] * REG_SHARE_PP[g] / GUARD_MEAN


def security(g):
    s = [s_total(i)[0] for i in range(3)]
    e = EXC[g]
    # low also admits the controlled cross-state regression (gross share x central spend)
    cand_low = [s[0] * e["low"], s[2] * e["low"], s[1] * reg_fraction(g)]
    cand_high = [s[0] * e["high"], s[2] * e["high"]]
    return min(cand_low), s[1] * e["central"], max(cand_high)


# ---- item 3: property values ----------------------------------------------------------------
# central/low 0 (transfer + capitalised crime/schools); high = taste arm, flagged
EXPO = {}
with open(DER / "exposure.csv") as f:
    for r in csv.DictReader(f):
        EXPO["mexican_origin" if r["group"].startswith("mex") else "nh_black"] = float(r["outsider_exposure_share"])
HH_SIZE = inp("persons_per_household", 2.5, "[TRAINING-DATA] ACS average household size ~2.5")
BFM_MEAN = inp("bfm_mean_mwtp_10pp_black_1990usd_month", -10.50, "[SOURCE] Bayer-Ferreira-McMillan w13236 Table 7")
BFM_DIFF = inp("bfm_black_vs_white_diff", 98.34, "[SOURCE] same, Table 7")
BFM_BLK_SHARE = inp("bfm_sample_black_share", 0.08, "[SOURCE] same, data section: full sample 68% white, 8% black")
mwtp_nonblack_2024 = to2024(BFM_MEAN - BFM_BLK_SHARE * BFM_DIFF, 1990)  # $/household/month per +10pp
HOUSING_PCE = inp("pce_housing_services_2024_bn", 2_900.0, "[TRAINING-DATA] BEA PCE housing services ~$2.9tn")
ACS_HISP_GRAD = inp("acs_hisp_grad_per_10pp", -0.0096, "[DATA] hedonic_composition_2026_09_19 ACS value, not a price")


def property_high(g):
    outsiders_hh = (POP_ALL - N[g]) / HH_SIZE
    if g == "nh_black":
        return -mwtp_nonblack_2024 * 12 * outsiders_hh * (EXPO[g] / 0.10) / 1e9
    return -ACS_HISP_GRAD * (EXPO[g] / 0.10) * HOUSING_PCE * (1 - SHARE[g])


# ---- item 4: school disruption --------------------------------------------------------------
PV = inp("pv_lifetime_earnings_2024", 750_886.47, "[DATA] school_dilution_2026_09_24 RESULT (CFR $522k 2010$)")
BETA = {"low": 0.15, "central": 0.165, "high": 0.20}
inp("chk_beta_per_unit_share_year", "0.15/0.165/0.20", "[SOURCE] CHK w22042 fn14: 0.6-0.8%/yr per peer in 25; AER 3.3%/5yr")
CRDC = "[SOURCE] CRDC 2021-22 First Look p.22 Figure 12 (ed.gov/media/document/2021-22-crdc-first-look-report-109194.pdf)"
OSS_RATE = inp("oss_rate_k12", 0.05, "[SOURCE] CRDC 2021-22 First Look p.22: 2.4M, 5% of K-12")
BLK_ENR, BLK_OSS = inp("black_enrol_share", 0.15, f"{CRDC}: boys 8% + girls 7%"), inp("black_oss_share", 0.35, f"{CRDC}: boys 22% + girls 13%")
HISP_ENR, HISP_OSS = inp("hisp_enrol_share", 0.29, f"{CRDC}: boys 15% + girls 14%"), inp("hisp_oss_share", 0.24, f"{CRDC}: boys 16% + girls 8%")
SHARES = {"nh_black": (BLK_OSS, BLK_ENR), "mexican_origin": (HISP_OSS, HISP_ENR)}  # Hispanic of any race proxies the union
ROUND = inp("crdc_rounding_bound", 0.01, "[CALCULATION] each printed share is rounded to 1 point, so a boys + girls sum is known to +/-1 point")
PUPIL_SHARE = {"nh_black": BLK_ENR, "mexican_origin": inp("mex_pupil_share", 8.487 / (8.487 + 39.45),
                                                          "[DATA] school_dilution: 8.487m group, 39.45m other pupils")}
POP_SHARE_ACS = {"nh_black": 0.11911, "mexican_origin": 0.11325}  # exposure.csv national shares
OUT_PUPILS = {"nh_black": inp("k12_enrol_m", 49.4, "[TRAINING-DATA] CRDC 2021-22 K-12 enrollment ~49.4M") * (1 - BLK_ENR),
              "mexican_origin": 39.45}
KAPPA = {"low": 0.3, "central": 0.6, "high": 1.0}
inp("kappa_behaviour_share_of_gap", "0.3/0.6/1.0", "[ASSUMPTION] share of discipline gap that is behaviour")
SCOPE = {"low": 6 / 13, "central": 6 / 13, "high": 1.0}  # CHK is elementary; high extends to K-12


def gap(g, arm):
    """Group's suspension rate minus other pupils', from its shares of suspensions and enrollment."""
    d = {"low": -ROUND, "central": 0.0, "high": ROUND}[arm]
    oss, enr = SHARES[g][0] + d, SHARES[g][1] - d
    return OSS_RATE * oss / enr - OSS_RATE * (1 - oss) / (1 - enr)


def school(g, arm, gap_arm=None):
    pupil_expo = EXPO[g] * PUPIL_SHARE[g] / POP_SHARE_ACS[g]
    return BETA[arm] * PV * OUT_PUPILS[g] * 1e6 * pupil_expo * gap(g, gap_arm or arm) * KAPPA[arm] * SCOPE[arm] / 1e9


def school_range(g):
    """Envelope over the corners: with a negative gap, the high parameters give the lowest cost."""
    corners = [school(g, a, b) for a in ("low", "high") for b in ("low", "high")]
    return min(corners), school(g, "central"), max(corners)


# ---- assemble -------------------------------------------------------------------------------
def main():
    rows, comp = [], []
    meta = {
        "fear_avoidance": ("modelled: CV WTP excess over victim cost x assumed fear share; contested",
                           "victim cost (excluded by construction); private security at high arm; property values",
                           "phi x sum_offence (Cohen 2004 WTP/Miller victim-only - 1) x group's victim cost to others; violent only"),
        "private_security": ("measured spend (Census SAS, BLS OES) x assumed crime share; arrest/victim-cost allocation",
                             "fear at high arm (WTP may include security); government guards excluded (fiscal)",
                             "crime-driven security x (group offending share - population share); property 0.75/violent 0.25"),
        "property_values": ("decision: transfer + capitalised crime/schools; high arm = taste (Black: BFM sorting; Mexican: ACS hedonic, not a price)",
                            "crime and school capitalisation (items 1, 2, 4, victim cost); high arm is taste-based",
                            "central 0; high = outsiders' WTP to avoid group neighbours x exposure [FRAMING-SENSITIVE]"),
        "school_disruption": ("causal peer estimate (CHK 2018) x contested discipline proxy",
                              "dilution lane (resources) is separate; school violence partly in NCVS victim cost",
                              "CHK beta x PV x outsider pupils x exposure x (group - others OSS rate) x behaviour share x grades"),
    }
    for g in ["mexican_origin", "nh_black"]:
        vals = {
            "fear_avoidance": tuple(fear(g, a) for a in ["low", "central", "high"]),
            "private_security": security(g),
            "property_values": (0.0, 0.0, property_high(g)),
            "school_disruption": school_range(g),
        }
        # the Black school low is set to 0 by the disconfirming race-composition evidence (HKR, Angrist-Lang)
        if g == "nh_black":
            vals["school_disruption"] = (0.0,) + vals["school_disruption"][1:]
        for item, (lo, ce, hi) in vals.items():
            ev, dc, note = meta[item]
            rows.append({"item": item, "group": g, "low_bn": f"{lo:.2f}", "central_bn": f"{ce:.2f}",
                         "high_bn": f"{hi:.2f}", "per_member_usd": f"{ce * 1e9 / N[g]:.0f}",
                         "evidence_level": ev, "double_count_with": dc, "method_note": note})
        comp += [{"group": g, "component": f"victim_full_{o}", "value": f"{V[g][o]:.4f}"} for o in OFFENCES]
        comp += [{"group": g, "component": f"security_excess_{a}", "value": f"{EXC[g][a]:.5f}"} for a in EXC[g]]
        comp += [{"group": g, "component": "outsider_exposure", "value": f"{EXPO[g]:.5f}"},
                 {"group": g, "component": "oss_gap_central", "value": f"{gap(g, 'central'):.5f}"},
                 {"group": g, "component": "population_share", "value": f"{SHARE[g]:.5f}"}]
    for i, a in enumerate(["low", "central", "high"]):
        tot, lines = s_total(i)
        comp.append({"group": "national", "component": f"security_crime_driven_bn_{a}", "value": f"{tot:.3f}"})
        comp += [{"group": "national", "component": f"security_line_bn_{k}", "value": f"{v:.3f}"} for k, v in lines.items()] if a == "central" else []
    comp += [{"group": "national", "component": f"wtp_excess_{o}", "value": f"{e:.4f}"} for o, e in excess.items()]
    comp += [{"group": "national", "component": "wtp_excess_robbery_uncapped", "value": f"{rob_uncapped:.4f}"},
             {"group": "national", "component": "mex_prop_share_cost", "value": f"{mex_prop_cost:.5f}"},
             {"group": "national", "component": "mex_prop_share_count", "value": f"{mex_prop_count:.5f}"},
             {"group": "national", "component": "mex_group_violent_cost_all_victims_bn", "value": f"{grp_total:.4f}"},
             {"group": "national", "component": "bfm_mwtp_nonblack_2024_month_10pp", "value": f"{mwtp_nonblack_2024:.3f}"},
             {"group": "national", "component": "inhouse_guards_bn", "value": f"{inhouse_bn:.3f}"}]
    for name, data, fields in [("items.csv", rows, list(rows[0])), ("components.csv", comp, ["group", "component", "value"]),
                               ("inputs.csv", [{"name": k, "value": v[0], "source": v[1]} for k, v in INPUTS.items()],
                                ["name", "value", "source"])]:
        with open(DER / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
            w.writeheader()
            w.writerows(data)
    for r in rows:
        print(f"{r['item']:18} {r['group']:15} {r['low_bn']:>8} {r['central_bn']:>8} {r['high_bn']:>8}  ${r['per_member_usd']}/member")
    for c in comp:
        print(c["group"], c["component"], c["value"])


if __name__ == "__main__":
    main()
