"""Arm 2: taxes and credits by Hispanic ethnicity. The account's CPS tax-model keys, tabulated
for Hispanic tax-unit heads, against Treasury OTA's tax-record distributions.

OTA assigns imputed race and ethnicity to the primary filer and reports shares of tax units
("families") and of credit dollars including outlays [SOURCE: OTA Working Paper 122, Table 5,
printed p.29]. The CPS tax model puts a unit's tax variables on one record (the head, or a
dependent filer), so the account's personal key already follows the head, as OTA does.

The Mexican-origin translation scales the union's EITC and child-credit dollars inside the
refundable-credit key by OTA's Hispanic share over the CPS Hispanic share, credit by credit:
the CPS's Hispanic error is assumed proportional within Hispanics. Totals are held, so other
residents take up the difference. Writes derived/ota_shares.csv, derived/ota_translation.csv
and derived/ota_deltas.json (main-case translation via translate_main_case.js).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frame as f  # noqa: E402

# OTA WP-122 Table 5 (FY2023): Hispanic shares in whole percent (share bank) and the dollar bank.
OTA = {
    "families": (0.15, "WP-122 Table 5: Total Number of Families 100 / 67 / 15; 186m, Hispanic 28m"),
    "eitc_incl_outlay": (0.28, "WP-122 Table 5: Earned income tax credit (including outlay) 100 / 49 / 28; $67bn, Hispanic $19bn"),
    "ctc_incl_outlay": (0.22, "WP-122 Table 5: Child credit (including outlay) 100 / 66 / 22; $113bn, Hispanic $24bn"),
    "ptc_incl_outlay": (0.18, "WP-122 Table 5: Premium assistance tax credit (including outlays) 100 / 66 / 18; $36bn, Hispanic $6bn"),
    "pref_rates_cg_div": (0.03, "WP-122 Table 5: Preferential rates capital gains and dividends 100 / 92 / 3"),
    "families_2024": (27.9 / 184.5, "OTA 2024 family counts (Jan 14, 2025): All RH 184.5m, Hispanic 27.9m"),
}
ROUNDING = 0.005  # OTA shares are whole percents
MFJ_TAX = {"hispanic": 9477, "white": 28664, "all": 25798}  # WP-124 Table 3 "Total" rows, TY2023
NON_PTC_BN = 228.809 - 118.35  # refundable line less Treasury premium credits (audit row 1)
PTC_BN = 118.35
ON_BOOKS = {"central": 0.524, "low": 0.416, "high": 0.631}  # onbooks_share_2026_09_23 uniform equivalents


def heads(d):
    """One head per tax unit: the non-dependent record carrying the unit's tax variables, else
    the unit's first non-dependent line."""
    tax = (d.AGI.ne(0) | d.FEDTAX_BC.ne(0) | d.FEDTAX_AC.ne(0) | d.EIT_CRED.ne(0) | d.ACTC_CRD.ne(0)
           | d.CTC_CRD.ne(0)).to_numpy()
    nondep = d.DEP_STAT.eq(0).to_numpy()
    frame = pd.DataFrame({"tax_id": d.TAX_ID.to_numpy(), "line": d.A_LINENO.to_numpy(),
                          "carrier": tax & nondep, "nondep": nondep})
    frame = frame[frame.nondep]
    order = frame.sort_values(["tax_id", "carrier", "line"], ascending=[True, False, True])
    head_index = order.groupby("tax_id").head(1).index
    out = np.zeros(len(d), bool)
    out[head_index] = True
    return out


def share(v, w, mask, group):
    return float((v[mask & group] @ w[mask & group]) / (v[mask] @ w[mask]))


def main():
    d = f.load()
    W = f.weights(d)
    w = W[:, 0]
    civ, target = f.masks(d)
    hisp = d.PEHSPNON.eq(1).to_numpy()
    white = d.PRDTRACE.eq(1).to_numpy() & ~hisp
    head = heads(d)
    un, latin = f.status(d)
    unauth = un & latin  # the audit's rule set: Latin-American-born imputed unauthorized
    eitc = d.EIT_CRED.to_numpy(float)
    actc = d.ACTC_CRD.to_numpy(float)
    ctc_nonref = d.CTC_CRD.to_numpy(float)
    everyone = np.ones(len(d), bool)
    rows = []

    def add(item, cps_value, ota_item=None, note=""):
        ota_value = OTA[ota_item][0] if ota_item else np.nan
        rows.append(dict(item=item, cps_hispanic_share=cps_value, ota_hispanic_share=ota_value,
                         ota_source=OTA[ota_item][1] if ota_item else "", ratio_ota_to_cps=ota_value / cps_value
                         if ota_item else np.nan, note=note))

    add("tax_units_heads", share(np.ones(len(d)), w, head, hisp), "families",
        "CPS tax units incl. nonfilers, head's ethnicity; OTA FY2023 families incl. nonfilers with information returns")
    add("tax_units_heads_2024", share(np.ones(len(d)), w, head, hisp), "families_2024", "OTA 2024 count table")
    add("eitc_raw", share(eitc, w, everyone, hisp), "eitc_incl_outlay",
        "CPS tax model: every eligible unit claims; no SSN rule")
    add("ctc_incl_refundable_raw", share(ctc_nonref + actc, w, everyone, hisp), "ctc_incl_outlay",
        "CTC_CRD (nonrefundable incl. other-dependent credit) + ACTC_CRD")
    add("actc_raw", share(actc, w, everyone, hisp), None, "refundable part only; OTA does not split")
    add("eitc_ssn_rule", share(np.where(unauth, 0.0, eitc), w, everyone, hisp), "eitc_incl_outlay",
        "EITC zeroed for Latin-American-born imputed unauthorized (audit row 2 rule)")
    for label, ob in ON_BOOKS.items():
        c = np.where(unauth, (ctc_nonref + actc) * ob, ctc_nonref + actc)
        add(f"ctc_on_books_{label}", share(c, w, everyone, hisp), "ctc_incl_outlay",
            f"child credits of imputed unauthorized scaled by on-books share {ob}")
    subsidized = d.MRKS.eq(1).to_numpy().astype(float)
    add("subsidized_marketplace_persons", share(subsidized, w, civ, hisp), "ptc_incl_outlay",
        "CPS persons with subsidized Marketplace coverage last year; OTA premium credit dollars")
    add("dividends_plus_capital_gains", share((d.DIV_VAL + d.CAP_VAL).clip(lower=0).to_numpy(float), w, civ, hisp),
        "pref_rates_cg_div", "CPS dividends + capital gains; OTA tax expenditure of preferential rates")
    # The account's own keys, Hispanic share (context; OTA publishes no liability share).
    rk = f.receipt_keys(d)["personal"]
    for key in ["federal_liability", "state_liability", "wage", "consumption"]:
        add(f"account_key_{key}", share(rk[key], w, civ, hisp), None, "account key, civilian universe")
    add("account_key_refundable_credits", share(eitc + actc, w, civ, hisp), None, "EIT_CRED + ACTC_CRD")
    add("mexican_origin_share_of_hispanic_persons", float(w[civ & hisp & target].sum() / w[civ & hisp].sum()), None,
        "union members among civilian Hispanics")
    # WP-124: average income tax per married-joint return, Hispanic vs white primaries.
    mfj = head & d.FILESTAT.isin([1, 2, 3]).to_numpy()
    for col, label in [("FEDTAX_AC", "after_refundable"), ("FEDTAX_BC", "before_refundable")]:
        v = d[col].to_numpy(float)
        mh = (v[mfj & hisp] @ w[mfj & hisp]) / w[mfj & hisp].sum()
        mw = (v[mfj & white] @ w[mfj & white]) / w[mfj & white].sum()
        ma = (v[mfj] @ w[mfj]) / w[mfj].sum()
        rows.append(dict(item=f"mfj_avg_tax_{label}", cps_hispanic_share=mh / mw,
                         ota_hispanic_share=MFJ_TAX["hispanic"] / MFJ_TAX["white"] if label == "after_refundable" else np.nan,
                         ota_source="WP-124 Table 3 Total rows: Hispanic 9,477, White 28,664 (TY2023)",
                         ratio_ota_to_cps=(MFJ_TAX["hispanic"] / MFJ_TAX["white"]) / (mh / mw),
                         note=f"ratio of means; CPS 2024 means Hispanic {mh:,.0f}, white {mw:,.0f}, all {ma:,.0f}"))
    shares = pd.DataFrame(rows)
    f.OUT.mkdir(parents=True, exist_ok=True)
    shares.to_csv(f.OUT / "ota_shares.csv", index=False, lineterminator="\n")
    print(shares[["item", "cps_hispanic_share", "ota_hispanic_share", "ratio_ota_to_cps"]].round(4).to_string())

    # Translation onto the union's refundable-credit key (non-PTC part) and the PTC person key.
    hf = f.household_fraction(d, civ)
    get = dict(zip(shares.item, shares.ratio_ota_to_cps))
    trans, deltas = [], {}
    ids = d.SPM_ID.to_numpy()
    specs = {
        "vs_adopted_raw_keys": dict(eitc=get["eitc_raw"], ctc=get["ctc_incl_refundable_raw"], rule=False),
        "vs_audit_package_ssn_rule": dict(eitc=get["eitc_ssn_rule"], ctc=get["ctc_on_books_central"], rule=True),
    }
    for spec, s in specs.items():
        for a in ["personal", "shared"]:
            e_raw, c_raw = eitc, actc
            if s["rule"]:
                e_raw = np.where(unauth, 0.0, eitc)
                c_raw = np.where(unauth, actc * ON_BOOKS["central"], actc)
            e_v, c_v = (e_raw, c_raw) if a == "personal" else (f.unit_equal(e_raw, ids), f.unit_equal(c_raw, ids))
            total = (e_v + c_v)[civ] @ W[civ]
            g_e, g_c = e_v[target] @ W[target], c_v[target] @ W[target]
            base = (g_e + g_c) / total
            new = (s["eitc"] * g_e + s["ctc"] * g_c) / total
            change = NON_PTC_BN * hf * (new - base)
            trans.append(dict(spec=spec, line="refundable_tax_credits", key="refundable_credits", allocation=a,
                              national_bn=NON_PTC_BN, ratio_eitc=s["eitc"], ratio_ctc=s["ctc"],
                              account_share=float(base[0]), benchmarked_share=float(new[0]),
                              change_bn=float(change[0]), change_se_bn=f.sdr(change)))
            deltas.setdefault(spec, {"receipts": {}, "spending": {}})["spending"].setdefault(
                "refundable_tax_credits", {}).setdefault("refundable_credits", {})[a] = float(change[0])
    # Premium credits: row 1 keys them by the union's 10.9% of subsidized Marketplace persons; OTA
    # tests the person key's Hispanic share against dollars.
    r_ptc = get["subsidized_marketplace_persons"]
    union_ptc = share(subsidized, w, civ, target)
    change = PTC_BN * hf * union_ptc * (r_ptc - 1)
    trans.append(dict(spec="audit_row1_ptc_person_key", line="refundable_tax_credits (PTC part)",
                      key="subsidized_marketplace_persons", allocation="both", national_bn=PTC_BN,
                      ratio_eitc=np.nan, ratio_ctc=r_ptc, account_share=union_ptc,
                      benchmarked_share=union_ptc * r_ptc, change_bn=change, change_se_bn=np.nan))
    trans = pd.DataFrame(trans)
    trans.to_csv(f.OUT / "ota_translation.csv", index=False, lineterminator="\n")
    (f.OUT / "ota_deltas.json").write_text(json.dumps(deltas, indent=1) + "\n")
    done = subprocess.run(["node", str(f.HERE / "translate_main_case.js"), str(f.OUT / "ota_deltas.json"),
                           str(f.OUT / "ota_main_case.csv")], capture_output=True, text=True)
    print(done.stdout + done.stderr)
    if done.returncode:
        sys.exit(done.returncode)
    print(trans.round(4).to_string())


if __name__ == "__main__":
    main()
