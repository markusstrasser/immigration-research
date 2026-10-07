#!/usr/bin/env python3
"""The tax side of the current-law arm: P.L. 119-21's individual tax changes against 2024 law, for the lineage.

post2024_law.py prices the law's transfer cuts. By the evidence-symmetry rules (decisions/2026-09-23-evidence-symmetry-
rules.md) the same law's tax changes for the same people belong beside them. The 2024 account already uses TCJA-era
law, so the TCJA extension is no change; only provisions that differ from 2024 law in TY2027 / FY2028 are priced:

  §70201 qualified tips deduction (cap $25,000, phase-out $100 per $1,000 of MAGI over $150k/$300k, SSN required)
  §70202 qualified overtime deduction (FLSA premium only, cap $12,500/$25,000, same phase-out, SSN required)
  §70203 car-loan interest deduction (cap $10,000, phase-out over $100k/$200k)
  §70103 senior deduction ($6,000 per person 65+, 6% phase-out over $75k/$150k, SSN required)
  §70104 child tax credit $2,200 indexed, against 2024 law's $2,000; units that lose the credit under the SSN rule
         (post2024_law.py) get nothing here, so the two never count the same unit
  §70102 standard-deduction increase beyond TCJA indexing ($750 / $1,500 / $1,125 in 2025, indexed)
  §70120 SALT cap $40,000 (2025) rising 1% a year to 2029, phased down 30% over $500k MAGI to a $10,000 floor
  §70424 charitable deduction for non-itemizers, $1,000 / $2,000, from 2026
plus two smaller items kept because the lineage's share is large: §70604's 1% excise on cash-funded remittances (a
tax increase) and §70204's $1,000 Trump-account deposit for citizen children born 2025-2028 (a new transfer).

Shares: Tax-Calculator 6.8.4 (`--with taxcalc`, which models these provisions) on CPS ASEC 2025 tax units (TAX_ID),
2024 incomes, 2024 law against 2024 law plus one provision at its statutory parameters; the change in iitax is
split equally over each unit's members and summed on the lineage weights over row-4 weights (post2024_law's frame).
Levels: JCT's FY2028 score where a provision is scored alone (tips, overtime, car loans, charity, remittances,
Trump accounts; CBO 61570). The senior deduction, the $200 child-credit increase, the standard-deduction increase and
the SALT change are scored only together with TCJA extensions, so their national levels come from Tax-Calculator on
its own bundled data for TY2027 (current law against the provision reverted to 2024 law) [CALCULATION, model level].

Proxies [ASSUMPTION]: tips = a fixed share of wages and self-employment income in customarily tipped occupations
(OCCUP, longest job: 0.40 food and drink service, 0.10 fast food and counter, 0.25 personal care, transport and
other); overtime = the FLSA half-time premium of employees paid by the hour (A_HRLYWK, asked only in the outgoing
rotation, PRERELG = 1, so the overtime share uses those records alone) with usual hours (HRSWK) over 40; car-loan
interest and cash giving are unobserved, so each unit gets a uniform $1,000 of interest or $500 of giving and the
share follows the tax value of the deduction; property tax = 1% of the owner household's property value (HPROP_VAL).
Imputed-unauthorized people get no tips, overtime or senior deduction (no work-authorized SSN). Remittances: the
lineage share of the taxed base is the Mexico corridor less H-2 pay ($58.8bn, consumption_key_2026_09_24) over the
base JCT's revenue implies (1% of $108.9bn), 0.40-0.65 around it. Trump accounts: the lineage's share of citizen
children aged 0.

Writes derived/tax_rows.csv and derived/tax_summary.json (the net line reads derived/summary.json, so run
post2024_law.py first). From the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with taxcalc==6.8.4 python3 infra/immigration-fiscal/post2024_law_2026_10_07/tax_side.py
"""
from __future__ import annotations

import csv
import gc
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE))
import post2024_law as P  # noqa: E402

import taxcalc as tc  # noqa: E402

OUT = LANE / "derived"
TAXCALC_VERSION = "6.8.4"
INCOME_P = ["SEMP_VAL", "FRSE_VAL", "PNSN_VAL", "ANN_VAL", "DIV_VAL", "RNT_VAL", "UC_VAL", "SS_VAL", "INT_VAL",
            "STATETAX_B", "OCCUP", "HRSWK", "WKSWORK", "A_HRLYWK", "PRERELG", "A_CLSWKR", "A_LINENO", "FILESTAT"]
INCOME_H = ["HPROP_VAL", "H_TENURE"]
TIP_FRAC = {**{c: 0.40 for c in (4040, 4110, 4120, 4130, 4150)}, 4055: 0.10,
            **{c: 0.25 for c in (3630, 4400, 4500, 4510, 4521, 4522, 4530, 9141, 9142, 9350)}}
PROPERTY_TAX_RATE = 0.01
CAR_LOAN_INTEREST = 1_000.0
CASH_GIVING = 500.0
STD_INCREASE_2025 = [750.0, 1500.0, 750.0, 1125.0, 1500.0]   # single, joint, separate, head of household, widow
# JCT FY2028 scores, $M (CBO 61570 Title VII revenue table; Trump accounts from the outlay table).
JCT = {"tips_70201": (70201, "Estimated Revenues", -8078), "overtime_70202": (70202, "Estimated Revenues", -22982),
       "car_loan_70203": (70203, "Estimated Revenues", -9916),
       "charity_nonitemizers_70424": (70424, "Estimated Revenues", -8149),
       "remittance_excise_70604": (70604, "Estimated Revenues", 1089),
       "trump_accounts_70204": (70204, "Estimated Outlays", 3685)}
REMITTANCE = {"corridor_net_h2_bn": 58.794, "share": (0.40, 0.54, 0.65)}
OUTPUTS = ("tax_rows.csv", "tax_summary.json")
FULL_CLAIM = {"eitc_claim_prob_scale": {2024: 9e99}, "actc_claim_prob_scale": {2024: 9e99}}


def reform(**params):
    return {k: {2024: v} for k, v in params.items()}


def calc(df: pd.DataFrame, year: int, ref: dict | None, records=None):
    pol = tc.Policy()
    # Every record claims the EITC and the refundable child credit (the CPS tax model's convention), so that a
    # reform never moves a record across Tax-Calculator's random take-up draw.
    pol.implement_reform({**FULL_CLAIM, **(ref or {})})
    rec = records if records is not None else tc.Records(data=df.copy(), start_year=year, gfactors=None, weights=None,
                                                         adjust_ratios=None)
    c = tc.Calculator(policy=pol, records=rec, verbose=False)
    c.calc_all()
    return c.array("iitax"), c


def units(d: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray]:
    """One Tax-Calculator record per CPS tax unit; returns the records and each person's record index."""
    dep = d.DEP_STAT.gt(0)
    unauth = d.unauth.astype(bool)
    nd = d[~dep].sort_values(["TAX_ID", "A_LINENO"])
    head = nd.groupby("TAX_ID").head(1).set_index("TAX_ID")
    spouse = nd.groupby("TAX_ID").nth(1).set_index("TAX_ID")
    ids = head.index.to_numpy()
    sp = spouse.reindex(ids)
    has_sp = sp.PH_SEQ.notna().to_numpy()
    occ_frac = d.OCCUP.map(TIP_FRAC).fillna(0.0)
    tips = np.where(unauth, 0.0, occ_frac * (d.WSAL_VAL.clip(lower=0) + d.SEMP_VAL.clip(lower=0)))
    hours = d.HRSWK.astype(float)
    ot_ok = (d.PRERELG.eq(1) & d.A_HRLYWK.eq(1) & hours.gt(40) & d.A_CLSWKR.between(1, 4) & d.WKSWORK.gt(0)
             & d.WSAL_VAL.gt(0) & ~unauth)
    rate = d.WSAL_VAL / (d.WKSWORK * (40 + 1.5 * (hours - 40))).where(ot_ok, np.nan)
    overtime = np.where(ot_ok, 0.5 * rate * (hours - 40) * d.WKSWORK, 0.0)
    hh_ref = d.A_LINENO.eq(1)
    prop = np.where(hh_ref & d.H_TENURE.eq(1), PROPERTY_TAX_RATE * d.HPROP_VAL.clip(lower=0), 0.0)
    d = d.assign(tips=tips, overtime=np.nan_to_num(overtime), ot_rec=ot_ok.to_numpy(), prop=prop)
    by = d.groupby("TAX_ID")
    kids = d.assign(k17=dep & d.A_AGE.lt(17) & d.PRCITSHP.lt(5), k18=dep & d.A_AGE.lt(18), k6=dep & d.A_AGE.lt(6),
                    k19=dep & d.A_AGE.lt(19), eld=dep & d.A_AGE.ge(65)).groupby("TAX_ID")

    def tot(col):
        return by[col].sum().reindex(ids).to_numpy(float)

    def own(frame, col):
        return frame[col].to_numpy(float) if col in frame else np.zeros(len(ids))
    fs = head.FILESTAT.to_numpy()
    mars = np.where(has_sp, 2, np.where(fs == 4, 4, 1))
    age_h = np.where(head.unauth.to_numpy(bool) & (head.A_AGE.to_numpy() >= 65), 64, head.A_AGE.to_numpy())
    age_s = np.where(has_sp, np.where(sp.unauth.fillna(False).to_numpy(bool) & (sp.A_AGE.fillna(0).to_numpy() >= 65),
                                      64, sp.A_AGE.fillna(0).to_numpy()), 0)
    wp, ws = head.WSAL_VAL.clip(lower=0).to_numpy(float), np.nan_to_num(sp.WSAL_VAL.clip(lower=0).to_numpy(float))
    sp_semp = np.nan_to_num(sp.SEMP_VAL.to_numpy(float))
    sp_frse = np.nan_to_num(sp.FRSE_VAL.to_numpy(float))
    div = tot("DIV_VAL").clip(min=0)
    rec = pd.DataFrame({
        "RECID": np.arange(1, len(ids) + 1), "MARS": mars, "XTOT": by.size().reindex(ids).to_numpy(),
        "s006": head.pw_row4.to_numpy(float), "FLPDYR": 2024, "age_head": age_h, "age_spouse": age_s,
        "e00200p": wp, "e00200s": ws, "e00200": wp + ws,
        "e00900p": head.SEMP_VAL.to_numpy(float), "e00900s": sp_semp,
        "e00900": head.SEMP_VAL.to_numpy(float) + sp_semp,
        "e02100p": head.FRSE_VAL.to_numpy(float), "e02100s": sp_frse,
        "e02100": head.FRSE_VAL.to_numpy(float) + sp_frse,
        "e00300": tot("INT_VAL").clip(min=0), "e00600": div, "e00650": div * 0.0,
        "e01500": tot("PNSN_VAL").clip(min=0) + tot("ANN_VAL").clip(min=0),
        "e01700": tot("PNSN_VAL").clip(min=0) + tot("ANN_VAL").clip(min=0),
        "e02400": tot("SS_VAL").clip(min=0), "e02300": tot("UC_VAL").clip(min=0), "e02000": tot("RNT_VAL"),
        "n24": kids.k17.sum().reindex(ids).fillna(0).to_numpy(int),
        "nu18": kids.k18.sum().reindex(ids).fillna(0).to_numpy(int),
        "nu06": kids.k6.sum().reindex(ids).fillna(0).to_numpy(int),
        "EIC": np.minimum(kids.k19.sum().reindex(ids).fillna(0).to_numpy(int), 3),
        "elderly_dependents": kids.eld.sum().reindex(ids).fillna(0).to_numpy(int),
        "e18400": tot("STATETAX_B").clip(min=0), "e18500": tot("prop"),
        "tip_income": tot("tips"), "overtime_income": tot("overtime"),
    })
    rec["n21"] = rec.nu18
    rec["nu13"] = rec.nu06
    rec["ot_unit"] = by.ot_rec.any().reindex(ids).to_numpy(bool)
    rec["filer_ssn"] = (~by.apply(lambda g: g.loc[~g.DEP_STAT.gt(0), "unauth"].astype(bool).all())).reindex(ids
                                                                                                            ).to_numpy()
    idx = pd.Series(np.arange(len(ids)), index=ids)
    return rec, d.TAX_ID.map(idx).fillna(-1).astype(int).to_numpy()


def national_own_data():
    """TY2027 national cost of four provisions on Tax-Calculator's bundled CPS: current law vs reverted to 2024 law."""
    pol = tc.Policy()
    pol.set_year(2027)
    std27, ctc27 = pol.STD[0].tolist(), float(pol.CTC_c[0])
    pol.set_year(2025)
    std25 = pol.STD[0].tolist()
    reverts = {
        "senior_70103": {"SeniorDed_c": {2027: 0}},
        "ctc_2200_70104": {"CTC_c": {2027: 2000}},
        "std_increase_70102": {"STD": {2027: [s - inc * s / b for s, inc, b in zip(std27, STD_INCREASE_2025, std25)]}},
        "salt_cap_70120": {"ID_AllTaxes_c": {2027: [10000, 10000, 5000, 10000, 10000]},
                           "ID_AllTaxes_c_ps": {2027: [9e99] * 5}, "ID_AllTaxes_c_po_rate": {2027: 0.0},
                           "ID_AllTaxes_c_po_floor": {2027: [0, 0, 0, 0, 0]}},
    }
    out = {}
    base_rec = tc.Records.cps_constructor()
    b = tc.Calculator(policy=tc.Policy(), records=base_rec, verbose=False)
    b.advance_to_year(2027)
    b.calc_all()
    base = b.weighted_total("iitax")
    del b, base_rec
    gc.collect()
    for k, r in reverts.items():
        pol = tc.Policy()
        pol.implement_reform(r)
        c = tc.Calculator(policy=pol, records=tc.Records.cps_constructor(), verbose=False)
        c.advance_to_year(2027)
        c.calc_all()
        out[k] = (c.weighted_total("iitax") - base) / 1e9
        del c
        gc.collect()
    return out, {"std_2027": std27, "ctc_2027": ctc27}


def main() -> None:
    P.gate("taxcalc_version", tc.__version__ == TAXCALC_VERSION, version=tc.__version__)
    # National levels first, so their Records are freed before the CPS frame loads (peak memory).
    own, own_params = national_own_data()
    d = P.build_frame(INCOME_P, INCOME_H)
    civ, tgt = d.civ.to_numpy(), d.target.to_numpy()
    lw, r4 = d.pw.to_numpy(float), d.pw_row4.to_numpy(float)
    rec, pidx = units(d)
    inunit = pidx >= 0
    n_members = np.bincount(pidx[inunit], minlength=len(rec)).astype(float)
    # Units with no non-dependent member (dependents whose filer is outside the household) have no record.
    outside = float(r4[civ & ~inunit].sum() / r4[civ].sum())
    P.gate("persons_without_a_tax_record_under_1pct", outside < 0.01 and n_members.min() >= 1, outside=outside)
    pidx_safe = np.where(inunit, pidx, 0)
    # Units that lose the child credit under the SSN rule (post2024_law.py) get no child-credit increase.
    rec.loc[~rec.filer_ssn, ["n24"]] = 0
    unit_cols = [c for c in rec.columns if c not in ("ot_unit", "filer_ssn")]
    t2024 = rec[unit_cols]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        base, _ = calc(t2024, 2024, None)
        runs = {
            "tips_70201": reform(TipIncomeDed_c=25000),
            "overtime_70202": reform(OvertimeIncomeDed_c=[12500, 25000, 12500, 12500, 12500]),
            "senior_70103": reform(SeniorDed_c=6000),
            "ctc_2200_70104": reform(CTC_c=2200),
            "std_increase_70102": reform(STD=[14600 + 750, 29200 + 1500, 14600 + 750, 21900 + 1125, 29200 + 1500]),
            "salt_cap_70120": reform(ID_AllTaxes_c=[40000, 40000, 20000, 40000, 40000],
                                     ID_AllTaxes_c_ps=[500000, 500000, 250000, 500000, 500000],
                                     ID_AllTaxes_c_po_rate=0.3, ID_AllTaxes_c_po_floor=[10000, 10000, 5000, 10000,
                                                                                        10000]),
        }
        cut = {k: base - calc(t2024, 2024, r)[0] for k, r in runs.items()}
        # Car loans and giving are unobserved: a uniform amount, valued by each unit's tax rates.
        car = t2024.assign(auto_loan_interest=np.where(rec.filer_ssn, CAR_LOAN_INTEREST, 0.0))
        cut["car_loan_70203"] = (calc(car, 2024, None)[0]
                                 - calc(car, 2024, reform(AutoLoanInterestDed_c=10000))[0])
        give = t2024.assign(e19800=CASH_GIVING)
        cut["charity_nonitemizers_70424"] = (calc(give, 2024, None)[0] - calc(give, 2024, reform(
            STD_charity_ded_nonitemizers_max=[1000, 2000, 1000, 1000, 1000]))[0])
    shares, rows = {}, []
    for k, v in cut.items():
        P.gate(f"{k}_cuts_tax", v.min() >= -1.0, min=float(v.min()))
        per = np.where(inunit, v[pidx_safe] / n_members[pidx_safe], 0.0)
        mask = (rec.ot_unit.to_numpy()[pidx_safe] & inunit) if k == "overtime_70202" else np.ones(len(d), bool)
        nat = float((per * r4)[civ & mask].sum())
        lin = float((per * lw)[tgt & mask].sum())
        P.gate(f"{k}_national_positive", nat > 0, nat=nat)
        shares[k] = {"lineage_share": lin / nat, "cps_model_national_2024_bn": nat / 1e9,
                     "cps_model_lineage_2024_bn": lin / 1e9}
    # Trump accounts: citizen children aged 0 (born in the survey year stand for each year's births).
    infant = civ & d.A_AGE.eq(0).to_numpy() & d.PRCITSHP.lt(5).to_numpy()
    shares["trump_accounts_70204"] = {"lineage_share": float(lw[infant & tgt].sum() / r4[infant].sum())}
    jct_total = {}
    t7 = P.sheet_rows(P.CBO_LAW, "Title VII")
    for k, (sec, label, printed) in JCT.items():
        hits = [i for i, r in enumerate(t7) if any(str(c).strip() == str(sec) for c in r if c is not None)]
        vals = [P.cbo_row(t7[i:], sec, label)["2028"] for i in hits if any(
            label in str(c) for r2 in t7[i:i + 4] for c in r2[:3] if c is not None)]
        P.gate(f"jct_{k}_fy2028_printed", printed in vals, read=vals, printed=printed)
        jct_total[k] = printed / 1e3
    defl = P.deflators()[0]["2028"]
    cpi = P.deflators()[1]
    ty2027_defl = 1 / ((1 + cpi["2025"]) * (1 + cpi["2026"]) * (1 + cpi["2027"]))

    def row(item, nat_nominal, share, lo, hi, level, sign, deflator, note):
        lo, hi = sorted((lo, hi))
        rows.append({"item": item, "level_source": level, "national_nominal_bn": round(nat_nominal, 4),
                     "lineage_share": round(share, 6),
                     "lineage_2024usd_bn": round(sign * nat_nominal * share * deflator, 4),
                     "lineage_low_bn": round(sign * nat_nominal * (lo if sign > 0 else hi) * deflator, 4),
                     "lineage_high_bn": round(sign * nat_nominal * (hi if sign > 0 else lo) * deflator, 4),
                     "lapses_by_ty2030": item in ("tips_70201", "overtime_70202", "car_loan_70203", "senior_70103",
                                                  "trump_accounts_70204", "salt_cap_70120"),
                     "note": note})
    # Tax cuts to the lineage are positive; the remittance excise is a tax increase (negative).
    for k in ("tips_70201", "overtime_70202", "car_loan_70203", "charity_nonitemizers_70424"):
        s = shares[k]["lineage_share"]
        row(k, -jct_total[k], s, s, s, "JCT FY2028", 1, defl, "CPS proxy share x JCT score")
    for k in ("senior_70103", "ctc_2200_70104", "std_increase_70102", "salt_cap_70120"):
        s = shares[k]["lineage_share"]
        row(k, own[k], s, s, s, "Tax-Calculator own data TY2027", 1, ty2027_defl,
            "CPS share x Tax-Calculator national (JCT scores it only with TCJA extensions)")
    s = shares["trump_accounts_70204"]["lineage_share"]
    row("trump_accounts_70204", jct_total["trump_accounts_70204"], s, s, s, "CBO/JCT FY2028 outlays", 1, defl,
        "new transfer: $1,000 per citizen child born 2025-2028")
    rs = REMITTANCE["share"]
    row("remittance_excise_70604", jct_total["remittance_excise_70604"], rs[1], rs[0], rs[2], "JCT FY2028", -1, defl,
        "tax increase on cash-funded remittances; Mexico corridor less H-2 over JCT's implied base")
    P.gate("remittance_share_fits_base", REMITTANCE["corridor_net_h2_bn"] / (jct_total["remittance_excise_70604"]
                                                                              / 0.01) < 1)

    benefit = json.loads((OUT / "summary.json").read_text())["totals"]["2028"]["consolidated_government"]
    tax = {k: sum(float(r[k]) for r in rows) for k in ("lineage_2024usd_bn", "lineage_low_bn", "lineage_high_bn")}
    perm = {k: sum(float(r[k]) for r in rows if not r["lapses_by_ty2030"])
            for k in ("lineage_2024usd_bn", "lineage_low_bn", "lineage_high_bn")}
    net = {"central": benefit["lineage_2024usd_bn"] - tax["lineage_2024usd_bn"],
           "benefit_low_tax_high": benefit["lineage_low_bn"] - tax["lineage_high_bn"],
           "benefit_high_tax_low": benefit["lineage_high_bn"] - tax["lineage_low_bn"]}
    summary = {"lane": "post2024_law_2026_10_07", "part": "tax side", "taxcalc": tc.__version__,
               "fy": "2028", "deflator_fy2028": defl, "deflator_ty2027": ty2027_defl,
               "shares": shares, "national_tax_calculator_own_data_ty2027_bn": own, "own_data_params": own_params,
               "jct_fy2028_bn": jct_total, "tax_side_lineage_bn": tax, "tax_side_permanent_only_bn": perm,
               "benefit_cuts_consolidated_bn": benefit,
               "net_benefit_cuts_minus_tax_cuts_bn": net,
               "net_after_temporary_provisions_lapse_bn": benefit["lineage_2024usd_bn"] - perm["lineage_2024usd_bn"]}
    OUT.mkdir(exist_ok=True)
    with open(OUT / "tax_rows.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    (OUT / "tax_summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    for r in rows:
        print(f"  {r['item']:30s} ${r['lineage_2024usd_bn']:7.3f}bn share {r['lineage_share']:.4f} "
              f"(national {r['national_nominal_bn']:.2f}, {r['level_source']})")
    print(f"  ▸ tax side ${tax['lineage_2024usd_bn']:.2f}bn; benefit cuts ${benefit['lineage_2024usd_bn']:.2f}bn; "
          f"net ${net['central']:.2f}bn ({net['benefit_low_tax_high']:.2f} to {net['benefit_high_tax_low']:.2f}); "
          f"after the temporary provisions lapse ${summary['net_after_temporary_provisions_lapse_bn']:.2f}bn")


if __name__ == "__main__":
    main()
