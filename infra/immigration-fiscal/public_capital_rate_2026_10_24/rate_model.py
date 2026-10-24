"""Opportunity-cost rate for public capital and its price in the v9 main case.

Model (steady-state Harberger weighting; see RESULT.md section 2):
    r = r_c + d * (r_i - r_c)
r_c = the case's 2.0810698764% (item 20); d = share of the capital's financing that displaces domestic private
investment; r_i = marginal pre-tax real return on the displaced private capital. Foreign-financed and
consumption-financed shares cost r_c. The case's capital return is linear in the rate, so each line moves by
return_at_rc * (r / r_c - 1).

Inputs read here:
- main_case_2026_10_16/derived/rate_check.json: arm B (2.081%) and arm capital_7pct (7% on capital only).
- main_case_2026_10_16/derived/summary.json v9.one_rate: per-line B-minus-v8 deltas (v8 rates 2% low, 3% high),
  used only for the line split, scaled to the v9 totals implied by the 7% arm.
Run (theta_item6.cjs first; it writes derived/theta_item6.json, read below):
    node infra/immigration-fiscal/public_capital_rate_2026_10_24/theta_item6.cjs
    uv run --no-project python3 infra/immigration-fiscal/public_capital_rate_2026_10_24/rate_model.py
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASE = HERE.parent / "main_case_2026_10_16" / "derived"
OUT = HERE / "derived"
OUT.mkdir(exist_ok=True)

summary = json.loads((CASE / "summary.json").read_text())
check = json.loads((CASE / "rate_check.json").read_text())
RC = summary["v9"]["one_rate"]["flat_real_equivalent"]
V8_RATE = {"low": 0.02, "high": 0.03}  # v8 rule: 2% low end, 3% high end (decision v9, alternative 2)
assert abs(RC - 0.020810698764237804) < 1e-15

B = check["arms"]["B"]["set"]
S7 = check["arms"]["capital_7pct"]["set"]
assert abs(B[0] - 368.0297) < 1e-3 and abs(B[1] - 436.5615) < 1e-3, "[BLOCKED] arm B moved"
# cash set moves by the same capital amount (capital return is not a pension leg)
for i in range(2):
    d_set = S7[i] - B[i]
    d_cash = check["arms"]["capital_7pct"]["cash"][i] - check["arms"]["B"]["cash"][i]
    assert abs(d_set - d_cash) < 1e-6, "[BLOCKED] set and cash 7% deltas differ"
CAP = {e: (S7[i] - B[i]) / (0.07 / RC - 1) for i, e in enumerate(["low", "high"])}

# Line split from the source-owned B-minus-v8 parts (method b_hotdeck_union_matched; the other method checked).
FED = {"pos_fed", "health_fed", "health_fed_user_fees", "gps_fed", "hwy_fed", "air_fed", "rec_fed"}
GROUP = {
    "k12": "schools", "k12_user_fees": "schools", "college": "colleges", "college_user_fees": "colleges",
    "pos_sl": "police/safety", "pos_fed": "police/safety", "health_sl": "health", "health_fed": "health",
    "health_sl_user_fees": "health", "health_fed_user_fees": "health", "hwy_sl": "roads", "hwy_fed": "roads",
    "air_fed": "transport", "rec_sl": "parks", "rec_fed": "parks", "gps_sl": "general government",
    "gps_fed": "general government",
}
lines = {}
for e in ("low", "high"):
    ratio = RC / V8_RATE[e] - 1
    by = summary["v9"]["one_rate"]["by_end"][e]["by_method"]
    tot = {}
    for m, mv in by.items():
        acc = defaultdict(float)
        for p in mv["parts"]:
            key = p["line"] if p["component"] == "capital_engine" else p["component"]
            acc[key] += p["delta_bn"] / ratio * (1 + ratio)
        tot[m] = acc
    a, b = tot["b_hotdeck_union_matched"], tot["b_matched_over_pooled"]
    assert abs(sum(a.values()) - sum(b.values())) / sum(a.values()) < 0.002, "[BLOCKED] methods disagree"
    scale = CAP[e] / sum(a.values())
    assert abs(scale - 1) < 0.01, f"[BLOCKED] v8-standalone split vs v9 total off by {scale - 1:.4f}"
    lines[e] = {k: v * scale for k, v in a.items()}


def group_of(k):
    if k.startswith("ent_"):
        return "enterprises"
    if k in ("capital_reporter", "capital_coverage"):
        return "union-completion and coverage capital"
    return GROUP[k]


def level_of(k):
    # federal enterprises (ent_other_fed, ent_power_fed) carry the federal margin too
    if k in FED or k.endswith("_fed"):
        return "federal"
    # federal-aid grants finance part of state/local highway capital at the federal margin
    return "state_local_hwy" if k == "hwy_sl" else "state_local"


# Inputs (sources in reads/). Each tuple is (low, central, high).
MPS = (0.024, 0.067, 0.11)          # marginal propensity to save out of disposable income: Dynan et al. via Moore et al. 2004 n.7; central = midpoint
DOMESTIC = (0.39, 0.57, 0.71)        # share of a national-saving decline that falls on domestic investment: Huntley 2014 small/central/large
D_BOND = (0.15, 0.33, 0.50)          # investment displaced per $ of borrowing: Huntley 2014 / CBO 2025 LTBO 0.33 (0.15-0.50)
D_TAX_HIGH_OVERRIDE = 0.15           # [INFERENCE] widening for business-paid taxes out of owners' saving
DEBT_SHARE_SL = 0.21                 # school_capital_return_2026_09_26 RESULT section 7: debt finances 21% of K-12 capital
d_tax = (MPS[0] * DOMESTIC[0], MPS[1] * DOMESTIC[1], D_TAX_HIGH_OVERRIDE)
d_sl = tuple((1 - DEBT_SHARE_SL) * t + DEBT_SHARE_SL * b for t, b in zip(d_tax, D_BOND))
d_fed = (d_tax[0], D_BOND[1], D_BOND[2])  # federal margin: tax-financed (low) to CBO deficit-financed (central/high)
# FHWA 23rd C&P Report, Highlights: the federal government funded 42.5% of highway capital spending in 2014
HWY_FED_SHARE = 0.425
d_hwy_sl = tuple(HWY_FED_SHARE * f + (1 - HWY_FED_SHARE) * s for f, s in zip(d_fed, d_sl))
D_BY_LEVEL = {"state_local": d_sl, "state_local_hwy": d_hwy_sl, "federal": d_fed}
# marginal pre-tax private return
R_I = {
    "aaa_real_2024": 0.050442 - 0.022601,   # FRED AAA 2024 mean minus Cleveland Fed 10y expected inflation 2024 mean
    "baa_real_2024": 0.057533 - 0.022601,
    "ce_pretax_tau25": RC / (1 - 0.25),     # certainty-equivalent pre-tax: r_c/(1 - tau_k), tau_k 2024 = 0.25 (GRR series)
    "grr_all_capital_pretax_2024": 0.0752,  # GRR all capital pre-tax 2024 annual mean (usdata.csv)
    "grr_all_capital_pretax_1947_2024": 0.0741,
    "omb_a94_1992": 0.07,
}
SCEN = {
    "low (open economy, SPC=1; Lind 1990, A-4 2023 lower value)": ("zero", None),
    "central (d central, r_i = Baa real 2024)": (1, R_I["baa_real_2024"]),
    "high (d high, r_i = GRR measured pre-tax 2024)": (2, R_I["grr_all_capital_pretax_2024"]),
    "beside: d central, r_i = GRR measured (no risk adjustment)": (1, R_I["grr_all_capital_pretax_2024"]),
    "beside: full displacement at 7% (A-94 1992 / A-4 2003)": ("full", 0.07),
    # Burgess & Zerbe (2011): the capital market is the marginal source for every project (debt paydown is the
    # alternative use), weights = CBO's 33/43/24 for every line.
    "beside: Burgess-Zerbe margin, CBO weights, risk-consistent returns": ("soc", (R_I["baa_real_2024"], RC, RC)),
    "beside: Burgess-Zerbe SOC, CBO weights, measured GRR returns": ("soc", (R_I["grr_all_capital_pretax_2024"], 0.0540, 0.0540)),
}
CBO_W = (0.33, 0.43, 0.24)  # displaced investment, induced private saving, foreign inflow (Huntley 2014 central)


def rate(level, scen):
    which, ri = scen
    if which == "zero":
        return RC
    if which == "full":
        return ri
    if which == "soc":
        return sum(w * r for w, r in zip(CBO_W, ri))
    d = D_BY_LEVEL[level][which]
    return RC + d * (ri - RC)


rows, totals = [], {}
for name, scen in SCEN.items():
    for e in ("low", "high"):
        tot = 0.0
        for k, v in sorted(lines[e].items()):
            r = rate(level_of(k), scen)
            delta = v * (r / RC - 1)
            tot += delta
            rows.append({"scenario": name, "end": e, "line": k, "group": group_of(k), "level": level_of(k),
                         "return_at_2081_bn": round(v, 4), "rate": round(r, 6), "delta_bn": round(delta, 4)})
        totals[(name, e)] = tot

with open(OUT / "line_deltas.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)

grp = defaultdict(lambda: [0.0, 0.0])
for e_i, e in enumerate(("low", "high")):
    for k, v in lines[e].items():
        grp[group_of(k)][e_i] += v

head = {"low": B[0], "high": B[1]}
out = {
    "r_c": RC,
    "capital_return_at_rc_bn": CAP,
    "check_7pct_arm_reproduced_bn": {e: CAP[e] * (0.07 / RC - 1) for e in CAP},
    "capital_return_by_group_at_rc_bn": {g: [round(x, 3) for x in v] for g, v in sorted(grp.items())},
    "d_state_local": d_sl, "d_state_local_highways": d_hwy_sl, "hwy_federal_share": HWY_FED_SHARE,
    "d_federal": d_fed, "d_tax": d_tax, "r_i_candidates": R_I,
    "state_local_rate": {n: rate("state_local", s) for n, s in SCEN.items()},
    "federal_rate": {n: rate("federal", s) for n, s in SCEN.items()},
    "headline_bn": {n: {"delta": [round(totals[(n, "low")], 3), round(totals[(n, "high")], 3)],
                        "headline": [round(head["low"] + totals[(n, "low")], 1),
                                     round(head["high"] + totals[(n, "high")], 1)]} for n in SCEN},
}
# Paired reading (RESULT section 7): theta = share of the measured return above the safe rate that scales with
# capital. Rate leg: r_i(theta) = Baa real + theta * (GRR - Baa real); item 6 leg from theta_item6.cjs, which prices
# the high-end corporate response 0.37 + theta * 0.63 on the v9 package (low end already at 1).
TH = json.loads((OUT / "theta_item6.json").read_text())
assert all(c["pass"] for c in TH["checks"]), "[BLOCKED] theta_item6 checks"


def r_i_theta(t):
    return R_I["baa_real_2024"] + t * (R_I["grr_all_capital_pretax_2024"] - R_I["baa_real_2024"])


theta_rows, pairing = [], {}
for name, e in TH["theta"].items():
    t = e["theta"]
    pairing[name] = {"theta": t, "r_i": r_i_theta(t), "item6_high_response": e["high_end_corporate_response"]}
    for dname, di in (("d_central", 1), ("d_high", 2)):
        scen = (di, r_i_theta(t))
        rd = {end: sum(v * (rate(level_of(k), scen) / RC - 1) for k, v in lines[end].items()) for end in ("low", "high")}
        rec = {"rate_state_local": rate("state_local", scen), "rate_federal": rate("federal", scen)}
        for which in ("set", "cash"):
            base = check["arms"]["B"][which]
            band = []
            for i, end in enumerate(("low", "high")):
                i6 = e[which][end]["total_bn"]
                band.append(base[i] + rd[end] + i6)
                theta_rows.append({"theta_name": name, "theta": round(t, 4), "r_i": round(r_i_theta(t), 6), "d": dname,
                                   "which": which, "end": end, "rate_state_local": round(rec["rate_state_local"], 6),
                                   "rate_federal": round(rec["rate_federal"], 6), "rate_delta_bn": round(rd[end], 4),
                                   "item6_response": 1 if end == "low" else round(e["high_end_corporate_response"], 4),
                                   "item6_delta_bn": round(i6, 4), "paired_delta_bn": round(rd[end] + i6, 4),
                                   "cost_bn": round(band[-1], 4)})
            rec[which] = {"rate_delta_bn": [rd["low"], rd["high"]], "item6_delta_bn": [e[which]["low"]["total_bn"], e[which]["high"]["total_bn"]],
                          "band_bn": band, "band_printed": [round(x, 1) for x in band]}
        pairing[name][dname] = rec
# the unpaired scenarios are the theta-0 and theta-1 rate legs
for i, end in enumerate(("low", "high")):
    assert abs(pairing["zero"]["d_central"]["set"]["rate_delta_bn"][i] - totals[("central (d central, r_i = Baa real 2024)", end)]) < 1e-9
    assert abs(pairing["one"]["d_high"]["set"]["rate_delta_bn"][i] - totals[("high (d high, r_i = GRR measured pre-tax 2024)", end)]) < 1e-9
# The adopted reading (2026-10-24): item 6's ends are the bound over theta, so each end takes its own theta.
# Low end: item 6 at 1 means everything scales (theta = 1); high end: TP-5's 0.37 means nothing above the
# normal return scales (theta = 0). Item 6 is unchanged at both ends; only each end's rate moves.
for name, i in (("one", 0), ("zero", 1)):
    assert abs(TH["theta"][name]["set"][("low", "high")[i]]["total_bn"]) < 1e-12, "[BLOCKED] bound end moves item 6"
pairing["bound"] = {
    "rule": "low end theta = 1 (item 6 response 1), high end theta = 0 (item 6 response 0.37); d central",
    "theta_by_end": [1.0, 0.0],
    "rate_state_local_by_end": [pairing["one"]["d_central"]["rate_state_local"], pairing["zero"]["d_central"]["rate_state_local"]],
    "rate_state_local_highways_by_end": [rate("state_local_hwy", (1, r_i_theta(1.0))), rate("state_local_hwy", (1, r_i_theta(0.0)))],
    "rate_federal_by_end": [pairing["one"]["d_central"]["rate_federal"], pairing["zero"]["d_central"]["rate_federal"]],
    **{which: {"band_bn": [pairing["one"]["d_central"][which]["band_bn"][0], pairing["zero"]["d_central"][which]["band_bn"][1]],
               "rate_delta_bn": [pairing["one"]["d_central"][which]["rate_delta_bn"][0], pairing["zero"]["d_central"][which]["rate_delta_bn"][1]]}
       for which in ("set", "cash")},
}
out["theta_pairing"] = pairing
with open(OUT / "theta_pairing.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(theta_rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(theta_rows)
(OUT / "rate_model.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps(out, indent=1))
