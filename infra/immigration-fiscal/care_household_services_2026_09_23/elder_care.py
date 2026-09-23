#!/usr/bin/env python3
"""Elder care: Medicaid nursing-facility saving net of Medicaid home-care spending, union frame.

The group's care workers keep other residents' elderly out of nursing homes (a Medicaid
saving the account omits), and also staff Medicaid-financed home care (a Medicaid outlay the
account omits). Both are fiscal and ADD to the account; their difference is the channel.

Dose. Removing the group removes its care workers and its own care needs. Care available per
unit of other residents' need changes by (1 - s)/(1 - d) - 1, s = the group's share of market
hours, d = its share of care need (ACS 2024, scaled to the CPS union). Each paper's reduced form
is scaled by this dose over the paper's own first stage (a Wald ratio):
  AAF  Almuhaisen–Amuedo-Dorantes–Furtado (J Health Econ 2024): Secure Communities (SC) cut
       home-care hours in home health and private households 5.95% (SE 2.81) and raised
       institutionalization of US citizens 65+ by 0.257pp (SE 0.096; 6.81% of the mean), or
       nursing-home residents by 2.71% (SE 0.51; LTCFocus, Appendix Table B2)
  KW   Kreider–Werner (JMP 2025): SC cut home-care workers 7.49% (SE 2.68) and formal home care
       of Medicaid elders with care needs by 4.6pp (SE 2.1; base 19.8%); non-Medicaid +0.6pp
  BMW  Butcher–Moran–Watson (NBER w29520): institutionalization of the US-born 65+ per unit of
       the less-educated foreign-born share of the working-age population, -0.151 (SE 0.027);
       mapped by labour share (the FAQ's route) and by care hours
Prices: Medicaid nursing-facility spending (CMS NHE 2024 Table 15) per resident (CMS provider
file) or per ACS institutional person 65+; Medicaid HCBS per person (KFF, FY2020, CPI to 2024).

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/care_household_services_2026_09_23/elder_care.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
D = HERE / "derived"
CMS_NH = HERE / "_cache/NH_ProviderInfo_Aug2026.csv"
CMS_NH_URL = ("https://data.cms.gov/provider-data/sites/default/files/resources/"
              "328596835e6db31b2564cd733c3795f4_1786724150/NH_ProviderInfo_Aug2026.csv")
NHE_XLSX = ROOT / ("infra/immigration-fiscal/mr_leads_papers_2026_09_21/_cache/nhe_tables/"
                   "Table 15 Nursing Care Facilities and Continuing Care Retirement Communities "
                   "Expenditures.xlsx")

CPS_UNION = 40_896_574
ACS_TOTAL_POP = 340_110_988
OTHERS = ACS_TOTAL_POP - CPS_UNION
DRAWS = 200_000
SEED = 20260923

# CMS National Health Expenditure 2024, Table 15 (nursing care facilities and CCRCs), $bn
NHE_2024 = {"total": 219.9, "medicare": 47.3, "medicaid": 78.9}
# NCHS NHSR 208 (2020 NPALS), nursing-home residents by age: under 65 = 17.9%
NH_SHARE_65PLUS = 1 - 0.179
NPALS_2020_RESIDENTS = 1_294_800
# KFF, Medicaid HCBS people served and spending, FY2020: per person, 1915(c) waivers for seniors
# and adults with physical disabilities $17,600; all state-plan HCBS $13,900
HCBS_PER_PERSON_2020 = {"state_plan_all": 13_900, "waiver_seniors_pd": 17_600}
CPI_U = {2020: 258.811, 2024: 313.689}  # BLS CUUR0000SA0 annual averages

AAF = {"fs": (-0.0595, 0.61382 / 21.82),
       "acs_abs": (0.00257, 0.00096),
       "acs_rel": (0.0681, 0.0681 * 0.00096 / 0.00257),
       "ltc_log_residents": (0.02714, 0.00508)}
KW = {"fs": (-29.727 / 396.8, 10.644 / 396.8), "formal_care_medicaid": (-0.046, 0.021)}
BMW = {"preferred": (0.151, 0.027), "without_california": (0.090, None),
       "year_by_state_ns": (0.061, 0.058)}


def nh_residents() -> tuple[float, str]:
    if CMS_NH.exists():
        d = pd.read_csv(CMS_NH, usecols=["Average Number of Residents per Day"])
        r = pd.to_numeric(d["Average Number of Residents per Day"], errors="coerce")
        return float(r.sum()), f"CMS provider file Aug 2026 ({r.notna().sum()} facilities)"
    print(f"  ! {CMS_NH.name} missing (fetch {CMS_NH_URL}); using NPALS 2020")
    return float(NPALS_2020_RESIDENTS), "NPALS 2020"


def check_nhe() -> str:
    if not NHE_XLSX.exists():
        return "NHE workbook not on this machine; constants as published"
    import openpyxl
    ws = openpyxl.load_workbook(NHE_XLSX, read_only=True, data_only=True).active
    for row in ws.iter_rows(values_only=True):
        if row and str(row[0]).strip() == "2024":
            got = {"total": float(row[1]), "medicare": float(row[5]), "medicaid": float(row[6])}
            if got != NHE_2024:
                raise SystemExit(f"[BLOCKED] NHE 2024 row {got} != {NHE_2024}")
            return "NHE workbook matches"
    raise SystemExit("[BLOCKED] NHE 2024 row not found")


def main() -> None:
    nat = pd.read_csv(D / "acs_national.csv")
    n = dict(zip(nat["item"], nat["estimate"]))
    mk = pd.read_csv(D / "acs_care_market_shares.csv")
    share = {(r.market, r.group): r.hours_share for r in mk.itertuples()}
    k = CPS_UNION / n["pop_union"]
    nhe_note = check_nhe()
    nh_total, nh_source = nh_residents()

    # ------------------------------------------------ populations (other residents)
    g_u, g_o = ("union_fb", "union_nat"), ("other_fb", "other_nat")
    tot = lambda stem, gs: sum(n[f"{stem}_{g}"] for g in gs)
    need = {
        "need_all_ages": (tot("need_hh_65p", g_u) + tot("need_hh_u65", g_u),
                          tot("need_hh_65p", g_o) + tot("need_hh_u65", g_o)),
        "need_65plus": (tot("need_hh_65p", g_u), tot("need_hh_65p", g_o)),
        "need_medicaid": (tot("need_hh_medicaid_65p", g_u) + tot("need_hh_medicaid_u65", g_u),
                          tot("need_hh_medicaid_65p", g_o) + tot("need_hh_medicaid_u65", g_o)),
        "no_netting": (0.0, 1.0),
    }
    demand_share = {name: k * u / (k * u + o) for name, (u, o) in need.items()}
    inst65_all = tot("e65_inst", g_u) + tot("e65_inst", g_o)
    union_inst_share = k * tot("e65_inst", g_u) / (k * tot("e65_inst", g_u) + tot("e65_inst", g_o))
    base = {
        "others_citizen_65p": tot("e65_citizen", g_o),
        "others_citizen_65p_institutional": tot("e65_citizen_inst", g_o),
        "others_usborn_65p": n["e65_other_nat"],
        "others_medicaid_65p_with_need_in_households": tot("need_hh_medicaid_65p", g_o),
        "nh_residents_all": nh_total,
        "nh_residents_others": nh_total * (1 - union_inst_share),
        "acs_institutional_65p_all": inst65_all,
    }

    # ------------------------------------------------ prices
    medicaid = NHE_2024["medicaid"] * 1e9
    price = {
        "per_nh_resident": medicaid / nh_total,
        "per_acs_institutional_65p": NH_SHARE_65PLUS * medicaid / inst65_all,
    }
    infl = CPI_U[2024] / CPI_U[2020]
    hcbs_price = {name: v * infl for name, v in HCBS_PER_PERSON_2020.items()}

    # ------------------------------------------------ doses
    dose_rows = []
    for market in ("home_care_aaf", "home_care_kw", "home_care_broad", "direct_care_all"):
        s = k * share[(market, "union")]
        for dname, d in demand_share.items():
            dose_rows.append(dict(market=market, union_hours_share_scaled=s, netting=dname,
                                  union_demand_share=d, net_dose=(1 - s) / (1 - d) - 1))
    doses = pd.DataFrame(dose_rows)
    doses.to_csv(D / "elder_care_doses.csv", index=False)
    dose = {(r.market, r.netting): r.net_dose for r in doses.itertuples()}

    # ------------------------------------------------ BMW treatment in the union frame
    T0 = n["bmw_lowed_fb_all"] / n["bmw_wa_all"]
    T1 = (n["bmw_lowed_fb_all"] - k * n["bmw_lowed_fb_union"]) / (n["bmw_wa_all"] - k * n["bmw_wa_union"])
    T1_mex = (n["bmw_lowed_fb_all"] - n["bmw_lowed_fb_mexborn"]) / n["bmw_wa_all"]

    rng = np.random.default_rng(SEED)

    def draw(mean_se):
        m, se = mean_se
        return m + (se or 0.0) * rng.standard_normal(DRAWS)

    rows, sims = [], {}

    def add(channel, spec, netting, people_point, people_draws, price_name, unit_price, sign):
        dollars = sign * people_draws * unit_price / 1e9
        pt = sign * people_point * unit_price / 1e9
        q = np.percentile(dollars, [2.5, 5, 50, 95, 97.5])
        rows.append(dict(channel=channel, spec=spec, netting=netting, people_point=people_point,
                         price=price_name, unit_price=unit_price, bn_point=pt,
                         bn_p2_5=q[0], bn_p5=q[1], bn_median=q[2], bn_p95=q[3], bn_p97_5=q[4],
                         per_group_member=pt * 1e9 / CPS_UNION, per_other_resident=pt * 1e9 / OTHERS))
        sims[(channel, spec, netting, price_name)] = dollars

    fs_aaf = draw(AAF["fs"])
    rf = {key: draw(AAF[key]) for key in ("acs_abs", "acs_rel", "ltc_log_residents")}
    fs_kw, rf_kw = draw(KW["fs"]), draw(KW["formal_care_medicaid"])
    for netting in demand_share:
        dz = dose[("home_care_aaf", netting)]
        ratio_pt, ratio = dz / AAF["fs"][0], dz / fs_aaf
        # nursing-facility saving: people kept out, priced by the measure's own denominator
        add("nf_saving", "aaf_ltcfocus_nh_residents", netting,
            AAF["ltc_log_residents"][0] * ratio_pt * base["nh_residents_others"],
            rf["ltc_log_residents"] * ratio * base["nh_residents_others"],
            "per_nh_resident", price["per_nh_resident"], +1)
        add("nf_saving", "aaf_acs_relative", netting,
            AAF["acs_rel"][0] * ratio_pt * base["others_citizen_65p_institutional"],
            rf["acs_rel"] * ratio * base["others_citizen_65p_institutional"],
            "per_acs_institutional_65p", price["per_acs_institutional_65p"], +1)
        add("nf_saving", "aaf_acs_absolute", netting,
            AAF["acs_abs"][0] * ratio_pt * base["others_citizen_65p"],
            rf["acs_abs"] * ratio * base["others_citizen_65p"],
            "per_acs_institutional_65p", price["per_acs_institutional_65p"], +1)
        # AAF's two outcome measures pooled by the precision of their reduced forms (the first
        # stage is common to both, so it scales both draws alike)
        l_pt = AAF["ltc_log_residents"][0] * ratio_pt * base["nh_residents_others"] * price["per_nh_resident"]
        a_pt = (AAF["acs_rel"][0] * ratio_pt * base["others_citizen_65p_institutional"]
                * price["per_acs_institutional_65p"])
        w_l = 1 / (l_pt * AAF["ltc_log_residents"][1] / AAF["ltc_log_residents"][0]) ** 2
        w_a = 1 / (a_pt * AAF["acs_rel"][1] / AAF["acs_rel"][0]) ** 2
        l_dr = sims[("nf_saving", "aaf_ltcfocus_nh_residents", netting, "per_nh_resident")]
        a_dr = sims[("nf_saving", "aaf_acs_relative", netting, "per_acs_institutional_65p")]
        pooled_pt = (w_l * l_pt + w_a * a_pt) / (w_l + w_a)
        pooled_dr = (w_l * l_dr + w_a * a_dr) / (w_l + w_a)
        q = np.percentile(pooled_dr, [2.5, 5, 50, 95, 97.5])
        rows.append(dict(channel="nf_saving", spec="aaf_pooled_precision_weighted", netting=netting,
                         people_point=np.nan, price="own_measure", unit_price=np.nan,
                         bn_point=pooled_pt / 1e9, bn_p2_5=q[0], bn_p5=q[1], bn_median=q[2],
                         bn_p95=q[3], bn_p97_5=q[4], per_group_member=pooled_pt / CPS_UNION,
                         per_other_resident=pooled_pt / OTHERS, pool_weight_ltcfocus=w_l / (w_l + w_a)))
        sims[("nf_saving", "aaf_pooled_precision_weighted", netting, "own_measure")] = pooled_dr
        # BMW, care-hour mapping on two markets
        for market in ("home_care_aaf", "direct_care_all"):
            c_T = share[(market, "lowed_fb_all_origins")]
            dT = -dose[(market, netting)] * T0 / c_T
            for bname, b in BMW.items():
                bd = draw(b)
                add("nf_saving", f"bmw_care_hours_{market}_{bname}", netting,
                    b[0] * dT * base["others_usborn_65p"], bd * dT * base["others_usborn_65p"],
                    "per_acs_institutional_65p", price["per_acs_institutional_65p"], +1)
        # Medicaid home care the group's workers staff (an outlay while present)
        dz_kw = dose[("home_care_kw", netting)]
        r_pt, r = dz_kw / KW["fs"][0], dz_kw / fs_kw
        for pname, pv in hcbs_price.items():
            add("hcbs_outlay", f"kw_formal_care_{pname}", netting,
                -KW["formal_care_medicaid"][0] * r_pt * base["others_medicaid_65p_with_need_in_households"],
                -rf_kw * r * base["others_medicaid_65p_with_need_in_households"],
                f"hcbs_{pname}", pv, -1)
    # BMW labour-share mapping (the FAQ's route, union frame and Mexico-born only)
    for bname, b in BMW.items():
        bd = draw(b)
        for label, dT in (("union_frame", T0 - T1), ("mexborn_only_faq", T0 - T1_mex)):
            add("nf_saving", f"bmw_labour_share_{label}_{bname}", "none_by_construction",
                b[0] * dT * base["others_usborn_65p"], bd * dT * base["others_usborn_65p"],
                "per_acs_institutional_65p", price["per_acs_institutional_65p"], +1)

    specs = pd.DataFrame(rows)
    specs.to_csv(D / "elder_care_specs.csv", index=False)

    # ------------------------------------------------ net Medicaid (saving minus home-care outlay)
    net_rows = []
    for netting in demand_share:
        for nf_spec in ("aaf_pooled_precision_weighted", "aaf_ltcfocus_nh_residents", "aaf_acs_relative",
                        "aaf_acs_absolute", "bmw_care_hours_home_care_aaf_preferred",
                        "bmw_care_hours_direct_care_all_preferred"):
            nf_key = [key for key in sims if key[0] == "nf_saving" and key[1] == nf_spec and key[2] == netting][0]
            for pname in hcbs_price:
                hc_key = ("hcbs_outlay", f"kw_formal_care_{pname}", netting, f"hcbs_{pname}")
                net = sims[nf_key] + sims[hc_key]
                pt = (specs.set_index(["channel", "spec", "netting"]).loc[(nf_key[0], nf_key[1], netting), "bn_point"]
                      + specs.set_index(["channel", "spec", "netting"]).loc[(hc_key[0], hc_key[1], netting), "bn_point"])
                q = np.percentile(net, [2.5, 5, 50, 95, 97.5])
                net_rows.append(dict(nf_spec=nf_spec, hcbs_price=pname, netting=netting, bn_point=float(pt),
                                     bn_p2_5=q[0], bn_p5=q[1], bn_median=q[2], bn_p95=q[3], bn_p97_5=q[4],
                                     prob_negative=float((net < 0).mean()),
                                     per_group_member=float(pt) * 1e9 / CPS_UNION,
                                     per_other_resident=float(pt) * 1e9 / OTHERS))
    net = pd.DataFrame(net_rows)
    net.to_csv(D / "elder_care_net.csv", index=False)

    audit = dict(cps_scale=k, nh_residents=nh_total, nh_source=nh_source, nhe_check=nhe_note,
                 nhe_2024_bn=NHE_2024, nh_share_65plus=NH_SHARE_65PLUS, prices=price,
                 hcbs_price_2024=hcbs_price, cpi_ratio_2024_2020=infl,
                 demand_share=demand_share, union_institutional_share_65p=union_inst_share,
                 bases=base, bmw_T0=T0, bmw_T1_union=T1, bmw_T1_mexborn=T1_mex,
                 bmw_dT_union=T0 - T1, bmw_dT_mexborn=T0 - T1_mex,
                 lowed_fb_hour_share={m: share[(m, "lowed_fb_all_origins")] for m in
                                      ("home_care_aaf", "home_care_kw", "direct_care_all")},
                 draws=DRAWS, seed=SEED,
                 faq13_price_per_resident=78.9e9 / 1_433_206)
    (D / "elder_care_audit.json").write_text(json.dumps(audit, indent=2))
    pd.set_option("display.width", 230)
    print(json.dumps(audit, indent=2))
    print(doses.to_string(index=False))
    show = specs[specs.netting.isin(["need_all_ages", "none_by_construction"])]
    print(show[["channel", "spec", "netting", "people_point", "unit_price", "bn_point", "bn_p5",
                "bn_median", "bn_p95"]].to_string(index=False))
    print(net.to_string(index=False))


if __name__ == "__main__":
    main()
