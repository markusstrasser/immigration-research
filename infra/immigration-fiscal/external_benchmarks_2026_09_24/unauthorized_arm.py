"""Arm 3: the account's taxes for the imputed unauthorized, against outside anchors.

The account's receipts for a subgroup S on each line are national_bn x S's share of that line's
key (cbo_collective keys, as the builder allocates). They are computed raw (the published account,
every CPS wage on the books) and under the audit package's status rules (EITC zeroed; wages,
liabilities, FICA-worker flag and child credits scaled by the on-books share; onbooks_share
lane's uniform equivalent 0.524, range 0.416-0.631). Subgroups: imputed-unauthorized Mexico-born
union members, Latin-American-born, and all origins (status_impute_2026_09_16 via frame.status).

Anchors: ITEP (July 2024, 2022 taxes of 10.9m undocumented), SSA Actuarial Note 151 (2010 OASDI),
National Taxpayer Advocate 2024 (TY2022 ITIN returns). Writes derived/unauthorized_taxes.csv and
derived/unauthorized_anchors.csv.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frame as f  # noqa: E402

ON_BOOKS = {"central": 0.524, "low": 0.416, "high": 0.631}
NON_PTC_BN = 228.809 - 118.35
STATE_LOCAL_EXCISE_BN = 271.298  # BEA Table 3.5 line 23, inside excise_selective_sales (371.262)
FEDERAL_EXCISE_BN = 99.964       # BEA Table 3.5 line 4
# Tax type -> (line, key, fraction of the line) for the comparison with ITEP's categories.
TYPES = {
    "federal_income_tax_gross": [("federal_income_tax", "federal_liability", 1.0)],
    "payroll_oasdi": [("employee_oasdi", "wage_oasdi", 1.0), ("employer_oasdi", "wage_oasdi", 1.0),
                      ("self_employment_oasdi_hi", "self_payroll", .124 / .153)],
    "payroll_hi": [("employee_hi", "wage", 1.0), ("employer_hi", "wage", 1.0),
                   ("self_employment_oasdi_hi", "self_payroll", .029 / .153)],
    "other_social_contributions_ui": [("other_domestic_social_contributions", "positive_fica_worker", 1.0)],
    "state_local_income_tax": [("state_local_income_tax", "state_liability", 1.0),
                               ("other_personal_tax", "state_liability", 1.0)],
    "state_local_sales_excise": [("general_sales_tax", "consumption", 1.0),
                                 ("excise_selective_sales", "consumption", STATE_LOCAL_EXCISE_BN / 371.262)],
    "federal_excise_customs": [("excise_selective_sales", "consumption", FEDERAL_EXCISE_BN / 371.262),
                               ("customs_duties", "consumption", 1.0)],
    "motor_vehicle_fees": [("personal_motor_vehicle", "adults", 1.0)],
}
# ITEP, "Tax Payments by Undocumented Immigrants" (July 2024), 2022, 10.9m people; pages printed.
ITEP = {
    "population_m": (10.9, "p.4"), "total_bn": (96.7, "p.3"), "federal_bn": (59.4, "p.3"),
    "state_local_bn": (37.3, "p.3"), "federal_income_tax_net": (19.5, "p.5 Figure 1"),
    "payroll_oasdi": (25.7, "p.6 Figure 2"), "payroll_hi": (6.4, "p.6 Figure 2"),
    "other_social_contributions_ui": (1.8, "p.6 Figure 2, state and federal UI"),
    "state_local_sales_excise": (15.1, "p.7 Figure 3"), "state_local_income_tax": (7.0, "p.7 Figure 3"),
    "state_local_property": (10.4, "p.7 Figure 3"), "misc_federal": (7.6, "p.5 Figure 1"),
}


# SSA national average wage index [SOURCE: ssa.gov/oact/cola/AWI.html, Wayback 2026 capture, saved
# as _cache/arm3b/awi_plain.html]: indexes 2010 and 2022 anchors to 2024 wages.
AWI = {2010: 41673.83, 2022: 63795.13, 2024: 69846.57}


def subgroup_share(v, W, civ, s):
    return (v[s] @ W[s]) / (v[civ] @ W[civ])


def main():
    d = f.load()
    W = f.weights(d)
    w = W[:, 0]
    civ, target = f.masks(d)
    hf = f.household_fraction(d, civ)
    un, latin = f.status(d)
    mexico = d.PENATVTY.eq(303).to_numpy()
    groups = {"unauthorized_mexico_born_union": un & latin & mexico & target,
              "unauthorized_latin_american_born": un & latin & civ,
              "unauthorized_all_origins": un & civ}
    lines = {l["id"]: l for l in f.model()["receipts"]["lines"]}
    rk = f.receipt_keys(d)
    eitc, actc = d.EIT_CRED.to_numpy(float), d.ACTC_CRD.to_numpy(float)
    rows = []
    for label, s in groups.items():
        people = w[s].sum()
        for rule in ["raw", "on_books_central", "on_books_low", "on_books_high"]:
            ob = None if rule == "raw" else ON_BOOKS[rule.split("_")[-1]]
            # The audit's rules apply to the Latin-American-born imputed unauthorized only.
            scaled = un & latin
            for a in ["personal", "shared"]:
                keys = dict(rk[a])
                if ob is not None:
                    base = rk["personal"]
                    for k in ["federal_liability", "state_liability", "wage", "wage_oasdi", "self_payroll",
                              "positive_fica_worker"]:
                        v = np.where(scaled, base[k] * ob, base[k])
                        keys[k] = v if a == "personal" else f.unit_equal(v, d.SPM_ID.to_numpy())
                for tax_type, parts in TYPES.items():
                    amount = sum(lines[l]["national_bn"] * frac * subgroup_share(keys[k], W, civ, s)
                                 for (l, k, frac) in parts)
                    rows.append(dict(group=label, people_m=people / 1e6, rule=rule, allocation=a,
                                     tax_type=tax_type, account_bn=float(amount[0]), account_se_bn=f.sdr(amount),
                                     per_person=float(amount[0]) * 1e9 / people))
                # Refundable credits (non-PTC part of BEA line 25), keyed by EITC + ACTC.
                e = eitc if ob is None else np.where(scaled, 0.0, eitc)
                c = actc if ob is None else np.where(scaled, actc * ob, actc)
                v = e + c if a == "personal" else f.unit_equal(e + c, d.SPM_ID.to_numpy())
                credit = NON_PTC_BN * hf * subgroup_share(v, W, civ, s)
                rows.append(dict(group=label, people_m=people / 1e6, rule=rule, allocation=a,
                                 tax_type="refundable_credits_eitc_actc", account_bn=float(credit[0]),
                                 account_se_bn=f.sdr(credit), per_person=float(credit[0]) * 1e9 / people))
    out = pd.DataFrame(rows)
    f.OUT.mkdir(parents=True, exist_ok=True)
    out.to_csv(f.OUT / "unauthorized_taxes.csv", index=False, lineterminator="\n")

    # Side-by-side with ITEP per person (2022, and indexed to 2024 by SSA's average wage index) and
    # with SSA's 2010 OASDI estimate indexed the same way.
    anchors = []
    pivot = out.pivot_table(index=["group", "rule", "allocation"], columns="tax_type", values="per_person")
    for (group, rule, a), r in pivot.iterrows():
        fit_net = r["federal_income_tax_gross"] - r["refundable_credits_eitc_actc"]
        for item, account, source, value, year in [
                ("federal_income_tax_net_of_eitc_actc", fit_net, "ITEP p.5", ITEP["federal_income_tax_net"][0], 2022),
                ("payroll_oasdi", r["payroll_oasdi"], "ITEP p.6", ITEP["payroll_oasdi"][0], 2022),
                ("payroll_oasdi", r["payroll_oasdi"], "SSA Note 151 p.3 ($13bn, 10.8m)", 13.0 / 10.8 * 10.9, 2010),
                ("payroll_oasdi", r["payroll_oasdi"], "PWBM 2025 ($24bn, 11m)", 24.0 / 11.0 * 10.9, 2024),
                ("payroll_hi", r["payroll_hi"], "ITEP p.6", ITEP["payroll_hi"][0], 2022),
                ("other_social_contributions_ui", r["other_social_contributions_ui"], "ITEP p.6",
                 ITEP["other_social_contributions_ui"][0], 2022),
                ("state_local_income_tax", r["state_local_income_tax"], "ITEP p.7", ITEP["state_local_income_tax"][0], 2022),
                ("state_local_sales_excise", r["state_local_sales_excise"], "ITEP p.7",
                 ITEP["state_local_sales_excise"][0], 2022)]:
            per = value / ITEP["population_m"][0] * 1e3  # $bn over 10.9m (SSA, PWBM rescaled to 10.9m)
            indexed = per * AWI[2024] / AWI[year]
            anchors.append(dict(group=group, rule=rule, allocation=a, item=item, source=source, source_year=year,
                                account_per_person=account, anchor_per_person=per, anchor_per_person_2024=indexed,
                                account_over_anchor_2024=account / indexed))
    anchors = pd.DataFrame(anchors)
    anchors.to_csv(f.OUT / "unauthorized_anchors.csv", index=False, lineterminator="\n")
    # Union's imputed-unauthorized Mexico-born: dollar gap to each anchor (people x per-person gap).
    people = w[groups["unauthorized_mexico_born_union"]].sum()
    gap = anchors.query("group == 'unauthorized_mexico_born_union' and allocation == 'personal'").copy()
    gap["anchor_minus_account_bn"] = (gap.anchor_per_person_2024 - gap.account_per_person) * people / 1e9
    gap.to_csv(f.OUT / "unauthorized_gap_mexico_born.csv", index=False, lineterminator="\n")
    ages = {k: float(w[s & d.A_AGE.lt(18).to_numpy()].sum() / w[s].sum()) for k, s in groups.items()}
    print("share under 18:", {k: round(v, 3) for k, v in ages.items()})
    print(gap.pivot_table(index=["item", "source"], columns="rule", values="anchor_minus_account_bn").round(2).to_string())
    print(anchors.drop_duplicates(["item", "source"])[["item", "source", "anchor_per_person",
                                                         "anchor_per_person_2024"]].round(0).to_string())
    agg = out.query("allocation == 'personal'").pivot_table(index=["group", "rule"], columns="tax_type", values="account_bn")
    print(agg.round(2).to_string())
    print(out.drop_duplicates("group")[["group", "people_m"]].to_string())


if __name__ == "__main__":
    main()
