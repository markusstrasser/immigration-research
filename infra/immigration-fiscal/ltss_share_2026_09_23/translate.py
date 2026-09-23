"""Union shares of Medicaid LTSS dollars and the effect of charging LTSS by them.

1. Shares. CMS's CY2023 TAF tables give each state's Hispanic dollars by LTSS category. Each
   state's Hispanic dollars are turned into union dollars with the ACS 2024 union-per-Hispanic
   ratio of a proxy population (acs_factors.py), shrunk toward the state's broad-population ratio
   when the state has few Hispanic records (K = 50 records). California's IHSS, absent from TAF,
   is added from the CMS-64 FMR at the Latino share of Medi-Cal HCBS recipients (CHCF, 2022).
2. Dollars. CY2023 LTSS dollars (TAF + IHSS) are carried to CY2024 at BEA's Medicaid growth
   (T3.12 lines 33+34, 2024 / 2023) and carved out of the $954.2bn line. The rest stays on the
   MEPS key, rebuilt without home-health dollars (meps_hh_key.py).
3. Effect. change = sum_c L_c (s_c - hf k) + R hf (k_R - k), where L_c is the carved-out dollars,
   s_c the union share, R the remainder, k_R its key; negative = the account over-charges.
   Combined with the medical-ethnicity lane (its ratio f applies to the community remainder only):
   combined = its five-line change + change + (f - 1) hf (R k_R - B k).
Every variant is run one at a time and over the full grid of plausible choices.
Writes derived/shares.csv, derived/shares_by_year.csv, derived/effects.csv, derived/combined.csv,
derived/summary.json.
Run from the repo root after taf_tables.py, acs_factors.py, fmr.py, meps_hh_key.py, gate.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 \
      infra/immigration-fiscal/ltss_share_2026_09_23/translate.py
"""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
DER = HERE / "derived"
MED = FISCAL / "medical_ethnicity_pooled_2026_09_23/derived"
BEA = Path.home() / "research-data/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx"
BEA_SHA = "69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e"
FIPS = {"Alabama": 1, "Alaska": 2, "Arizona": 4, "Arkansas": 5, "California": 6, "Colorado": 8,
        "Connecticut": 9, "Delaware": 10, "District of Columbia": 11, "Florida": 12, "Georgia": 13,
        "Hawaii": 15, "Idaho": 16, "Illinois": 17, "Indiana": 18, "Iowa": 19, "Kansas": 20,
        "Kentucky": 21, "Louisiana": 22, "Maine": 23, "Maryland": 24, "Massachusetts": 25,
        "Michigan": 26, "Minnesota": 27, "Mississippi": 28, "Missouri": 29, "Montana": 30,
        "Nebraska": 31, "Nevada": 32, "New Hampshire": 33, "New Jersey": 34, "New Mexico": 35,
        "New York": 36, "North Carolina": 37, "North Dakota": 38, "Ohio": 39, "Oklahoma": 40,
        "Oregon": 41, "Pennsylvania": 42, "Rhode Island": 44, "South Carolina": 45,
        "South Dakota": 46, "Tennessee": 47, "Texas": 48, "Utah": 49, "Vermont": 50, "Virginia": 51,
        "Washington": 53, "West Virginia": 54, "Wisconsin": 55, "Wyoming": 56}
K = 50  # shrinkage weight, in Hispanic ACS records
BROAD = {"inst65": "all65", "comm_adl_65": "all65", "comm_adl": "all", "comm_adl_u65": "all",
         "comm_cog_u65": "all"}
# CHCF / ATI Advisory (Oct 2025), p. 2 Figure 3: Latino/x 31%, Unknown 7% of ALW, CBAS, HCBA,
# IHSS and MSSP recipients, 2022 (IHSS is 92% of their enrollment, p. 1).
IHSS_LATINO = {"reported_31": 0.31, "unknown_spread": 0.31 / 0.93}
CPS_UNION, CPS_CIV = 40896574.15235156, 336727803.00001377  # full_account_spending README
CATS = ["NF", "ICF", "MHF", "HCBS"]


def bea_growth():
    if hashlib.sha256(BEA.read_bytes()).hexdigest() != BEA_SHA:
        raise SystemExit("[BLOCKED] BEA workbook changed")
    rows = list(openpyxl.load_workbook(BEA, read_only=True, data_only=True)["T31200-A"].values)
    head = [r for r in rows if r[0] == "Line"][0]
    col = {str(x): i for i, x in enumerate(head)}
    line = {int(r[0]): r for r in rows if str(r[0]).isdigit()}
    if not (line[33][1].strip() == "Medicaid" and line[34][1].strip().startswith("Other medical care")):
        raise SystemExit("[BLOCKED] BEA line labels changed")
    b23 = (line[33][col["2023"]] + line[34][col["2023"]]) / 1e3
    b24 = (line[33][col["2024"]] + line[34][col["2024"]]) / 1e3
    return b23, b24


def factors():
    """State union-per-Hispanic ratios by proxy population, raw and shrunk."""
    st = pd.read_csv(DER / "acs_state_factors_2024.csv")
    nat = pd.read_csv(DER / "acs_shares_2024.csv").query("quantity == 'f_union_per_hisp'") \
        .set_index("population").value
    spread = pd.read_csv(DER / "acs_shares_2024.csv").query("quantity == 'f_union_per_hisp_generic_spread'").value.iloc[0]
    raw = st.pivot(index="STATE", columns="population", values="f")
    n = st.pivot(index="STATE", columns="population", values="hisp_records").fillna(0)
    hp = st.pivot(index="STATE", columns="population", values="hisp_persons").fillna(0)
    shrunk = pd.DataFrame(index=raw.index)
    for pop, broad in BROAD.items():
        prior = raw[broad] * nat[pop] / nat[broad]
        f = raw[pop].where(hp[pop] > 0)
        shrunk[pop] = ((n[pop] * f.fillna(0) + K * prior) / (n[pop] + K))
    shrunk["all"], shrunk["all65"] = raw["all"], raw["all65"]
    return raw, shrunk, hp, nat, spread


def main():
    taf = pd.read_csv(DER / "taf_race_ethn.csv")
    e = taf[(taf.year == 2023) & (taf.measure == "expenditures") & taf.category.isin(CATS)
            & ~taf.state.eq("National")]
    hisp = e[e.group == "hispanic"].pivot(index="state", columns="category", values="value")
    total = e.groupby(["state", "category"]).total.first().unstack()
    national = taf[(taf.year == 2023) & (taf.measure == "expenditures") & taf.state.eq("National")
                   & taf.group.eq("hispanic")].set_index("category")
    if set(hisp.index) != set(FIPS):
        raise SystemExit("[BLOCKED] state set differs from FIPS map")
    for c in CATS:  # states sum to the national row
        if abs(total[c].sum() - national.loc[c, "total"]) > 1e3 or abs(hisp[c].sum() - national.loc[c, "value"]) > 1e3:
            raise SystemExit(f"[BLOCKED] {c}: states do not sum to the national row")
    hisp.index = hisp.index.map(FIPS)
    total.index = total.index.map(FIPS)
    age = pd.read_csv(DER / "taf_age.csv")
    age = age[(age.year == 2023) & (age.measure == "expenditures") & age.state.eq("National")] \
        .pivot(index="category", columns="group", values="pct") / 100
    w65 = {c: float(age.loc[c, "age_65plus"]) for c in CATS}
    raw, fs, hp, nat, spread = factors()
    fmr = pd.read_csv(DER / "fmr_ltss_lines.csv")
    ca = fmr[(fmr.state == "California") & (fmr.group == "hcbs_pc_cfc")].groupby("fiscal_year").total_computable.sum() / 1e9
    ihss_cy2023 = 0.75 * ca[2023] + 0.25 * ca[2024]  # CY2023 = Jan-Sep of FFY2023 + Oct-Dec of FFY2024
    gate = json.loads((DER / "gate.json").read_text())
    B, hf, k = gate["medicaid_national_bn"], gate["household_pool_fraction"], gate["household_key_share"]
    rate = hf * k
    mk = json.loads((DER / "meps_hh_key.json").read_text())
    k_ex = mk["key_share"]["medicaid_ex_home_health"]
    meps_hh = mk["meps_national_medicaid_home_health_bn"]
    b23, b24 = bea_growth()
    if abs(b24 - B) > 1e-6:
        raise SystemExit("[BLOCKED] BEA 2024 line differs from the account")
    acs = pd.read_csv(DER / "acs_shares_2024.csv")
    acs_union = float(acs.query("population == 'all' and quantity == 'union'").value.iloc[0])
    acs_mcd_users = float(acs.query("population == 'inst65_mcd' and quantity == 'union'").value.iloc[0])
    cps_scale = (CPS_UNION / CPS_CIV) / acs_union

    # ---- factor choices per category -------------------------------------------------------
    hw = {a: float(age.loc["HCBS", g]) for a, g in [("u65", "age_0_20"), ("u65b", "age_21_44"), ("u65c", "age_45_64")]}
    w_u65, w_65 = sum(hw.values()), float(age.loc["HCBS", "age_65plus"])
    persons = pd.read_csv(DER / "acs_shares_2024.csv").query("quantity == 'persons'").set_index("population").value
    c_u, c_o = w_u65 / persons["comm_adl_u65"], w_65 / persons["comm_adl_65"]  # TAF $ per proxy person

    def f_nf(choice):
        inst = fs["inst65"] * (spread / nat["inst65"] if choice == "generic_spread" else 1.0)
        if choice == "all65":
            return raw["all65"]
        if choice == "inst65_only":
            return fs["inst65"]
        return w65["NF"] * inst + (1 - w65["NF"]) * fs["comm_adl_u65"]

    def f_hcbs(choice):
        if choice == "all_ages":
            return raw["all"]
        if choice == "age_weighted":
            a, b = c_u * hp["comm_adl_u65"], c_o * hp["comm_adl_65"]
            return ((a * fs["comm_adl_u65"] + b * fs["comm_adl_65"]) / (a + b)).fillna(fs["comm_adl"])
        return fs["comm_adl"]

    def f_icf(choice):
        return raw["all"] if choice == "all_ages" else fs["comm_cog_u65"]

    def f_mhf(choice):
        return fs["comm_cog_u65"] if choice == "cog_u65" else raw["all"]

    def shares(nf="blend", hc="comm_adl", icf="cog_u65", mhf="all_ages", ihss="unknown_spread",
               union="acs", national_f=False, with_ihss=True):
        f = {"NF": f_nf(nf), "HCBS": f_hcbs(hc), "ICF": f_icf(icf), "MHF": f_mhf(mhf)}
        if national_f:
            natf = {"NF": w65["NF"] * nat["inst65"] + (1 - w65["NF"]) * nat["comm_adl_u65"],
                    "HCBS": nat["comm_adl"], "ICF": nat["comm_cog_u65"], "MHF": nat["all"]}
            f = {c: pd.Series(natf[c], index=hisp.index) for c in CATS}
        scale = cps_scale if union == "cps" else 1.0
        out = {}
        for c in CATS:
            u = float((hisp[c] * f[c].reindex(hisp.index)).sum()) / 1e9
            L = float(total[c].sum()) / 1e9
            if c == "NF" and nf == "acs_medicaid_users":  # ACS-only: union share of Medicaid-covered 65+ residents
                u = L * acs_mcd_users
            if c == "HCBS" and with_ihss:
                u += ihss_cy2023 * IHSS_LATINO[ihss] * float(f["HCBS"].loc[6])
                L += ihss_cy2023
            out[c] = dict(L2023=L, union2023=u * scale, share=u * scale / L,
                          hisp_share=float(hisp[c].sum()) / 1e9 / (L - (ihss_cy2023 if c == "HCBS" and with_ihss else 0)))
        return out

    def effect(sh, growth=True, remainder="ex_home_health"):
        g = b24 / b23 if growth else 1.0
        L = {c: sh[c]["L2023"] * g for c in CATS}
        if remainder == "ex_home_health":
            R, kr = B - sum(L.values()), k_ex
            carved = L
        else:  # the brief's reading: carve out only the HCBS dollars MEPS does not record
            carved = dict(L, HCBS=L["HCBS"] - meps_hh)
            R, kr = B - sum(carved.values()), k
        parts = {c: carved[c] * (sh[c]["share"] - rate) for c in CATS}
        parts["remainder_key"] = R * hf * (kr - k)
        return dict(total=sum(parts.values()), R=R, kr=kr, L=sum(L.values()), **parts)

    # ---- central, one-at-a-time, grid -------------------------------------------------------
    central = shares()
    rows = [dict(variant="central", category=c, **v) for c, v in central.items()]
    one = {"nf=inst65_only": dict(nf="inst65_only"), "nf=generic_spread": dict(nf="generic_spread"),
           "nf=all65": dict(nf="all65"), "nf=acs_medicaid_users": dict(nf="acs_medicaid_users"), "hcbs=age_weighted": dict(hc="age_weighted"),
           "hcbs=all_ages": dict(hc="all_ages"), "icf=all_ages": dict(icf="all_ages"),
           "mhf=cog_u65": dict(mhf="cog_u65"), "ihss_latino=31%": dict(ihss="reported_31"),
           "union=cps_scaled": dict(union="cps"),
           "diagnostic: national factors": dict(national_f=True),
           "diagnostic: no IHSS": dict(with_ihss=False)}
    for name, kw in one.items():
        rows += [dict(variant=name, category=c, **v) for c, v in shares(**kw).items()]
    sh = pd.DataFrame(rows)
    sh.to_csv(DER / "shares.csv", index=False)

    eff = [dict(variant="central", **effect(central))]
    for name, kw in one.items():
        eff.append(dict(variant=name, **effect(shares(**kw))))
    eff.append(dict(variant="no growth (2023 dollars)", **effect(central, growth=False)))
    eff.append(dict(variant="brief: carve out only HCBS MEPS misses, key unchanged",
                    **effect(central, remainder="brief")))
    grid = []
    dims = dict(nf=["blend", "inst65_only", "generic_spread", "all65", "acs_medicaid_users"], hc=["comm_adl", "age_weighted", "all_ages"],
                icf=["cog_u65", "all_ages"], mhf=["all_ages", "cog_u65"], ihss=["unknown_spread", "reported_31"],
                union=["acs", "cps"])
    for combo in itertools.product(*dims.values()):
        s_ = shares(**dict(zip(dims, combo)))
        for growth in (True, False):
            for rem in ("ex_home_health", "brief"):
                grid.append(effect(s_, growth, rem)["total"])
    eff = pd.DataFrame(eff)
    eff.to_csv(DER / "effects.csv", index=False)

    # ---- stability: TAF-only union shares by year, central factors ----------------------------
    fc = {"NF": f_nf("blend"), "HCBS": f_hcbs("comm_adl"), "ICF": f_icf("cog_u65"), "MHF": f_mhf("all_ages")}
    by_year = []
    for year in sorted(taf.year.unique()):
        y = taf[(taf.year == year) & (taf.measure == "expenditures") & taf.category.isin(CATS)
                & ~taf.state.eq("National") & taf.group.eq("hispanic")].dropna(subset=["value"])
        for c in CATS:
            yc = y[y.category == c]
            fy = yc.state.map(FIPS).map(fc[c])
            by_year.append(dict(year=int(year), category=c, taf_total_bn=float(yc.total.sum()) / 1e9,
                                hispanic_share=float(yc.value.sum() / yc.total.sum()),
                                union_share_taf_only=float((yc.value * fy).sum() / yc.total.sum()),
                                states=int(len(yc))))
    pd.DataFrame(by_year).to_csv(DER / "shares_by_year.csv", index=False)

    # ---- combined with the medical-ethnicity lane ---------------------------------------------
    ta = pd.read_csv(MED / "translation_account.csv")
    med = ta[ta.line.eq("medicaid_and_chip_other_medical")].set_index("spec")
    five = ta[ta.line.eq("all five medical lines")].set_index("spec")
    base = effect(central)
    comb = []
    for spec in med.index:
        f = float(med.loc[spec, "key_weighted_ratio"])
        adj = (f - 1) * hf * (base["R"] * base["kr"] - B * k)
        comb.append(dict(spec=spec, med_ratio=f, med_five_line_bn=float(five.loc[spec, "delta_bn"]),
                         med_five_line_se=float(five.loc[spec, "se_bn"]), ltss_change_bn=base["total"],
                         remainder_ratio_adjustment_bn=adj,
                         combined_bn=float(five.loc[spec, "delta_bn"]) + base["total"] + adj))
    comb = pd.DataFrame(comb)
    comb.to_csv(DER / "combined.csv", index=False)
    summary = dict(
        cy2023_ltss_bn={c: central[c]["L2023"] for c in CATS}, ihss_cy2023_bn=ihss_cy2023,
        bea_growth_2024_over_2023=b24 / b23, current_rate=rate, remainder_key_ex_home_health=k_ex,
        union_share={c: central[c]["share"] for c in CATS},
        union_share_institutional=sum(central[c]["union2023"] for c in ["NF", "ICF", "MHF"])
        / sum(central[c]["L2023"] for c in ["NF", "ICF", "MHF"]),
        hispanic_share={c: central[c]["hisp_share"] for c in CATS},
        effect_central_bn=base["total"], effect_parts_bn={c: base[c] for c in CATS + ["remainder_key"]},
        effect_grid_bn=[float(np.min(grid)), float(np.median(grid)), float(np.max(grid))], grid_size=len(grid),
        cps_union_scale=cps_scale,
        main_case_adopted_bn=gate["main_case_adopted_bn"],
        main_case_with_ltss_bn=[x + base["total"] for x in gate["main_case_adopted_bn"]])
    (DER / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    pd.set_option("display.width", 220)
    print(sh.pivot_table(index="variant", columns="category", values="share").round(4).to_string())
    print(eff.round(2).to_string())
    print(comb.round(2).to_string())
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
