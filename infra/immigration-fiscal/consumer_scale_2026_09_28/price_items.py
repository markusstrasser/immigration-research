"""Consumer-side scale benefits of the Mexican-origin union for other US residents, 2024 $.

Four items, each with and without the 40.9m CPS 2025 Mexican-origin union (absolute) and against as
many average residents (normalized): grocery variety from city size (Handbury & Weinstein), grocery
product mix from city income (Handbury 2021), fixed-cost spreading in private network industries,
and cross-group media variety (Waldfogel). Sign convention: cost to others positive, benefit negative.
Parameters and their evidence tags are written to derived/inputs.csv.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/consumer_scale_2026_09_28/price_items.py
"""
from __future__ import annotations

import csv
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "derived"
CE_SRC = ROOT / "infra/immigration-fiscal/consumption_key_2026_09_24/_cache/sources"
AREAS = ROOT / "infra/immigration-fiscal/scale_spillovers_2026_09_23/derived/area_measures_cbsa.csv"
POP = ROOT / "infra/immigration-fiscal/crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv"
PUBLISHED = ROOT / "infra/immigration-fiscal/consumer_price_benefit_2026_09_18/derived/cex_detail_all.csv"  # CE 2024 all-CU means
FILES = ["241x", "242", "243", "244", "251"]
FMLI_SUMMARY = {"food_home": "FDHOME", "electricity": "ELCTRC", "natural_gas": "NTLGAS",
                "telephone": "TELEPH", "reading": "READ"}
MTBI_UCC = {"cable_satellite_tv": [270310], "internet": [690114]}
MEX_HORREF1 = [1, 2, 3]  # Mexican, Mexican-American, Chicano (as in consumption_key_2026_09_24)

# (name, low, central, high, tag). "low" is the most favourable to the group (largest benefit).
P = {
    # Handbury & Weinstein, NBER w17067 Table 6 col 9: variety-adjusted exact price index on ln(pop).
    "hw_beta": (-0.011 - 1.96 * 0.0036, -0.011, -0.011 + 1.96 * 0.0036,
                "SOURCE: HW w17067 Table 6 col 9, -0.011 (s.e. 0.0036); low/high = 95% CI"),
    # Handbury 2021 (NBER w26574) Table 4 col 2, local prices.
    "h21_beta1": (0.10 * 1.96 - 0.042, -0.042, -0.042 - 1.96 * 0.10,
                  "SOURCE: Handbury w26574 Table 4 col 2, ln(per-capita income) -0.042 (0.10); low/high = 95% CI"),
    "h21_beta2": (-0.15, -0.15, -0.15, "SOURCE: Handbury w26574 Table 4 col 2, x demeaned ln(HH income) -0.15 (0.039)"),
    "h21_beta3": (-0.0095, -0.0095, -0.0095, "SOURCE: Handbury w26574 Table 4 col 2, ln(pop) -0.0095 (0.018)"),
    "h21_beta4": (-0.011, -0.011, -0.011, "SOURCE: Handbury w26574 Table 4 col 2, ln(pop) x demeaned ln(HH income) -0.011 (0.0072)"),
    # Long-run share of the bill that does not scale with customers at fixed consumption per customer.
    "fixed_share_energy": (0.0826, 0.02, 0.0,
                           "SOURCE: Roberts 1986 Land Econ: +1% output and customers -> +0.98% total cost (central 0.02); "
                           "Farsi et al. 2007 Energy Econ Table 6 scale economies 0.94 (CI 0.80-1.09): high 1-1/1.09, low 0"),
    "fixed_share_telecom": (0.09, 0.04, 0.015,
                            "INFERENCE: per-location wireline cost falls 0.06-0.18 per ln unit of household density "
                            "(Cartesian/ACA Connects 2021 table from the FBA 2019 model) x passing-plant share of the bill 0.25-0.5 (assumed)"),
    # Waldfogel radio: other-group effect relative to own-group effect.
    "media_r": (0.46, 0.097, -0.83,
                "SOURCE: Waldfogel w7391: listening 0.017/0.175 (central); non-Hispanic-targeted stations "
                "-2.561/3.089 = -0.83 (high); station-ratio upper 95% (-2.561+1.96*2.031)/3.089 = 0.46 (low)"),
    "media_sigma": (3.0, 3.0, 3.0, "INFERENCE: assumed elasticity of substitution among local media titles"),
}
HANDBURY_INCOME_LEVELS = [25_000, 35_000, 50_000, 70_000, 95_000, 125_000, 160_000, 200_000]  # w26574 Table 4 notes


def cpi_annual(path: Path, year: int) -> float:
    data = json.loads(path.read_text())["Results"]["series"][0]["data"]
    months = [float(d["value"]) for d in data if int(d["year"]) == year and d["period"] != "M13"]
    assert len(months) == 12, (year, len(months))
    return sum(months) / 12


def read_ce() -> pd.DataFrame:
    frames = []
    with zipfile.ZipFile(CE_SRC / "intrvw24.zip") as z:
        for q in FILES:
            cols = ["NEWID", "FINLWT21", "HORREF1", "FAM_SIZE", "FINCBTXM"]
            cols += [f"{v}{s}" for v in FMLI_SUMMARY.values() for s in ("PQ", "CQ")]
            f = pd.read_csv(z.open(f"intrvw24/fmli{q}.csv"), usecols=cols).set_index("NEWID")
            m = pd.read_csv(z.open(f"intrvw24/mtbi{q}.csv"), usecols=["NEWID", "UCC", "COST"])
            for name, uccs in MTBI_UCC.items():
                f[name] = 4 * m[m.UCC.isin(uccs)].groupby("NEWID").COST.sum().reindex(f.index).fillna(0.0)
            for name, v in FMLI_SUMMARY.items():
                f[name] = 4 * (f[f"{v}PQ"].fillna(0) + f[f"{v}CQ"].fillna(0))
            frames.append(f)
    d = pd.concat(frames)
    d["mex"] = d.HORREF1.isin(MEX_HORREF1)
    return d


def main() -> None:
    OUT.mkdir(exist_ok=True)
    pop = pd.read_csv(POP).set_index("group")
    n_group = float(pop.loc["union", "all_ages"])
    ce = read_ce()
    cats = list(FMLI_SUMMARY) + list(MTBI_UCC)
    w = ce.FINLWT21

    def per_person(mask: pd.Series) -> dict[str, float]:
        persons = (w[mask] * ce.FAM_SIZE[mask]).sum()
        return {c: float((w[mask] * ce.loc[mask, c]).sum() / persons) for c in cats}

    pp_all, pp_mex = per_person(ce.index == ce.index), per_person(ce.mex)
    per_cu_all = {c: float((w * ce[c]).sum() / w.sum()) for c in cats}
    # Food at home is filled in only ~20% of Interview records (one interview per CU), and Interview reading
    # misses Diary purchases: take the level from the published integrated table and only the group/all
    # ratio from the microdata (food: among reporting CUs).
    pub = pd.read_csv(PUBLISHED, header=None, names=["row", "item", "mean"]).set_index("item")["mean"]
    cu_size = float((w * ce.FAM_SIZE).sum() / w.sum())
    for c, label in (("food_home", "Food at home"), ("reading", "Reading")):
        mask = ce[c] > 0 if c == "food_home" else ce[c] == ce[c]
        pp_rep = lambda mm: float((w * ce[c])[mm].sum() / (w * ce.FAM_SIZE)[mm].sum())
        ratio = pp_rep(mask & ce.mex) / pp_rep(mask)
        per_cu_all[c] = float(pub[label])
        pp_all[c] = per_cu_all[c] / cu_size
        pp_mex[c] = pp_all[c] * ratio

    a = pd.read_csv(AREAS)
    n_other = float(a.other_persons.sum())
    assert abs(a.group_persons.sum() - n_group) < 1.0, "area file must carry the whole union"
    s_bar = n_group / (n_group + n_other)
    # Others' per-person spending: all-person total less the group's, spread over other persons.
    pp_other = {c: (pp_all[c] * (n_group + n_other) - pp_mex[c] * n_group) / n_other for c in cats}

    rows_ce = [{"category": c, "per_cu_all_usd": round(per_cu_all[c], 2), "per_person_all_usd": round(pp_all[c], 2),
                "per_person_mexican_ref_usd": round(pp_mex[c], 2), "ratio_mex_to_all": round(pp_mex[c] / pp_all[c], 4),
                "group_total_bn": round(pp_mex[c] * n_group / 1e9, 4),
                "others_total_bn": round(pp_other[c] * n_other / 1e9, 4)} for c in cats]

    # --- 1. Grocery variety from city size (HW) --------------------------------------------------------
    s = a.group_persons / (a.group_persons + a.other_persons)
    S = a.other_persons * pp_other["food_home"]  # others' grocery spending by area
    exposure = float((S * -np.log1p(-s)).sum())  # sum of spending x log population lost
    exposure_avg = float(S.sum() * -np.log1p(-s_bar))

    def scale_cost(beta: float, expo: float) -> float:  # presence lowers the index by |beta| x log gain
        return beta * expo / 1e9

    # --- 2. Grocery product mix from city income (Handbury 2021) ------------------------------------
    cpi12 = cpi_annual(CE_SRC / "bls_cpi_u_2003_2012.json", 2012)
    cpi24 = cpi_annual(CE_SRC / "bls_cpi_u_2015_2024.json", 2024)
    y_tilde = float(np.mean(np.log(HANDBURY_INCOME_LEVELS)))
    oth = ~ce.mex
    inc12 = (ce.FINCBTXM[oth] * cpi12 / cpi24).clip(HANDBURY_INCOME_LEVELS[0], HANDBURY_INCOME_LEVELS[-1])
    fw = w[oth] * ce.food_home[oth]
    m_dev = float((fw * (np.log(inc12) - y_tilde)).sum() / fw.sum())
    y_with = (a.group_earnings + a.other_earnings) / (a.group_persons + a.other_persons)
    dy = np.log((a.other_earnings / a.other_persons) / y_with)  # rise in ln earnings per head without the group
    comp_expo = float((S * dy).sum())

    def comp_cost(beta1: float) -> float:  # lnP_with - lnP_without = -(b1 + b2 m) dy
        return -(beta1 + P["h21_beta2"][1] * m_dev) * comp_expo / 1e9

    # --- 3. Network fixed-cost spreading -------------------------------------------------------------
    networks = {"electricity": "fixed_share_energy", "natural_gas": "fixed_share_energy",
                "telephone": "fixed_share_telecom", "internet": "fixed_share_telecom",
                "cable_satellite_tv": "fixed_share_telecom"}

    # --- 4. Media cross-group variety ----------------------------------------------------------------
    sigma = P["media_sigma"][1]
    b_identical = pp_other["reading"] * n_other * ((1 - s_bar) ** (-1 / (sigma - 1)) - 1) / 1e9

    items: list[dict] = []

    def add(item, measure, lo, ce_, hi, level, dc, note):
        vals = sorted([lo, hi])
        items.append({"item": item, "group": "mexican_origin", "measure": measure, "low_bn": round(vals[0], 4),
                      "central_bn": round(ce_, 4), "high_bn": round(vals[1], 4),
                      "per_member_usd": round(ce_ * 1e9 / n_group, 2), "evidence_level": level,
                      "double_count_with": dc, "method_note": note})

    hw = [scale_cost(b, exposure) for b in P["hw_beta"][:3]]
    hw_avg = [scale_cost(b, exposure_avg) for b in P["hw_beta"][:3]]
    dc_groc = "restaurant_variety_market_size (food away from home, excluded here); consumer_price_benefit (services only); CRY premia (wages)"
    add("grocery_variety_scale", "absolute", *hw, "measured cross-city elasticity (49 cities, 2005); not causal",
        dc_groc, f"others' food-at-home spending by CBSA x HW beta x -ln(1-s); spending-weighted -ln(1-s) = {exposure / S.sum():.4f}")
    add("grocery_variety_scale", "normalized", *[g - v for g, v in zip(hw, hw_avg)],
        "measured cross-city elasticity; not causal", dc_groc,
        f"absolute minus 40.9m average residents spread pro rata (-ln(1-{s_bar:.4f}) = {-np.log1p(-s_bar):.4f})")
    comp = [comp_cost(b) for b in P["h21_beta1"][:3]]
    add("grocery_product_mix_income", "absolute", *comp, "measured cross-city relation; beta1 insignificant; sign uncertain",
        "grocery_variety_scale (separate regressor)", f"others' food-at-home spending x -(b1 + b2 x {m_dev:.3f}) x rise in ln earnings per head "
        f"without the group; spending-weighted rise {comp_expo / S.sum():.4f}")
    add("grocery_product_mix_income", "normalized", *comp, "measured cross-city relation; sign uncertain",
        "grocery_variety_scale", "equal to absolute: average residents leave per-capita income unchanged")
    net_abs = {k: [0.0, 0.0, 0.0] for k in ("absolute", "normalized")}
    for cat, key in networks.items():
        f = P[key][:3]
        g_abs = [-fi * pp_mex[cat] * n_group / 1e9 for fi in f]
        g_norm = [-fi * (pp_mex[cat] - pp_all[cat]) * n_group / 1e9 for fi in f]
        for i in range(3):
            net_abs["absolute"][i] += g_abs[i]
            net_abs["normalized"][i] += g_norm[i]
        lvl = ("measured cost-function elasticities (long run, customer density)" if key == "fixed_share_energy"
               else "modelled: density-cost table x assumed plant share")
        dc = "none: private utilities are outside the fiscal account; public power/water/transit are in enterprises D"
        add(f"network_fixed_cost_{cat}", "absolute", *g_abs, lvl, dc,
            f"-(fixed share) x group CE spending ${pp_mex[cat]:.0f}/person x 40.9m")
        add(f"network_fixed_cost_{cat}", "normalized", *g_norm, lvl, dc,
            f"-(fixed share) x (group - average per-person spending, ${pp_mex[cat]:.0f} - ${pp_all[cat]:.0f}) x 40.9m")
    media = [-r * b_identical for r in P["media_r"][:3]]
    add("media_cross_group_variety", "absolute", *media, "measured cross-group ratio (radio); valuation modelled",
        "cultural_output_2026_09_19 (no dollar line); restaurant_variety_composition (cuisine)",
        f"-r x identical-taste gain; identical-taste gain = others' reading spending x ((1-{s_bar:.4f})^(-1/(sigma-1))-1) = {b_identical:.4f}bn")
    add("media_cross_group_variety", "normalized", *[(1 - r) * b_identical for r in P["media_r"][:3]],
        "measured cross-group ratio; valuation modelled", "as absolute", "(1 - r) x identical-taste gain: average residents have r = 1")

    tot = {}
    for meas in ("absolute", "normalized"):
        sub = [r for r in items if r["measure"] == meas]
        tot[meas] = [sum(r[k] for r in sub) for k in ("low_bn", "central_bn", "high_bn")]
    add("total_consumer_scale", "absolute", *tot["absolute"], "stacked arms, not an interval", "see rows",
        "sum of rows above (low and high are row-wise extremes)")
    add("total_consumer_scale", "normalized", *tot["normalized"], "stacked arms, not an interval", "see rows",
        "sum of rows above")

    # Arms beside the items (not added).
    h21_full_scale = scale_cost(P["h21_beta3"][1] + P["h21_beta4"][1] * m_dev, exposure)
    arms = [
        {"arm": "handbury2021_population_term", "central_bn": round(h21_full_scale, 4),
         "note": "beta3 + beta4 x m instead of HW beta; conditional on per-capita income; beta3 s.e. 0.018"},
        {"arm": "handbury2021_both_terms", "central_bn": round(h21_full_scale + comp[1], 4),
         "note": "population term + income term, Table 4 col 2"},
        {"arm": "grocery_scale_on_group_spending", "central_bn": round(hw[1] * pp_mex["food_home"] / pp_other["food_home"], 4),
         "note": "HW scaled by group/other per-person grocery spending (variety follows spending, not heads)"},
        # Short-run (5-year) fixed-cost spreading, LBNL/Brattle 2025: +10% statewide load -> -0.6 c/kWh on the
        # all-sector average. Residential price and US retail sales are TRAINING-DATA (EIA 2024, ~16.5 c/kWh, ~4,100 TWh).
        {"arm": "electricity_short_run_lbnl", "central_bn": round(
            -0.006 / 0.10 * (pp_mex["electricity"] * n_group / 0.165 / 4.1e12)
            * (4.1e12 - pp_mex["electricity"] * n_group / 0.165) / 1e9, 4),
         "note": "not the long-run frame: LBNL -0.6 c/kWh per 10% load x group residential load share x others' kWh; "
                 "residential-only coefficient smaller and insignificant"},
        {"arm": "media_sigma_5", "central_bn": round(-P["media_r"][1] * pp_other["reading"] * n_other
                                                     * ((1 - s_bar) ** (-1 / 4) - 1) / 1e9, 4),
         "note": "media central with sigma 5"},
    ]
    inputs = [{"parameter": k, "low": v[0], "central": v[1], "high": v[2], "tag": v[3]} for k, v in P.items()]
    inputs += [
        {"parameter": "n_group", "low": n_group, "central": n_group, "high": n_group, "tag": "DATA: target_population_cps2025.csv union all_ages"},
        {"parameter": "n_other", "low": n_other, "central": n_other, "high": n_other, "tag": "DATA: area_measures_cbsa.csv other_persons sum"},
        {"parameter": "s_bar", "low": s_bar, "central": s_bar, "high": s_bar, "tag": "CALCULATION"},
        {"parameter": "cu_size_all", "low": cu_size, "central": cu_size, "high": cu_size, "tag": "CALCULATION: CE 2024 Interview FINLWT21-weighted FAM_SIZE"},
        {"parameter": "food_home_per_cu", "low": per_cu_all["food_home"], "central": per_cu_all["food_home"], "high": per_cu_all["food_home"],
         "tag": "DATA: CE 2024 published all-CU mean (cex_detail_all.csv 'Food at home'); group/all ratio from Interview reporters"},
        {"parameter": "reading_per_cu", "low": per_cu_all["reading"], "central": per_cu_all["reading"], "high": per_cu_all["reading"],
         "tag": "DATA: CE 2024 published all-CU mean (cex_detail_all.csv 'Reading'); group/all ratio from Interview microdata"},
        {"parameter": "m_dev", "low": m_dev, "central": m_dev, "high": m_dev,
         "tag": "CALCULATION: CE 2024 non-Mexican-ref CUs, food-at-home-weighted mean of ln(income, 2012$, clipped 25k-200k) - mean ln of Handbury's eight levels [INFERENCE: demeaning reference]"},
        {"parameter": "cpi_2012", "low": cpi12, "central": cpi12, "high": cpi12, "tag": "DATA: BLS CPI-U json in consumption_key _cache"},
        {"parameter": "cpi_2024", "low": cpi24, "central": cpi24, "high": cpi24, "tag": "DATA: BLS CPI-U json in consumption_key _cache"},
        {"parameter": "exposure_share", "low": exposure / S.sum(), "central": exposure / S.sum(), "high": exposure / S.sum(),
         "tag": "CALCULATION: others' grocery-spending-weighted -ln(1-s)"},
        {"parameter": "comp_expo_share", "low": comp_expo / S.sum(), "central": comp_expo / S.sum(), "high": comp_expo / S.sum(),
         "tag": "CALCULATION: others' grocery-spending-weighted rise in ln earnings per head without the group"},
        {"parameter": "b_identical_bn", "low": b_identical, "central": b_identical, "high": b_identical, "tag": "CALCULATION"},
    ]
    for name, rows in (("items", items), ("ce_spending", rows_ce), ("arms", arms), ("inputs", inputs)):
        with open(OUT / f"{name}.csv", "w", newline="") as fh:
            wr = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
            wr.writeheader()
            wr.writerows(rows)
    print(pd.DataFrame(rows_ce).to_string(index=False))
    print(pd.DataFrame(items)[["item", "measure", "low_bn", "central_bn", "high_bn", "per_member_usd"]].to_string(index=False))
    print(pd.DataFrame(arms).to_string(index=False))
    print(f"s_bar={s_bar:.4f} exposure_share={exposure / S.sum():.4f} comp_share={comp_expo / S.sum():.4f} m={m_dev:.4f} "
          f"cpi12={cpi12:.3f} cpi24={cpi24:.3f} others_food_bn={S.sum() / 1e9:.1f}")


if __name__ == "__main__":
    main()
