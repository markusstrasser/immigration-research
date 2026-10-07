"""Social Security and Medicare Part A on an accrual basis for the white slices, beside the cash re-key.

The pension lane (pension_accrual_2026_09_28) is imported read-only and run at its central settings (payable benefits,
entry-age attribution, the Trustees' new-issue rates, general mortality, Note 2025.7 ratios by the age-adjusted career
level) on two CPS groups of its frame: the Mexican-origin union and the third-plus NH white reference (`WHITE`).
Gates: the union's OASDI accrual per tax dollar (payable 1.018378, scheduled 1.297788), its Part A accrual
($41.137bn) and its benefit-tax timing (0.083884) reproduce the lane's stored values.

For each group: OASDI accrual per dollar of OASDI tax, net of the income tax the accrued benefits will carry; Part A
accrual per dollar of HI tax. These ratios are applied to the re-key's own OASDI and HI tax lines (derived/
rekey_line_shares.csv), and the re-key's 2024 Social Security and Part A cash lines are removed, as the pension lane
does for the engine's union. Outputs: derived/accrual_ratios.csv, derived/accrual_beside.csv.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.dont_write_bytecode = True   # read-only imports from other lanes: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
DER = LANE / "derived"
sys.path.insert(0, str(FISCAL / "pension_accrual_2026_09_28"))
import pension_accrual as P  # noqa: E402

SS = P.ss
WHITE_REL_RATE = 1.0     # whites' 2024 income tax on benefits relative to the nation's [INFERENCE: they draw ~3/4 of
                         # benefits, so their rate is close to the national one; not measured with Tax-Calculator]
STORED = dict(payable=1.018378, scheduled=1.297788, part_a=41.137128, timing=0.08388440990158708,
              rel_union=0.5233824966647924, cur_rate_union=0.03174001912172151, cur_rate_nation=0.06064402100563528,
              receipt_low=2.091206, ss_cash_low=56.258695)
G = (P.CENTRAL["rate"], P.CENTRAL["mortality"])


def oasdi_ratio(q, grids, u_long, taus, scens=None):
    """Per-person central accrual (both scenarios) and the benefit-tax timing, as pension_accrual.central_accrual."""
    fam = SS.family_vector(q, "observed_family")
    level = P.career_levels(q, P.CENTRAL["mapping"])
    lvl = np.clip(level, P.MODEL_LEVELS[0], P.MODEL_LEVELS[-1])
    birth = np.clip(SS.INCOME_YEAR - q.age.to_numpy(), P.BIRTHS[0], P.BIRTHS[-1]).astype(float)
    entry = np.where(q.mexico_born & q.arrival_age.notna(), q.arrival_age.fillna(21), 21.0)
    w, tax = q.w.to_numpy(), q.tax_oasdi.to_numpy()
    out = {}
    for scen in scens or P.SCENARIOS:
        fac = P.model_factor(grids[scen], P.CENTRAL["method"], G, fam, entry, birth, lvl, q.age.to_numpy().astype(float))
        acc = tax * P.note_mwr(q, P.S.mwr_table(P.MWR_TABLE[scen]), level, fam) * fac * np.where(q.unauth, u_long, 1.0)
        tau = P.person_tau(taus, fam, birth)[(G, scen)]
        out[scen] = dict(ratio=float((w * acc).sum() / (w * tax).sum()),
                         timing=float((w * acc * tau).sum() / (w * acc).sum()), tax_bn=float((w * tax).sum() / 1e9))
    return out


def part_a(u, econ, u_long, scen):
    """pension_accrual.hi_accrual's central (own sex, no spouse credit) for a group, generation by generation."""
    w = u.w.to_numpy()
    covered = (u.tax_hi > 0).to_numpy()
    pq = np.zeros(len(u))
    start = np.where(u.mexico_born & u.arrival_age.notna(), np.maximum(u.arrival_age.fillna(21), 21), 21).astype(int)
    n_years = np.zeros(len(u))
    for g in sorted(u.gen.unique()):
        m = (u.gen == g).to_numpy()
        old = m & (u.age >= 65).to_numpy() & ~u.unauth.to_numpy()
        pq[m] = float(np.average((u.MCARE == 1).to_numpy()[old], weights=w[old]))
        wt = pd.Series(w[m]).groupby(u.age.to_numpy()[m]).sum()
        num = pd.Series(covered[m] * w[m]).groupby(u.age.to_numpy()[m]).sum()
        cov = (num / wt).reindex(range(0, 91)).fillna(0.0).to_numpy()
        n_years[m] = [cov[s:65].sum() for s in start[m]]
    own = P.part_a_pv(u.age.to_numpy(), u.sex.to_numpy(), econ, P.CENTRAL["rate"], scen, P.CENTRAL["mortality"])
    base = np.where(covered & (u.age < 65).to_numpy() & (n_years > 0), pq * own / np.maximum(n_years, 1e-9), 0.0)
    acc = base * u.onbooks.to_numpy() * np.where(u.unauth.to_numpy(), u_long, 1.0)
    return dict(accrual_bn=float((w * acc).sum() / 1e9), hi_tax_bn=float((w * u.tax_hi.to_numpy()).sum() / 1e9),
                p_qualify=float(np.average(pq[(u.age >= 65).to_numpy()], weights=w[(u.age >= 65).to_numpy()])))


def main():
    q = P.S.quotes()
    u_long = q["note151_eligible_share"]["value"]["end_of_projection"]
    part_a_share = q["mtr_benefits_2024_bn"]["value"]["hi"] / q["mtr_benefits_2024_bn"]["value"]["total"]
    p = P.frame()
    econ = P.L.Economy()
    prelim = P.S.scaled_factors().preliminary.to_numpy()
    P.GRID = [G, P.BASE]            # only the central run and Note 2025.7's own basis (the factor's normalizer)
    grids = {s: P.model_grid(econ, prelim, P.payable_path(econ) if s == "payable" else None) for s in P.SCENARIOS}
    share = P.tob_share_path() * (1 + P.hi_over_oasdi_tob()) * P.obbba_factor()
    taus = P.tob_timing(econ, prelim, share, runs=[(G, s) for s in P.SCENARIOS])
    white = p.copy()
    white["union"] = white[P.WHITE].to_numpy()
    white["gen"] = np.where(white.union, "W3", "")
    groups = {"union": p, "third_plus_nh_white": white}
    ratios = {}
    for name, frame in groups.items():
        qq = frame[frame.union & (frame.tax_oasdi > 0)].reset_index(drop=True)
        o = oasdi_ratio(qq, grids, u_long, taus)
        a = {s: part_a(frame[frame.union].copy(), econ, u_long, s) for s in P.SCENARIOS}
        ratios[name] = (o, a)
        print(f"{name}: OASDI accrual per tax dollar payable {o['payable']['ratio']:.6f} scheduled "
              f"{o['scheduled']['ratio']:.6f}; timing {o['payable']['timing']:.6f}; Part A payable "
              f"{a['payable']['accrual_bn']:.3f}bn on HI tax {a['payable']['hi_tax_bn']:.3f}bn")
    o, a = ratios["union"]
    for k, got in (("payable", o["payable"]["ratio"]), ("scheduled", o["scheduled"]["ratio"]),
                   ("part_a", a["payable"]["accrual_bn"]), ("timing", o["payable"]["timing"])):
        if abs(got - STORED[k]) > 1e-5 * max(1, abs(STORED[k])):
            raise SystemExit(f"[BLOCKED] the union's {k} does not reproduce the pension lane: {got} vs {STORED[k]}")
    print("[gate] union ratios, Part A accrual and benefit-tax timing reproduce the pension lane")
    rel = {"union": STORED["rel_union"], "third_plus_nh_white": WHITE_REL_RATE}
    # the case's receipt side loses the tax on 2024 benefits: the union's stored receipt per dollar of benefits at its
    # rate, carried to each group at its relative rate (the HI part rides in the same ratio)
    receipt_per_ben = STORED["receipt_low"] / (STORED["ss_cash_low"] * STORED["rel_union"])
    rows = []
    for name, (o, a) in ratios.items():
        for scen in P.SCENARIOS:
            rows.append({"group": name, "scenario": scen, "oasdi_per_tax_dollar": f"{o[scen]['ratio']:.6f}",
                         "benefit_tax_timing": f"{o[scen]['timing']:.6f}", "relative_benefit_tax_rate": f"{rel[name]:.6f}",
                         "future_share": f"{rel[name] * o[scen]['timing']:.6f}",
                         "oasdi_per_tax_dollar_net": f"{o[scen]['ratio'] * (1 - rel[name] * o[scen]['timing']):.6f}",
                         "part_a_per_hi_tax_dollar": f"{a[scen]['accrual_bn'] / a[scen]['hi_tax_bn']:.6f}",
                         "cps_oasdi_tax_bn": f"{o[scen]['tax_bn']:.4f}", "cps_hi_tax_bn": f"{a[scen]['hi_tax_bn']:.4f}",
                         "part_a_accrual_bn": f"{a[scen]['accrual_bn']:.4f}",
                         "p_qualify_65plus": f"{a[scen]['p_qualify']:.6f}"})
    with open(DER / "accrual_ratios.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)

    # Beside the re-key: each scenario's OASDI / HI tax and Social Security / Medicare lines at the low end (the old-age
    # lines are identical at both ends in the re-key, and their responses are 1).
    ls = pd.read_csv(DER / "rekey_line_shares.csv").set_index("line")
    summ = pd.read_csv(DER / "rekey_summary.csv")
    ratio_of = {"mexican_origin_rough": "union"}
    beside = []
    for col in [c for c in ls.columns if c.startswith("share_") and "engine" not in c]:
        lab = col[len("share_"):]
        grp = ratio_of.get(lab, "third_plus_nh_white" if "white" in lab else None)
        if grp is None:
            continue
        amt = ls.national_bn * ls[col]
        se = amt["self_employment_oasdi_hi"]
        oasdi_part = 0.124 / (0.124 + 0.029)     # statutory SE split [SOURCE: TR 2025 Table V.C6]
        oasdi_tax = amt["employee_oasdi"] + amt["employer_oasdi"] + oasdi_part * se
        hi_tax = amt["employee_hi"] + amt["employer_hi"] + (1 - oasdi_part) * se
        ss_cash, pa_cash = amt["social_security"], part_a_share * amt["medicare"]
        o, a = ratios[grp]
        for scen in P.SCENARIOS:
            fs = rel[grp] * o[scen]["timing"]
            acc_net = o[scen]["ratio"] * (1 - fs) * oasdi_tax
            receipt = receipt_per_ben * rel[grp] * ss_cash
            pa_acc = a[scen]["accrual_bn"] / a[scen]["hi_tax_bn"] * hi_tax
            d = (acc_net - ss_cash + receipt) + (pa_acc - pa_cash)
            for end in ("low", "high"):
                cash = float(summ[(summ.group == lab) & (summ.end == end)].cost.iloc[0])
                beside.append({"group": lab, "scenario": scen, "end": end, "cost_cash_bn": f"{cash:.4f}",
                               "oasdi_tax_bn": f"{oasdi_tax:.4f}", "oasdi_accrual_net_bn": f"{acc_net:.4f}",
                               "ss_cash_bn": f"{ss_cash:.4f}", "benefit_tax_receipt_bn": f"{receipt:.4f}",
                               "hi_tax_bn": f"{hi_tax:.4f}", "part_a_accrual_bn": f"{pa_acc:.4f}",
                               "part_a_cash_bn": f"{pa_cash:.4f}", "delta_accrual_minus_cash_bn": f"{d:.4f}",
                               "cost_accrual_bn": f"{cash + d:.4f}",
                               "cost_accrual_per_member": f"{(cash + d) * 1e9 / 40_896_574.152351856:.0f}"})
    b = pd.DataFrame(beside)
    for (scen, end), g in b.groupby(["scenario", "end"]):
        u = float(g[g.group == "mexican_origin_rough"].cost_accrual_bn.iloc[0])
        b.loc[g.index, "delta_like_for_like_accrual_bn"] = [f"{u - float(x):.4f}" for x in g.cost_accrual_bn]
    b.to_csv(DER / "accrual_beside.csv", index=False, lineterminator="\n")
    print(b[["group", "scenario", "end", "cost_cash_bn", "delta_accrual_minus_cash_bn", "cost_accrual_bn",
             "delta_like_for_like_accrual_bn"]].to_string(index=False))


def main_oct07():
    """--case oct07 (main case v6, item 1): the payable ratios of the union and the third-plus NH white reference on the
    pension accrual's 2026 path, the arm all_2026_inputs_separate_funds of pension_tr2026_2026_10_06 that the case's
    meta.pension_accrual takes (tr2026_path.py rebuilds its grid, timing and Part A path through that lane's code), by
    this script's oasdi_ratio and part_a. The case's scheduled-benefits arm stays on the 2025 reports, so only the payable
    scenario is written; the relative benefit-tax rates are the 2025 run's (measured on 2024 benefits).
    Gates ([BLOCKED], nothing written): the case payload's ratio_net and Part A accrual are the arm's union row of
    arms.csv (tr2026_path.case_check); the union here reproduces that row's OASDI accrual per tax dollar, benefit-tax
    timing and Part A accrual (5e-9, arms.csv's printed precision). Output: derived/accrual_ratios_oct07.csv
    (accrual_ratios.csv's columns), read by rekey_sept29.py --case oct07."""
    import json
    import tr2026_path as TP
    TP.case_check(json.loads((FISCAL / "main_case_2026_10_07/derived/corrections.json").read_text())["meta"])
    q = P.S.quotes()
    u_long = q["note151_eligible_share"]["value"]["end_of_projection"]
    p = P.frame()
    prelim = P.S.scaled_factors().preliminary.to_numpy()
    econ, grid, taus, paths = TP.payable(P, prelim)
    white = p.copy()
    white["union"] = white[P.WHITE].to_numpy()
    white["gen"] = np.where(white.union, "W3", "")
    ratios = {}
    for name, frame in (("union", p), ("third_plus_nh_white", white)):
        qq = frame[frame.union & (frame.tax_oasdi > 0)].reset_index(drop=True)
        with TP.on_path(P, paths):
            o = oasdi_ratio(qq, {"payable": grid}, u_long, taus, scens=("payable",))["payable"]
            a = part_a(frame[frame.union].copy(), econ, u_long, "payable")
        ratios[name] = (o, a)
        print(f"{name} (2026 path): OASDI accrual per tax dollar payable {o['ratio']:.9f}; timing {o['timing']:.9f}; "
              f"Part A payable {a['accrual_bn']:.9f}bn on HI tax {a['hi_tax_bn']:.9f}bn")
    o, a = ratios["union"]
    row = TP.union_row()
    for k, got, col in (("OASDI accrual per tax dollar", o["ratio"], "per_tax_dollar"), ("timing", o["timing"], "timing"),
                        ("Part A accrual", a["accrual_bn"], "part_a_bn"), ("HI tax", a["hi_tax_bn"], "hi_tax_bn")):
        if abs(got - float(row[col])) > 5e-9 * max(1.0, abs(float(row[col]))):
            raise SystemExit(f"[BLOCKED] the union's {k} {got} does not reproduce {TP.ARM}'s {col} {row[col]}")
    print(f"[gate] the union's ratio, timing and Part A accrual reproduce {TP.ARM}'s union row of arms.csv")
    rel = {"union": STORED["rel_union"], "third_plus_nh_white": WHITE_REL_RATE}
    rows = [{"group": name, "scenario": "payable", "oasdi_per_tax_dollar": f"{o['ratio']:.6f}",
             "benefit_tax_timing": f"{o['timing']:.6f}", "relative_benefit_tax_rate": f"{rel[name]:.6f}",
             "future_share": f"{rel[name] * o['timing']:.6f}",
             "oasdi_per_tax_dollar_net": f"{o['ratio'] * (1 - rel[name] * o['timing']):.6f}",
             "part_a_per_hi_tax_dollar": f"{a['accrual_bn'] / a['hi_tax_bn']:.6f}",
             "cps_oasdi_tax_bn": f"{o['tax_bn']:.4f}", "cps_hi_tax_bn": f"{a['hi_tax_bn']:.4f}",
             "part_a_accrual_bn": f"{a['accrual_bn']:.4f}", "p_qualify_65plus": f"{a['p_qualify']:.6f}"}
            for name, (o, a) in ratios.items()]
    with open(DER / "accrual_ratios_oct07.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)
    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--case", default="sept29", choices=["sept29", "oct07"],
                    help="sept29 (default: the 2025 reports, which the sept29 and oct05 cases read) or oct07 (main_oct07)")
    main() if ap.parse_args().case == "sept29" else main_oct07()
