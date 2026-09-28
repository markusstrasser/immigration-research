"""Rough re-key of the adopted September 27 case's lines to non-Hispanic Black residents. Not the engine.

National lines, responses and capital stocks come from the engine at specs 48 / 11 (engine_lines.cjs ->
derived/engine_lines.json). Group shares come from CPS ASEC 2025 (income year 2024), MEPS 2024, T-MSIS LTSS 2023 and
justice shares. The same CPS keys run on the Mexican-origin union, so the rough method can be read against the engine.
Outputs: derived/rekey_summary.csv, derived/rekey_line_shares.csv, derived/rekey_gap_by_program.csv, derived/keys.csv.
"""
import csv
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
ROOT = FISCAL.parent.parent
DER = LANE / "derived"
ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
MEPS = ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
US = [57, 60, 66, 69, 73, 78]
OASDI_CAP = 168_600       # 2024 taxable maximum [SOURCE: SSA]
BETA = 0.7                # consumption ~ household income^0.7 [INFERENCE]
K12_PART = 0.74           # K-12 part of education_services; the rest higher education [INFERENCE]
LTSS_PART = 228.65 / 870.0   # T-MSIS 2023 LTSS spending over total Medicaid spending [DATA; total TRAINING-DATA]
BLK_LTSS = 0.20865        # T-MSIS 2023 LTSS spending, black_nh [DATA: ltss_share_2026_09_23/derived/taf_race_ethn.csv]
BLK_CUSTODY = 0.331       # SPI 2016 NH Black share of prisoners [SOURCE: research/immigration-crime-race-ethnicity-2026-09-05.md]
BLK_ARREST = 0.266        # FBI UCR 2019 Table 43A, Black share of all arrests [TRAINING-DATA]
REF_EITC_PART = 0.45      # EITC and ACTC in the refundable-credit line; the rest mostly premium credits [INFERENCE]

PC = ["PH_SEQ", "TAX_ID", "SPM_ID", "SPM_NUMPER", "MARSUPWT", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY",
      "PEMNTVTY", "PRDTHSP", "PEHSPNON", "PRDTRACE", "PEARNVAL", "PTOTVAL", "FEDTAX_AC", "STATETAX_A", "EIT_CRED",
      "ACTC_CRD", "SS_VAL", "SSI_VAL", "UC_VAL", "VET_VAL", "WC_VAL", "PAW_VAL", "SPM_SNAPSUB", "SPM_CAPHOUSESUB",
      "SPM_ENGVAL", "NOW_MCARE", "A_HSCOL", "INT_VAL", "DIV_VAL", "RNT_VAL"]
with zipfile.ZipFile(ZIP) as z:
    d = pd.read_csv(z.open("pppub25.csv"), usecols=PC)
    h = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "HPROP_VAL"]).rename(columns={"H_SEQ": "PH_SEQ"})
d = d.merge(h, on="PH_SEQ", how="left", validate="many_to_one")
civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
w = d.MARSUPWT.to_numpy(float) / 100 * civ
native = d.PRCITSHP.isin([1, 2, 3])
GROUPS = {
    "mex": ((d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)) | (native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)))
            | (native & d.PEFNTVTY.isin(US) & d.PEMNTVTY.isin(US) & d.PRDTHSP.eq(1))).to_numpy(),
    "blk": (d.PEHSPNON.eq(2) & d.PRDTRACE.eq(2)).to_numpy(),
}


def split(values, keys):
    """Sum a unit-level field over the unit's records, then give each member an equal part."""
    f = pd.DataFrame({k: d[k] for k in keys}).assign(v=np.asarray(values, float))
    g = f.groupby(keys).v
    return (g.transform("sum") / g.transform("size")).to_numpy()


def per_member(field):
    """SPM-unit field repeated on each member: the member's equal part."""
    return d[field].to_numpy(float) / d.SPM_NUMPER.to_numpy(float)


earn = d.PEARNVAL.clip(lower=0).to_numpy(float)
hh_n = d.groupby("PH_SEQ").PH_SEQ.transform("size").to_numpy(float)
hh_inc = split(d.PTOTVAL.clip(lower=0), ["PH_SEQ"]) * hh_n
college = d.A_HSCOL.eq(2).to_numpy(float)
inc_pp = hh_inc / hh_n
K = {
    "pc": np.ones(len(d)),
    "fit": np.maximum(split(d.FEDTAX_AC, ["PH_SEQ", "TAX_ID"]), 0),
    "sit": np.maximum(split(d.STATETAX_A, ["PH_SEQ", "TAX_ID"]), 0),
    "ref": split(d.EIT_CRED + d.ACTC_CRD, ["PH_SEQ", "TAX_ID"]),
    "oasdi": np.minimum(earn, OASDI_CAP),
    "hi": earn,
    "workers": (earn > 0).astype(float),
    "cons": np.maximum(hh_inc, 5_000) ** BETA / hh_n,
    "capinc": split((d.INT_VAL + d.DIV_VAL + d.RNT_VAL).clip(lower=0), ["PH_SEQ"]),
    "prop": d.HPROP_VAL.clip(lower=0).to_numpy(float) / hh_n,
    "mcare": d.NOW_MCARE.eq(1).to_numpy(float),
    "ss": d.SS_VAL.to_numpy(float), "ssi": d.SSI_VAL.to_numpy(float), "uc": d.UC_VAL.to_numpy(float),
    "vet": d.VET_VAL.to_numpy(float), "wc": d.WC_VAL.to_numpy(float), "paw": d.PAW_VAL.to_numpy(float),
    "snap": per_member("SPM_SNAPSUB"), "house": per_member("SPM_CAPHOUSESUB"), "eng": per_member("SPM_ENGVAL"),
    "k12": d.A_AGE.between(5, 17).to_numpy(float),
    "college": college,
    "edben": college * (inc_pp < np.median(inc_pp[civ])),
}
share = {g: {k: float((w * v)[m].sum() / (w * v).sum()) for k, v in K.items()} for g, m in GROUPS.items()}
pop = {g: float(w[m].sum()) for g, m in GROUPS.items()}
cps_bn = {g: {k: float((w * K[k])[m].sum() / 1e9) for k in ("fit", "sit")} for g, m in GROUPS.items()}

# MEPS 2024: NH Black (RACETHX 3) share of each public payer's spending.
sys.path.insert(0, str(FISCAL / "build"))
from public_mvp_io import parse_meps_sas_fields  # noqa: E402

lay = parse_meps_sas_fields(MEPS.with_name("h256su.txt"))
F = ["PERWT24F", "RACETHX", "TOTMCD24", "TOTMCR24", "TOTOFD24", "TOTSTL24", "TOTVA24", "TOTTRI24"]
with zipfile.ZipFile(MEPS) as z:
    name = [n for n in z.namelist() if n.lower().endswith(".dat")][0]
    rows = [{k: float(t[lay[k][0]:sum(lay[k])]) for k in F} for t in (ln.decode("ascii") for ln in z.open(name))]
md = pd.DataFrame(rows)
mw = md.PERWT24F.to_numpy()
mb = md.RACETHX.eq(3).to_numpy()
meps = {c: float((mw * md[c])[mb].sum() / (mw * md[c]).sum()) for c in F[2:]}
meps["other_public"] = float((mw * (md.TOTOFD24 + md.TOTSTL24))[mb].sum() / (mw * (md.TOTOFD24 + md.TOTSTL24)).sum())
meps["pop"] = float(mw[mb].sum() / mw.sum())

cj = pd.read_csv(FISCAL / "cj_use_allocation_2026_09_23/derived/central_split.csv").set_index("component")
case = json.loads((DER / "engine_lines.json").read_text())
lo_lines = {l["side"] + "|" + l["id"]: l for l in case["low"]["lines"] if l["side"] != "scalar"}
NATIONAL = {k: l["national_bn"] for k, l in lo_lines.items()}
eng_share = {k: (l["amount_bn"] / l["national_bn"] if abs(l["national_bn"]) > 1e-6 else 0.0) for k, l in lo_lines.items()}
pc_scale = eng_share["spending|general_public_services"] / share["mex"]["pc"]   # engine's per-head share over CPS's


def pc(g):
    return share[g]["pc"] * pc_scale


def justice_blk():
    """The adopted justice lane's rule: police half arrests, courts 60% arrests, prisons custody, rest per head."""
    ph = pc("blk")
    key = {"fire": ph, "prisons": BLK_CUSTODY, "law_courts": 0.6 * BLK_ARREST + 0.4 * ph, "police_cbp": ph,
           "police_ice_border": ph, "police_ice_interior": ph, "police_non_border": 0.5 * BLK_ARREST + 0.5 * ph}
    return float(sum(cj.loc[c, "national_bn"] * k for c, k in key.items()) / cj.national_bn.sum())


medicaid_blk = LTSS_PART * BLK_LTSS + (1 - LTSS_PART) * meps["TOTMCD24"]
RECEIPT_KEY = {"federal_income_tax": "fit", "state_local_income_tax": "sit", "personal_motor_vehicle": "cons",
               "personal_property_tax": "prop", "other_personal_tax": "fit", "employee_oasdi": "oasdi",
               "employer_oasdi": "oasdi", "employee_hi": "hi", "employer_hi": "hi", "self_employment_oasdi_hi": "oasdi",
               "medicare_supplementary_premiums": "mcare", "other_domestic_social_contributions": "workers",
               "corporate_capital": "capinc", "corporate_labor": "hi", "general_sales_tax": "cons",
               "modeled_owner_property": "prop", "remaining_production_property": "capinc",
               "excise_selective_sales": "cons", "customs_duties": "cons", "other_production_taxes": "capinc",
               "government_asset_income": "pc", "business_current_transfers": "capinc",
               "personal_current_transfers": "cons", "enterprise_surplus": "pc"}
SPEND_KEY = {"general_public_services": "pc", "defense": "pc", "economic_affairs_services": "hi",
             "housing_community_services": "pc", "recreation_culture": "pc", "income_security_services": "snap",
             "social_security": "ss", "unemployment": "uc", "railroad_retirement": "ss", "pension_guaranty": "ss",
             "veterans_life_insurance": "vet", "workers_compensation": "wc", "veterans_pension_disability": "vet",
             "veterans_readjustment": "vet", "snap": "snap", "black_lung": "wc", "ssi": "ssi",
             "refundable_tax_credits": "ref", "other_federal_benefits": "ss", "temporary_disability": "wc",
             "family_and_general_assistance": "paw", "energy_assistance": "eng", "other_state_welfare": "paw",
             "education_benefits": "edben", "employment_training": "pc", "other_state_benefits": "pc",
             "domestic_interest": "pc", "agricultural_subsidies": "hi", "housing_subsidies": "house",
             "transport_subsidies": "hi", "other_subsidies": "hi"}
BLK_EXTERNAL = {"public_order_safety": justice_blk(), "health_services": meps["other_public"],
                "medicare": meps["TOTMCR24"], "veterans_other": meps["TOTVA24"], "military_medical": meps["TOTTRI24"],
                "medicaid_and_chip_other_medical": medicaid_blk}
ADJUST = {"school_reprice", "college_rekey", "lane_constants", "source_rounding"}   # Mexican-origin-specific lines
ZERO = {"rest_world_tax_contributions", "rest_world_current_transfers", "foreign_territory_social_benefits",
        "other_foreign_current_transfers", "foreign_interest"}
# CPS misses the top tail: a group's CPS tax dollars are charged against the national line, not scaled up.
TOP_TAIL = {"federal_income_tax": ("fit", "receipts|federal_income_tax"),
            "other_personal_tax": ("fit", "receipts|federal_income_tax"),
            "state_local_income_tax": ("sit", "receipts|state_local_income_tax")}
OLD_AGE = {"employee_oasdi", "employer_oasdi", "employee_hi", "employer_hi", "self_employment_oasdi_hi",
           "medicare_supplementary_premiums", "social_security", "medicare", "railroad_retirement", "pension_guaranty"}
BUCKETS = {
    "income taxes": ["federal_income_tax", "state_local_income_tax", "other_personal_tax"],
    "payroll and Medicare premiums": ["employee_oasdi", "employer_oasdi", "employee_hi", "employer_hi",
                                      "self_employment_oasdi_hi", "medicare_supplementary_premiums",
                                      "other_domestic_social_contributions"],
    "sales, excise, customs, fees": ["general_sales_tax", "excise_selective_sales", "customs_duties",
                                     "personal_current_transfers", "personal_motor_vehicle"],
    "capital, property, production taxes": ["corporate_capital", "corporate_labor", "modeled_owner_property",
                                            "remaining_production_property", "other_production_taxes",
                                            "business_current_transfers", "personal_property_tax",
                                            "government_asset_income", "enterprise_surplus"],
    "Social Security and Medicare": ["social_security", "medicare", "railroad_retirement", "pension_guaranty"],
    "Medicaid": ["medicaid_and_chip_other_medical"],
    "schools and colleges": ["education_services", "education_benefits", "school_reprice", "college_rekey"],
    "police, courts, prisons": ["public_order_safety"],
    "SNAP, SSI, housing, cash aid, credits, other welfare": [
        "snap", "ssi", "housing_subsidies", "family_and_general_assistance", "other_state_welfare", "energy_assistance",
        "refundable_tax_credits", "income_security_services", "unemployment", "workers_compensation",
        "temporary_disability", "black_lung"],
    "veterans and military medical": ["veterans_pension_disability", "veterans_readjustment", "veterans_other",
                                      "veterans_life_insurance", "military_medical"],
}


def line_share(g, side, lid):
    if lid in ZERO:
        return 0.0
    key = RECEIPT_KEY.get(lid) if side == "receipts" else SPEND_KEY.get(lid)
    if side == "spending" and lid == "education_services":
        return K12_PART * share[g]["k12"] + (1 - K12_PART) * share[g]["college"]
    if key == "pc":
        return pc(g)
    if lid in TOP_TAIL:
        k, nat = TOP_TAIL[lid]
        return cps_bn[g][k] / NATIONAL[nat]
    if lid == "refundable_tax_credits":
        return REF_EITC_PART * share[g]["ref"] + (1 - REF_EITC_PART) * pc(g)
    if key:
        return share[g][key]
    if g == "blk":
        return BLK_EXTERNAL[lid]
    return eng_share[side + "|" + lid]     # the Mexican rough run keeps the engine's medical and justice shares


def run(g, end):
    """g: 'eng' (the engine's own amounts), 'mex' or 'blk' (rough keys)."""
    e = case[end]
    rec_amt = rec_eff = sp_amt = sp_eff = alloc_bal = 0.0
    old = dict(bal=0.0, net=0.0, alloc=0.0)
    rows = []
    for ln in e["lines"]:
        if ln["side"] == "scalar":
            continue
        side, lid = ln["side"], ln["id"]
        if g == "eng" or (lid in ADJUST and g == "mex"):
            amt = ln["amount_bn"]
        elif lid in ADJUST:
            amt = 0.0
        else:
            amt = ln["national_bn"] * line_share(g, side, lid)
        eff = amt * ln["response"]
        if lid not in ZERO:
            alloc_bal += ln["national_bn"] if side == "receipts" else -ln["national_bn"]
        if lid in OLD_AGE:
            sgn = 1 if side == "receipts" else -1
            old["bal"] += sgn * amt
            old["net"] -= sgn * eff
            old["alloc"] += sgn * ln["national_bn"]
        if side == "receipts":
            rec_amt += amt
            rec_eff += eff
        else:
            sp_amt += amt
            sp_eff += eff
        rows.append((side, lid, ln["national_bn"], amt, ln["response"]))
    sg = share["mex" if g == "eng" else g]
    ck = {"k12": sg["k12"], "college": sg["college"], "hwy": sg["hi"], "air": sg["hi"]}
    cap_bn = 0.0
    for c in e["capital"]:
        cid = c["id"]
        if cid.startswith("pos"):
            k = BLK_EXTERNAL["public_order_safety"] if g == "blk" else c["key"]
        elif cid.startswith("health"):
            k = BLK_EXTERNAL["health_services"] if g == "blk" else c["key"]
        else:
            k = ck.get(cid.split("_")[0], pc("mex" if g == "eng" else g))
        cap_bn += c["stock_charged_bn"] * k * c["response"] * e["rate"]
    if g == "eng":
        cap_bn = e["capital_bn"]
    prod = [x for x in e["lines"] if x["side"] == "scalar" and x["id"] == "production_gain_bn"][0]["effect_bn"]
    prod = prod if g in ("mex", "eng") else 0.0    # no production term for the Black group
    net = sp_eff - rec_eff
    popg = pop["blk"] if g == "blk" else e["target_population"]
    sh = popg / e["resident_population"]
    bal = rec_amt - sp_amt
    return dict(taxes_paid=rec_amt, spending_drawn=sp_amt, taxes_lost=rec_eff, spending_saved=sp_eff, net_budget=net,
                capital=cap_bn, production_gain=prod, cost=net + cap_bn - prod, balance=bal,
                gap=bal - sh * alloc_bal, cost_ex_old_age=net + cap_bn - prod - old["net"],
                gap_ex_old_age=(bal - old["bal"]) - sh * (alloc_bal - old["alloc"]), population=popg,
                pop_share=sh), rows


def write(name, rows, fields):
    with open(DER / name, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)


def main():
    summary, line_rows, bucket_rows = [], {}, []
    for end in ("low", "high"):
        for g in ("eng", "mex", "blk"):
            r, rows = run(g, end)
            lab = {"eng": "mexican_origin_engine", "mex": "mexican_origin_rough", "blk": "nh_black_rough"}[g]
            summary.append({"group": lab, "end": end, "spec": case[end]["spec"],
                            **{k: f"{v:.4f}" for k, v in r.items() if k not in ("population", "pop_share")},
                            "population": f"{r['population']:.0f}", "pop_share": f"{r['pop_share']:.6f}",
                            "cost_per_member": f"{r['cost'] * 1e9 / r['population']:.0f}",
                            "gap_per_member": f"{r['gap'] * 1e9 / r['population']:.0f}"})
            print(f"{lab:22s} {end:4s} cost {r['cost']:7.1f}  net budget {r['net_budget']:7.1f}  capital "
                  f"{r['capital']:5.1f}  gap {r['gap']:7.1f}  ex old-age cost {r['cost_ex_old_age']:7.1f} gap "
                  f"{r['gap_ex_old_age']:7.1f}  per member cost {r['cost'] * 1e9 / r['population']:6.0f}")
            if end == "low":
                line_rows[g] = rows
                contrib = {}
                for side, lid, nat, amt, _ in rows:
                    if lid in ZERO:
                        continue
                    b = next((k for k, v in BUCKETS.items() if lid in v), "per head: government, defense, interest, roads")
                    contrib[b] = contrib.get(b, 0.0) + (1 if side == "receipts" else -1) * (amt - r["pop_share"] * nat)
                for b, v in contrib.items():
                    bucket_rows.append({"group": lab, "bucket": b, "gap_bn": f"{v:.4f}",
                                        "per_member": f"{v * 1e9 / r['population']:.0f}"})
    write("rekey_summary.csv", summary, list(summary[0]))
    write("rekey_gap_by_program.csv", bucket_rows, ["group", "bucket", "gap_bn", "per_member"])
    shares = []
    for (side, lid, nat, amt_b, resp), (_, _, _, amt_m, _), (_, _, _, amt_e, _) in zip(
            line_rows["blk"], line_rows["mex"], line_rows["eng"]):
        s = (lambda a: f"{a / nat:.6f}" if abs(nat) > 1e-6 else "")
        shares.append({"side": side, "line": lid, "national_bn": f"{nat:.4f}", "response_low": f"{resp:.4f}",
                       "share_mex_engine": s(amt_e), "share_mex_rough": s(amt_m), "share_nh_black_rough": s(amt_b),
                       "amount_nh_black_rough_bn": f"{amt_b:.4f}"})
    write("rekey_line_shares.csv", shares, list(shares[0]))
    keys = [{"key": f"meps_nh_black_{k}", "value": f"{v:.6f}"} for k, v in meps.items()]
    keys += [{"key": "medicaid_nh_black_blended", "value": f"{medicaid_blk:.6f}"},
             {"key": "justice_nh_black", "value": f"{justice_blk():.6f}"},
             {"key": "per_head_scale", "value": f"{pc_scale:.6f}"},
             {"key": "cps_population_mex", "value": f"{pop['mex']:.0f}"},
             {"key": "cps_population_nh_black", "value": f"{pop['blk']:.0f}"}]
    write("keys.csv", keys, ["key", "value"])


if __name__ == "__main__":
    main()
