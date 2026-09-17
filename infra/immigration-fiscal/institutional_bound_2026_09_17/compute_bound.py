#!/usr/bin/env python3
"""Bound the effect of omitted public institutional costs on the all-age fiscal gaps.

Inputs : derived/acs_cells.csv (from pull_acs.py), derived/gate_raw.json,
         ../acs_institutional_2026_09_16/acs_institutional_rates.csv (gate reference),
         ../all_age_ledger_2026_09_17/derived/estimates.csv (stored CPS gaps).
Outputs: derived/institutional_bound.csv, derived/institutional_rates.csv, derived/audit.json
"""
import csv, json, pathlib
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
DER = HERE / "derived"

# ---- cost parameters (all fetched 2026-09-17; provenance in RESULT.md) --------------
PRISON = 60989.0          # USAFacts / BJS+Census: median state spending per prisoner, 2023
JAIL_ALT = 47057.0        # Vera "The Price of Jails": mean annual cost per jail inmate (35 jurisdictions)
NF_TOTAL_PER_RES = 147e9 / 1.2e6           # KFF: $147bn institutional LTC 2023 / 1.2M residents Jul-2024
NF_PUBLIC_SHARE = 0.63 + 0.14              # KFF/CASPER 2025 resident primary payer: Medicaid + Medicare
NF_PUBLIC = NF_TOTAL_PER_RES * NF_PUBLIC_SHARE
NF_PUBLIC_MEDICAID_ONLY = NF_TOTAL_PER_RES * 0.44   # KFF: Medicaid paid 44% of institutional LTC, 2023

BANDS = ["0_17", "18_24", "25_34", "35_44", "45_54", "55_64", "65_74", "75_99"]
OLD = {"65_74", "75_99"}
TARGETS = ["mexico_born", "usborn_mexican", "mexican_total"]
REFS = ["native_nh_white", "all_natives"]

# ---- load ACS cells ----------------------------------------------------------------
N = defaultdict(float)      # (group, band) -> total population
I = defaultdict(float)      # (group, band) -> institutional (TYPEHUGQ=2)
IM = defaultdict(float)     # (group, band) -> institutional men
for r in csv.DictReader(open(DER / "acs_cells.csv")):
    g, b, w = r["group"], r["band"], float(r["weighted"])
    N[(g, b)] += w
    if r["typehugq"] == "2":
        I[(g, b)] += w
        if r["sex"] == "1":
            IM[(g, b)] += w
for b in BANDS:                              # synthetic pooled Mexican-origin target
    for D in (N, I, IM):
        D[("mexican_total", b)] = D[("mexico_born", b)] + D[("usborn_mexican", b)]

# ---- cost per institutionalized person ---------------------------------------------
def cost(group, band, arm, nf_public):
    if band in OLD:
        return nf_public
    if arm == "adverse":
        return PRISON
    male_share = IM[(group, band)] / I[(group, band)] if I[(group, band)] else 0.0
    return PRISON * male_share

def C(group, band, arm, nf_public):
    return I[(group, band)] * cost(group, band, arm, nf_public)

# ---- age standard: native NH white ACS age shares ----------------------------------
white_tot = sum(N[("native_nh_white", b)] for b in BANDS)
S = {b: N[("native_nh_white", b)] / white_tot for b in BANDS}

rows = []
for arm, nf in (("adverse", NF_PUBLIC), ("moderate", NF_PUBLIC),
                ("adverse_nf_medicaid_only", NF_PUBLIC_MEDICAID_ONLY),
                ("moderate_nf_medicaid_only", NF_PUBLIC_MEDICAID_ONLY)):
    base_arm = arm.split("_nf_")[0]
    for g in TARGETS:
        cost_g = sum(C(g, b, base_arm, nf) for b in BANDS)
        pop_g = sum(N[(g, b)] for b in BANDS)
        for r in REFS:
            d_gap = -sum(C(g, b, base_arm, nf)
                         - (N[(g, b)] / N[(r, b)]) * C(r, b, base_arm, nf) for b in BANDS)
            d_std = -sum(S[b] * (C(g, b, base_arm, nf) / N[(g, b)]
                                 - C(r, b, base_arm, nf) / N[(r, b)]) for b in BANDS)
            rows.append(dict(arm=arm, target=g, reference=r,
                             target_population=round(pop_g, 1),
                             target_institutional_cost_bn=round(cost_g / 1e9, 3),
                             target_institutional_cost_per_person=round(cost_g / pop_g, 1),
                             delta_age_matched_gap_bn=round(d_gap / 1e9, 3),
                             delta_age_matched_gap_per_target_person=round(d_gap / pop_g, 1),
                             delta_standardized_per_person=round(d_std, 1)))

with open(DER / "institutional_bound.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

# ---- institutional rates per 1,000 --------------------------------------------------
rate_rows = []
for g in TARGETS + REFS:
    for b in BANDS:
        n, i, im = N[(g, b)], I[(g, b)], IM[(g, b)]
        rate_rows.append(dict(group=g, band=b, population=round(n, 1), institutional=round(i, 1),
                              rate_per_1000=round(1000 * i / n, 3) if n else None,
                              male_share_of_institutional=round(im / i, 4) if i else None,
                              white_age_share=round(S[b], 5)))
with open(DER / "institutional_rates.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rate_rows[0])); w.writeheader(); w.writerows(rate_rows)

# ---- gates --------------------------------------------------------------------------
stored = None
for r in csv.DictReader(open(HERE.parent / "acs_institutional_2026_09_16/acs_institutional_rates.csv")):
    if r["year"] == "2024" and r["group"] == "Mexican" and r["nativity"] == "native":
        stored = float(r["institutional"])
fresh = json.load(open(DER / "gate_raw.json"))["gate_fresh_institutional_usborn_mexican_men_18_39_2024"]

stored_gaps = {}
for r in csv.DictReader(open(HERE.parent / "all_age_ledger_2026_09_17/derived/estimates.csv")):
    if r["scenario"] == "all_age_shared" and r["target"] == "mexican_observed_total":
        if r["matching"] == "age_band" and r["metric"] == "gap_total":
            stored_gaps[f"gap_total_vs_{r['reference']}_bn"] = round(float(r["estimate"]) / 1e9, 3)
        if r["metric"] == "absolute_total" and not r["reference"]:
            stored_gaps["absolute_total_bn"] = round(float(r["estimate"]) / 1e9, 3)
        if r["matching"] == "common_age" and r["metric"] == "standardized_gap_per_person":
            stored_gaps[f"std_gap_pp_vs_{r['reference']}"] = round(float(r["estimate"]), 1)

audit = {
    "acs_year": 2024, "acs_source": "Census API ACS 1-year PUMS tabulate endpoint",
    "gate1_stored_acs_institutional_2026_09_16": stored,
    "gate1_fresh_pull": fresh,
    "gate1_pass": stored == fresh,
    "gate2_mexican_total_equals_sum_of_parts": all(
        abs(N[("mexican_total", b)] - N[("mexico_born", b)] - N[("usborn_mexican", b)]) < 1e-6 for b in BANDS),
    "gate3_self_reference_delta_zero": max(
        abs(-sum(C("native_nh_white", b, "adverse", NF_PUBLIC)
                 - (N[("native_nh_white", b)] / N[("native_nh_white", b)]) * C("native_nh_white", b, "adverse", NF_PUBLIC)
                 for b in BANDS)), 0.0),
    "parameters": {"prison_annual_per_person": PRISON, "jail_alt_not_used_in_headline": JAIL_ALT,
                   "nf_total_per_resident_year": round(NF_TOTAL_PER_RES, 1),
                   "nf_public_share_residents": NF_PUBLIC_SHARE,
                   "nf_public_per_resident_year": round(NF_PUBLIC, 1),
                   "nf_public_medicaid_only_per_resident_year": round(NF_PUBLIC_MEDICAID_ONLY, 1)},
    "white_age_shares": {b: round(S[b], 5) for b in BANDS},
    "stored_cps_gaps_all_age_shared_mexican_observed_total": stored_gaps,
}
json.dump(audit, open(DER / "audit.json", "w"), indent=1)

print(f"[gate1] stored={stored} fresh={fresh} pass={audit['gate1_pass']}")
print(f"[params] prison={PRISON:,.0f} nf_public={NF_PUBLIC:,.0f} (share {NF_PUBLIC_SHARE:.2f})")
print(f"[stored] {stored_gaps}")
for r in rows:
    if r["arm"] in ("adverse", "moderate"):
        print(f"  {r['arm']:9s} {r['target']:16s} vs {r['reference']:16s} "
              f"cost={r['target_institutional_cost_bn']:8.2f}bn  dgap={r['delta_age_matched_gap_bn']:8.2f}bn  "
              f"dstd={r['delta_standardized_per_person']:9.1f}/person")

# ---- sign-flip headroom: uniform cost multiplier m applied to every institutionalized person ----
# Deltas and the target cost are linear in the cost parameters, so the multiplier that would drive
# each quantity to zero is read off directly.
head = {}
for g in TARGETS:
    for r in REFS:
        for arm in ("adverse", "moderate"):
            d = -sum(C(g, b, arm, NF_PUBLIC) - (N[(g, b)] / N[(r, b)]) * C(r, b, arm, NF_PUBLIC) for b in BANDS)
            key = f"{arm}|{g}|vs_{r}"
            gap = stored_gaps[f"gap_total_vs_{'third_plus_nh_white' if r=='native_nh_white' else 'all_native'}_bn"] * 1e9
            # gap + m*d = 0  ->  m = -gap/d   (only meaningful when d moves toward zero)
            head[key] = round(-gap / d, 1) if d else None
cost_tot = {arm: {g: sum(C(g, b, arm, NF_PUBLIC) for b in BANDS) for g in TARGETS} for arm in ("adverse", "moderate")}
head_abs = {arm: round(stored_gaps["absolute_total_bn"] * 1e9 / cost_tot[arm]["mexican_total"], 2)
            for arm in ("adverse", "moderate")}
audit["signflip_cost_multiplier_needed_for_age_matched_gap"] = head
audit["signflip_cost_multiplier_needed_for_absolute_50_2bn"] = head_abs
audit["implied_cost_per_institutionalized_person_year_to_flip_absolute"] = {
    arm: round(head_abs[arm] * PRISON, 0) for arm in head_abs}
json.dump(audit, open(DER / "audit.json", "w"), indent=1)
print("[headroom gap multipliers]", json.dumps(head, indent=1))
print("[headroom absolute multipliers]", head_abs, "implied $/person-yr",
      audit["implied_cost_per_institutionalized_person_year_to_flip_absolute"])
