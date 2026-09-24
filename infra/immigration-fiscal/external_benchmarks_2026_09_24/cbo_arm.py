"""Arm 1: the account's receipt and transfer keys on all CPS households, against CBO's
distribution of household income (publication 61911, January 2026, data year 2022).

For each CBO concept the account's key is tabulated by CBO-style income group (quintiles of
people ranked by size-adjusted income before transfers and taxes, the top quintile split into
81-90, 91-95, 96-99 and the top 1 percent, households with negative income apart). The target
share of a key is s = sum_j pi_j * theta_j: pi_j is group j's share of the national key, theta_j
the Mexican-origin union's share of the key inside group j. Replacing pi_j by CBO's share keeps
the group's own position inside each income group and moves only the income gradient:
s' = sum_j pi'_j * theta_j. The change in the group's dollars is national_bn x (s' - s), times
the household pool fraction for spending lines, as in the account's builders.

Writes derived/cbo_group_shares.csv, derived/cbo_translation.csv, derived/cbo_ranking_check.csv
and derived/cbo_deltas.json (read by translate_main_case.js).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frame as f  # noqa: E402

CBO_ROOT = f.CACHE / "arm1"
CBO_DIR = CBO_ROOT / "cbo61911_data/61911-additional-data-for-researchers/CBO_distribution_household_income_2022_data"
CBO_FIGURES = CBO_ROOT / "61911-data-underlying-figures.xlsx"
CBO_ZIP_SHA = "703c3f8c768d00ab283a586b943b1e364b3de481c18b75a00453b765a3fd99d6"
NAMES = {"lowest_quintile": "q1", "second_quintile": "q2", "middle_quintile": "q3", "fourth_quintile": "q4",
         "highest_quintile": "q5", "percentiles_81_90": "p81_90", "percentiles_91_95": "p91_95",
         "percentiles_96_99": "p96_99", "top_1_percent": "top1", "all_quintiles": "all"}
QUINTILES = ["q1", "q2", "q3", "q4", "q5"]
YEARS = [2022, 2019, 2018]
# Medicaid line: LTSS dollars at 2024 scale, which the LTSS lane re-keys (audit row 5); CBO's
# household Medicaid excludes people in institutions, so only the community remainder is moved.
LTSS_BN = 264.7  # [SOURCE: ltss_share_2026_09_23/RESULT.md verdict]


def table(number, name, ranking="inc_before_trans_tax"):
    path = CBO_DIR / f"households_ranked_by_{ranking}_table_{number:02d}_{name}_1979_2022.csv"
    t = pd.read_csv(path)
    t = t[t.household_type.eq("all_households")].copy()
    t["group"] = t.income_group.map(NAMES)
    if t.group.isna().any():
        raise ValueError(f"Unmapped CBO income group in {path.name}")
    return t


def refundable_credit_pct(year):
    """Figure 15: average refundable credits as a percentage of income before transfers and taxes,
    lowest, second and middle quintiles (the only groups CBO publishes)."""
    ws = openpyxl.load_workbook(CBO_FIGURES, read_only=True, data_only=True)["Figure 15"]
    for row in ws.iter_rows(values_only=True):
        if row and row[0] == year:
            return dict(zip(["q1", "q2", "q3"], [v / 100 for v in row[1:4]]))
    raise ValueError(f"Figure 15 has no {year} row")


def cbo_shares(year):
    """Fractions of each concept by CBO group; 'negative' is the residual CBO leaves unshown."""
    out = {}
    for number, name, columns in [(12, "federal_tax_shares", ["federal_taxes", "individual_inc_tax", "payroll_taxes",
                                                              "corporate_inc_tax", "excise_taxes"]),
                                  (11, "means_tested_transfer_shares", ["means_tested_transfers", "medicaid_and_chip",
                                                                        "snap", "ssi", "other_transfers"]),
                                  (10, "household_income_shares", ["market_inc", "inc_before_transfers_taxes"])]:
        t = table(number, name).query("year == @year").set_index("group")
        for c in columns:
            out[c] = t[c] / 100
    demo = table(1, "demographics").query("year == @year").set_index("group")
    comp = table(5, "components_ibtt").query("year == @year").set_index("group")
    taxes = table(7, "components_federal_taxes").query("year == @year").set_index("group")
    hh = demo.num_households
    for c in ["social_security", "medicare", "unemployment_insurance", "workers_compensation"]:
        dollars = comp[c] * hh
        out[c] = dollars / dollars["all"]
    # Individual income tax before refundable credits: CBO's net tax plus Figure 15's credits for
    # the three quintiles it publishes; none added above them ("gross") or Q3's dollars per household
    # added to Q4 as an upper bound ("gross_q4").
    credits = refundable_credit_pct(year)
    net = taxes.individual_inc_tax * hh
    for label, q4 in [("individual_inc_tax_gross", False), ("individual_inc_tax_gross_q4", True)]:
        add = pd.Series(0.0, index=net.index)
        for q, pct in credits.items():
            add[q] = pct * comp.loc[q, "inc_before_transfers_taxes"] * hh[q]
        if q4:
            add["q4"] = add["q3"] / hh["q3"] * hh["q4"]
        add["all"] = add[["q1", "q2", "q3", "q4"]].sum()
        out[label] = (net + add) / (net["all"] + add["all"])
    frame = pd.DataFrame(out)
    frame.loc["negative"] = 1 - frame.loc[QUINTILES].sum()
    frame["people"] = (demo.num_people / demo.num_people["all"]).reindex(frame.index)
    frame["households"] = (hh / hh["all"]).reindex(frame.index)
    return frame


def groups(d, w=None):
    medicare_bn = next(l for l in f.model()["spending"]["lines"] if l["id"] == "medicare")["national_bn"]
    weight = d.pwwgt0.to_numpy(float) if w is None else w
    enrollees = weight[d.MCARE.eq(1).to_numpy()].sum()
    per = medicare_bn * 1e9 / enrollees
    return f.cbo_groups(d, f.cbo_income(d, per), weight)


def decompose(v, W, civ, target, g):
    """pi[j] = group j's share of the national key; theta[j] = target share inside group j.
    W may be a vector (point) or n x 161 (replicates); outputs follow."""
    total = v[civ] @ W[civ]
    pi, theta = {}, {}
    for j in f.GROUPS:
        m = civ & (g == j)
        gj = v[m] @ W[m]
        tj = v[m & target] @ W[m & target]
        pi[j] = gj / total
        theta[j] = np.divide(tj, gj, out=np.zeros_like(np.asarray(tj, float)), where=np.asarray(gj) != 0)
    return pi, theta


def reweighted_share(pi, theta):
    return sum(pi[j] * theta[j] for j in f.GROUPS)


def cbo_detail(cbo, column, pi_negative):
    """CBO fractions on the lane's groups (Q5 split into its four published parts).

    CBO leaves negative-income households unshown, so its residual mixes them with the rounding of
    five cells. The eight positive groups are renormalized to the CPS key's positive-income mass and
    the negative group keeps its CPS share: both sides then compare households with income >= 0.
    """
    positive = [j for j in f.GROUPS if j != "negative"]
    total = sum(float(cbo.loc[j, column]) for j in positive)
    out = {j: float(cbo.loc[j, column]) / total * (1 - pi_negative) for j in positive}
    out["negative"] = pi_negative
    return out


def ratio_target(pi_line, pi_composite, cbo):
    """Scale a line's group shares by CBO / composite, renormalized (keeps line differences)."""
    raw = {j: (pi_line[j] * cbo[j] / pi_composite[j] if pi_composite[j] != 0 else cbo[j]) for j in f.GROUPS}
    total = sum(raw.values())
    return {j: raw[j] / total for j in f.GROUPS}


# Concept -> account lines (id, key, side, national share used) compared with that CBO column.
CONCEPTS = {
    "individual_inc_tax": [("federal_income_tax", "federal_liability", "receipts", None)],
    "payroll_taxes": [("employee_oasdi", "wage_oasdi", "receipts", None), ("employee_hi", "wage", "receipts", None),
                      ("self_employment_oasdi_hi", "self_payroll", "receipts", None),
                      ("employer_oasdi", "wage_oasdi", "receipts", None), ("employer_hi", "wage", "receipts", None)],
    "excise_taxes": [("excise_selective_sales", "consumption", "receipts", "federal_excise")],
    "corporate_inc_tax": [("corporate_capital", "capital", "receipts", None), ("corporate_labor", "wage", "receipts", None)],
    "medicaid_and_chip": [("medicaid_and_chip_other_medical", "medicaid", "spending", "community")],
    "snap": [("snap", "snap", "spending", None)],
    "ssi": [("ssi", "ssi", "spending", None)],
    "other_transfers": [("family_and_general_assistance", "cash_assistance", "spending", None),
                        ("energy_assistance", "energy", "spending", None),
                        ("other_state_welfare", "wic", "spending", None),
                        ("housing_subsidies", "housing_support", "spending", None)],
    "social_security": [("social_security", "social_security", "spending", None),
                        ("railroad_retirement", "social_security", "spending", None)],
    "medicare": [("medicare", "medicare", "spending", None)],
    "unemployment_insurance": [("unemployment", "unemployment", "spending", None)],
    "workers_compensation": [("workers_compensation", "workers_comp", "spending", None)],
    # Sensitivity: CBO's federal-excise distribution applied to every consumption-keyed receipt line
    # (state-local sales and excise, customs, personal transfers), which CBO does not distribute.
    "excise_all_consumption_lines": [("general_sales_tax", "consumption", "receipts", None),
                                     ("excise_selective_sales", "consumption", "receipts", None),
                                     ("customs_duties", "consumption", "receipts", None),
                                     ("personal_current_transfers", "consumption", "receipts", None)],
}
# CBO columns compared with each concept; the income-tax line gets three definitions of CBO's tax.
VARIANTS = {"individual_inc_tax": ["individual_inc_tax_gross", "individual_inc_tax", "individual_inc_tax_gross_q4"],
            "excise_all_consumption_lines": ["excise_taxes"]}
# CBO rounds household averages to $100; UI ($200) and workers' compensation ($100) are too coarse
# to distribute (their group shares sum to 1.3 and 0.8). Tabulated, never translated.
UNTESTABLE = {"unemployment_insurance", "workers_compensation"}
FEDERAL_EXCISE_BN = 99.964  # BEA Table 3.5 line 4, 2024 (pinned workbook), inside the 371.262 line
# Lines whose change enters the main case one for one (direct receipts, household transfers).
IN_MAIN_CASE = {"federal_income_tax", "employee_oasdi", "employee_hi", "self_employment_oasdi_hi", "employer_oasdi",
                "employer_hi", "excise_selective_sales", "general_sales_tax", "customs_duties",
                "personal_current_transfers", "medicaid_and_chip_other_medical", "snap", "ssi",
                "family_and_general_assistance", "energy_assistance", "other_state_welfare", "social_security",
                "railroad_retirement", "medicare", "unemployment", "workers_compensation"}


def national_amount(line, part):
    if part == "federal_excise":
        return FEDERAL_EXCISE_BN
    if part == "community":
        return line["national_bn"] - LTSS_BN
    return line["national_bn"]


def main():
    if f.sha(CBO_ROOT / "61911-additional-data-for-researchers.zip") != CBO_ZIP_SHA:
        raise ValueError("Unreviewed CBO researcher file")
    d = f.load()
    civ, target = f.masks(d)
    W = f.weights(d)
    w = W[:, 0]
    hf = f.household_fraction(d, civ)
    g, adjusted = groups(d)
    m = f.model()
    lines = {l["id"]: l for l in m["receipts"]["lines"]}
    lines.update({l["id"]: l for l in m["spending"]["lines"]})
    rk, sk = f.receipt_keys(d), f.spending_keys(d)
    vec = {side: {a: (rk if side == "receipts" else sk)[a] for a in ["personal", "shared"]}
           for side in ["receipts", "spending"]}

    # Ranking check: CPS income, people and households by group against CBO.
    cbo = {y: cbo_shares(y) for y in YEARS}
    hh_first = ~pd.Series(d.PH_SEQ).duplicated().to_numpy()
    check = []
    for j in f.GROUPS:
        mj = g == j
        check.append(dict(group=j, cps_people_share=w[mj].sum() / w.sum(),
                          cps_household_share=w[mj & hh_first].sum() / w[hh_first].sum(),
                          cps_ibtt_share=float(np.nan),
                          target_people_share_of_group=w[mj & target].sum() / w[mj & civ].sum(),
                          group_share_of_target=w[mj & target].sum() / w[target].sum(),
                          cbo2022_people_share=cbo[2022].loc[j, "people"] if j in cbo[2022].index else np.nan,
                          cbo2022_ibtt_share=cbo[2022].loc[j, "inc_before_transfers_taxes"]))
    medicare_bn = lines["medicare"]["national_bn"]
    per = medicare_bn * 1e9 / w[d.MCARE.eq(1).to_numpy()].sum()
    ibtt = f.cbo_income(d, per)
    for row in check:
        mj = g == row["group"]
        row["cps_ibtt_share"] = (ibtt[mj] @ w[mj]) / (ibtt @ w)
    check = pd.DataFrame(check)

    group_rows, trans_rows, component_rows, deltas, spec_reps = [], [], [], {}, {}
    for concept, members in CONCEPTS.items():
        variants = VARIANTS.get(concept, [concept])
        # Composite distribution of the account's lines (dollar-weighted), for ratio scaling.
        pis = {}
        for (lid, key, side, part) in members:
            v = vec[side]["personal"][key]
            pis[lid], _ = decompose(v, w, civ, target, g)
        amounts = {lid: national_amount(lines[lid], part) for (lid, key, side, part) in members}
        comp = {j: sum(amounts[l] * pis[l][j] for l in pis) / sum(amounts.values()) for j in f.GROUPS}
        for year in YEARS:
            for variant in variants:
                spec = f"{concept}|{year}" if variant == concept else f"{concept}={variant}|{year}"
                target_cbo = cbo_detail(cbo[year], variant, comp["negative"])
                for j in f.GROUPS:
                    group_rows.append(dict(spec=spec, concept=concept, cbo_column=variant, year=year,
                                           group=j, account_share=comp[j], cbo_share=target_cbo[j],
                                           cbo_share_published=float(cbo[year].loc[j, variant]),
                                           gap_pp=100 * (target_cbo[j] - comp[j]),
                                           translated=concept not in UNTESTABLE))
                if concept in UNTESTABLE:
                    continue
                for (lid, key, side, part) in members:
                    line = lines[lid]
                    amount = national_amount(line, part)
                    scale = hf if side == "spending" else 1.0
                    pi_point = pis[lid]
                    pi_new = target_cbo if len(members) == 1 else ratio_target(pi_point, comp, target_cbo)
                    for a in ["personal", "shared"]:
                        v = vec[side][a][key]
                        pi_r, th_r = decompose(v, W, civ, target, g)
                        s_r = reweighted_share(pi_r, th_r)
                        # Replicates: the CBO target is fixed; for ratio scaling each replicate
                        # rescales its own line shares by the point composite ratio.
                        if len(members) == 1:
                            s_new_r = sum(target_cbo[j] * th_r[j] for j in f.GROUPS)
                        else:
                            s_new_r = sum(pi_new[j] / pi_point[j] * pi_r[j] * th_r[j] if pi_point[j] else 0
                                          for j in f.GROUPS)
                        change = amount * scale * (s_new_r - s_r)
                        trans_rows.append(dict(spec=spec, concept=concept, cbo_column=variant, year=year, line=lid,
                                               key=key, side=side, allocation=a, national_bn=amount,
                                               pool_fraction=scale, account_share=float(s_r[0]),
                                               reweighted_share=float(s_new_r[0]),
                                               change_bn=float(change[0]), change_se_bn=f.sdr(change),
                                               in_main_case=lid in IN_MAIN_CASE))
                        if year == YEARS[0] and variant == variants[0]:
                            for j in f.GROUPS:
                                component_rows.append(dict(line=lid, key=key, allocation=a, group=j,
                                                           key_share_pi=float(pi_r[j][0]),
                                                           target_share_theta=float(th_r[j][0]),
                                                           target_dollars_bn=float(amount * scale * pi_r[j][0] * th_r[j][0])))
                        if lid in IN_MAIN_CASE:
                            # Cost to other residents: group receipts down or transfers up raise it.
                            cost = -change if side == "receipts" else change
                            spec_reps[(spec, a)] = spec_reps.get((spec, a), 0) + cost
                            method = deltas.setdefault(spec, {"receipts": {}, "spending": {}})
                            if side == "receipts":
                                method["receipts"].setdefault(lid, {})[a] = float(change[0])
                            else:
                                method["spending"].setdefault(lid, {}).setdefault(key, {})[a] = float(change[0])
                        elif side == "receipts":
                            # Corporate cells are not direct in the engine (capital response), so
                            # their main-case effect is the engine's own, reported without the
                            # linear-sum gate below.
                            deltas.setdefault(spec, {"receipts": {}, "spending": {}})["receipts"].setdefault(
                                lid, {})[a] = float(change[0])
                # Medicaid with coverage inside income groups: CBO's income gradient for dollars, the
                # union's share of CPS Medicaid-covered persons (the account's alternative key) inside
                # each group, against the published MEPS-key allocation.
                if concept == "medicaid_and_chip":
                    lid, key, side, part = members[0]
                    amount = national_amount(lines[lid], part)
                    for a in ["personal", "shared"]:
                        pi_m, th_m = decompose(vec[side][a][key], W, civ, target, g)
                        _, th_c = decompose(vec[side][a]["medicaid_covered"], W, civ, target, g)
                        s_m = reweighted_share(pi_m, th_m)
                        s_c = sum(target_cbo[j] * th_c[j] for j in f.GROUPS)
                        change = amount * hf * (s_c - s_m)
                        spec_c = f"{concept}=coverage_theta|{year}"
                        spec_reps[(spec_c, a)] = change
                        trans_rows.append(dict(spec=spec_c, concept=concept, cbo_column=variant, year=year, line=lid,
                                               key=key, side=side, allocation=a, national_bn=amount, pool_fraction=hf,
                                               account_share=float(s_m[0]), reweighted_share=float(s_c[0]),
                                               change_bn=float(change[0]), change_se_bn=f.sdr(change),
                                               in_main_case=True))
                        deltas.setdefault(spec_c, {"receipts": {}, "spending": {}})["spending"].setdefault(
                            lid, {}).setdefault(key, {})[a] = float(change[0])
    f.OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(component_rows).to_csv(f.OUT / "cbo_components.csv", index=False, lineterminator="\n")
    pd.DataFrame(group_rows).to_csv(f.OUT / "cbo_group_shares.csv", index=False, lineterminator="\n")
    trans = pd.DataFrame(trans_rows)
    trans.to_csv(f.OUT / "cbo_translation.csv", index=False, lineterminator="\n")
    check.to_csv(f.OUT / "cbo_ranking_check.csv", index=False, lineterminator="\n")
    # Bundles for the main case: every translated concept at its central definition.
    central = {"individual_inc_tax": "individual_inc_tax=individual_inc_tax_gross"}
    bundle_concepts = ["individual_inc_tax", "payroll_taxes", "excise_taxes", "medicaid_and_chip", "snap", "ssi",
                       "other_transfers", "social_security", "medicare"]
    for year in YEARS:
        bundle = {"receipts": {}, "spending": {}}
        for concept in bundle_concepts:
            spec = f"{central.get(concept, concept)}|{year}"
            for side in ["receipts", "spending"]:
                for lid, val in deltas[spec][side].items():
                    if side == "receipts":
                        bundle[side][lid] = val
                    else:
                        bundle[side].setdefault(lid, {}).update(val)
        deltas[f"all_concepts|{year}"] = bundle
        deltas[f"all_but_medicaid|{year}"] = {"receipts": bundle["receipts"],
                                              "spending": {k: v for k, v in bundle["spending"].items()
                                                           if k != "medicaid_and_chip_other_medical"}}
        wide = json.loads(json.dumps(bundle))
        wide["receipts"].update(deltas[f"excise_all_consumption_lines=excise_taxes|{year}"]["receipts"])
        deltas[f"all_concepts_excise_on_all_consumption_lines|{year}"] = wide
        for a in ["personal", "shared"]:
            parts = {c: spec_reps[(f"{central.get(c, c)}|{year}", a)] for c in bundle_concepts}
            spec_reps[(f"all_concepts|{year}", a)] = sum(parts.values())
            spec_reps[(f"all_but_medicaid|{year}", a)] = sum(v for c, v in parts.items() if c != "medicaid_and_chip")
            spec_reps[(f"all_concepts_excise_on_all_consumption_lines|{year}", a)] = (
                sum(parts.values()) - parts["excise_taxes"]
                + spec_reps[(f"excise_all_consumption_lines=excise_taxes|{year}", a)])
    (f.OUT / "cbo_deltas.json").write_text(json.dumps(deltas, indent=1) + "\n")
    done = subprocess.run(["node", str(f.HERE / "translate_main_case.js"), str(f.OUT / "cbo_deltas.json"),
                           str(f.OUT / "cbo_main_case.csv")], capture_output=True, text=True)
    print(done.stdout + done.stderr)
    if done.returncode:
        sys.exit(done.returncode)
    # Main-case change per spec with its replicate SE (lines summed within each replicate). Every
    # translated line enters the main case one for one, so the sum must equal the engine's change.
    node = pd.read_csv(f.OUT / "cbo_main_case.csv").query("profile == 'cbo_category_lag_non_school_full'")
    node = node.set_index("method")
    rows = []
    for (s, a), r in spec_reps.items():
        engine = node.loc[s, "change_low_bn" if a == "shared" else "change_high_bn"]
        if abs(engine - r[0]) > 2e-3:
            raise ValueError(f"[BLOCKED] linear sum {r[0]:.4f} != engine {engine:.4f} for {s}/{a}")
        rows.append(dict(spec=s, allocation=a, band_end="low" if a == "shared" else "high",
                         main_case_change_bn=float(r[0]), main_case_change_se_bn=f.sdr(r)))
    pd.DataFrame(rows).to_csv(f.OUT / "cbo_spec_totals.csv", index=False, lineterminator="\n")
    summary = trans.query("year == 2022").groupby(["spec", "allocation"]).change_bn.sum().unstack()
    print(summary.round(2).to_string())


if __name__ == "__main__":
    main()
