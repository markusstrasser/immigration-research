"""Social Security and Medicare Part A accrual per tax dollar for non-Hispanic Black residents (the sept29 re-key).

The v4 case (main_case_2026_09_29) books the pension promises that accrue while members work instead of the benefits
paid in 2024. rekey_sept29.py applies that rule to every group at the group's own accrual per tax dollar. The white
lane has the union's and the third-plus NH white ratios (white_replacement_2026_09_28/accrual_white.py); this script
adds the NH Black group's.

The pension lane (pension_accrual_2026_09_28) is imported read-only and run at its central settings (payable benefits,
entry-age attribution, the Trustees' new-issue rates, general mortality, Note 2025.7 ratios by the age-adjusted career
level), as accrual_white.py runs it. The group is its CPS frame's persons with PEHSPNON 2 and PRDTRACE 2 (the Black
lane's group), matched on PH_SEQ and A_LINENO. Entry: the lane starts a Mexico-born member's career at arrival and
everyone else's at 21; here every foreign-born member starts at arrival (PEINUSYR midpoints, the lane's own map), the
same rule applied to the group's immigrants. The arm with every member at 21 is written beside. The same run for all
residents (relative benefit-tax rate 1 by definition) prices the white lane's all-residents benchmark slice.

The relative benefit-tax rate (the group's 2024 federal income tax on benefits per benefit dollar, over the nation's)
is not measured for the group: the pension lane ran Tax-Calculator for the union only (0.523382). A statutory proxy
(section 86 thresholds on tax-unit income other than benefits, the 2024 bracket rate at the unit's taxable income)
is computed for the nation, the union, the group and the third-plus NH white reference; the group's rate is its proxy
relative rate scaled by the union's measured / proxy ratio [INFERENCE].

Gates (each stops with [BLOCKED]): the union's OASDI accrual per tax dollar (payable 1.018378, scheduled 1.297788), its
Part A accrual ($41.137bn) and its benefit-tax timing (0.083884) reproduce the pension lane with this script's entry
code. Outputs: derived/accrual_ratios.csv, derived/benefit_tax_proxy.csv. Run from the repository root (about 3 min):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/black_comparator_rough_2026_09_28/accrual_black.py

--case oct07 (main case v6, item 1) prices the same groups on the pension accrual's 2026 path, the arm
all_2026_inputs_separate_funds of pension_tr2026_2026_10_06 that the case's meta.pension_accrual takes (the white
lane's tr2026_path.py rebuilds its grid, timing and Part A path through that lane's code), payable only (the case's
scheduled-benefits arm stays on the 2025 reports), at the same relative benefit-tax rates. Gates: the case payload's
ratio_net and Part A accrual are the arm's union row of the 2026 lane's arms.csv, and the union here reproduces that
row's OASDI accrual per tax dollar, timing, Part A accrual and HI tax (5e-9). Output: derived/accrual_ratios_oct07.csv
(benefit_tax_proxy.csv is the 2025 run's: the proxy does not read the path).
"""
from __future__ import annotations

import contextlib
import csv
import importlib.util
import json
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True   # read-only imports from other lanes: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
DER = LANE / "derived"
ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
sys.path.insert(0, str(FISCAL / "pension_accrual_2026_09_28"))
import pension_accrual as P  # noqa: E402

SS = P.ss
STORED = dict(payable=1.018378, scheduled=1.297788, part_a=41.137128, timing=0.08388440990158708,
              rel_union=0.5233824966647924)   # the pension lane's union values (accrual_white.py STORED)
G = (P.CENTRAL["rate"], P.CENTRAL["mortality"])
US = [57, 60, 66, 69, 73, 78]
# 2024 federal brackets, upper limits of taxable income [SOURCE: IRS Rev. Proc. 2023-34]
BRACKETS = {"single": [(11_600, .10), (47_150, .12), (100_525, .22), (191_950, .24), (243_725, .32), (609_350, .35)],
            "joint": [(23_200, .10), (94_300, .12), (201_050, .22), (383_900, .24), (487_450, .32), (731_200, .35)]}
TOP_RATE = 0.37
# Section 86 base amounts: 50% tier from T1, 85% tier from T2 [SOURCE: 26 USC 86(c)]
THRESHOLDS = {"single": (25_000, 34_000), "joint": (32_000, 44_000)}


def oasdi_ratio(q, grids, u_long, taus, scens=None):
    """accrual_white.oasdi_ratio with the entry age as a column (q.entry); scens: the scenarios (all by default)."""
    fam = SS.family_vector(q, "observed_family")
    level = P.career_levels(q, P.CENTRAL["mapping"])
    lvl = np.clip(level, P.MODEL_LEVELS[0], P.MODEL_LEVELS[-1])
    birth = np.clip(SS.INCOME_YEAR - q.age.to_numpy(), P.BIRTHS[0], P.BIRTHS[-1]).astype(float)
    entry = q.entry.to_numpy(float)
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
    """accrual_white.part_a with the career start as a column (u.start)."""
    w = u.w.to_numpy()
    covered = (u.tax_hi > 0).to_numpy()
    pq = np.zeros(len(u))
    start = u.start.to_numpy().astype(int)
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


def bracket_rate(ti, joint):
    out = np.full(len(ti), TOP_RATE)
    for kind, mask in (("single", ~joint), ("joint", joint)):
        r = np.full(len(ti), TOP_RATE)
        for lim, rate in reversed(BRACKETS[kind]):
            r = np.where(ti <= lim, rate, r)
        out = np.where(mask, r, out)
    return out


def benefit_tax_proxy():
    """Statutory proxy of each person's 2024 federal income tax on Social Security benefits; rate per benefit dollar by
    group. Tax unit (PH_SEQ, TAX_ID): benefits and income other than benefits (PTOTVAL less SS_VAL) summed; joint when
    a member's FILESTAT is 1-3; taxable benefits by section 86; the unit's bracket rate at its TAX_INC (10% when the
    unit has taxable benefits but no taxable income); each member keeps the part proportional to own benefits."""
    cols = ["PH_SEQ", "TAX_ID", "MARSUPWT", "A_AGE", "PRPERTYP", "PEHSPNON", "PRDTRACE", "PRCITSHP", "PENATVTY",
            "PEFNTVTY", "PEMNTVTY", "PRDTHSP", "SS_VAL", "PTOTVAL", "TAX_INC", "FILESTAT"]
    with zipfile.ZipFile(ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=cols)
    w = (d.MARSUPWT / 100 * (d.PRPERTYP.eq(2) | d.A_AGE.lt(15))).to_numpy(float)
    native = d.PRCITSHP.isin([1, 2, 3])
    pus = d.PEFNTVTY.isin(US) & d.PEMNTVTY.isin(US)
    groups = {"nation": np.ones(len(d), bool),
              "union": ((d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)) | (native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)))
                        | (native & pus & d.PRDTHSP.eq(1))).to_numpy(),
              "nh_black": (d.PEHSPNON.eq(2) & d.PRDTRACE.eq(2)).to_numpy(),
              "third_plus_nh_white": (native & pus & d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1)).to_numpy()}
    u = d.groupby(["PH_SEQ", "TAX_ID"])
    ss = d.SS_VAL.clip(lower=0).to_numpy(float)
    ss_u = u.SS_VAL.transform(lambda s: s.clip(lower=0).sum()).to_numpy(float)
    other = np.maximum(u.PTOTVAL.transform("sum").to_numpy(float) - ss_u, 0.0)
    joint = u.FILESTAT.transform("min").isin([1, 2, 3]).to_numpy()
    t1 = np.where(joint, THRESHOLDS["joint"][0], THRESHOLDS["single"][0])
    t2 = np.where(joint, THRESHOLDS["joint"][1], THRESHOLDS["single"][1])
    pi = other + 0.5 * ss_u
    taxable = np.where(pi <= t1, 0.0, np.where(pi <= t2, np.minimum(0.5 * ss_u, 0.5 * (pi - t1)),
                       np.minimum(0.85 * ss_u, 0.85 * (pi - t2) + np.minimum(0.5 * ss_u, 0.5 * (t2 - t1)))))
    ti = np.maximum(u.TAX_INC.transform("sum").to_numpy(float), 0.0)
    rate = np.where(ti > 0, bracket_rate(ti, joint), np.where(taxable > 0, 0.10, 0.0))
    own = np.divide(ss, ss_u, out=np.zeros(len(d)), where=ss_u > 0)
    btax = taxable * rate * own
    out = {g: dict(benefits_bn=float((w * ss)[m].sum() / 1e9), benefit_tax_bn=float((w * btax)[m].sum() / 1e9))
           for g, m in groups.items()}
    for g in out:
        out[g]["rate"] = out[g]["benefit_tax_bn"] / out[g]["benefits_bn"]
    for g in out:
        out[g]["relative_rate_proxy"] = out[g]["rate"] / out["nation"]["rate"]
    scale = STORED["rel_union"] / out["union"]["relative_rate_proxy"]
    for g in out:
        out[g]["relative_rate_calibrated"] = out[g]["relative_rate_proxy"] * scale
    return out


def tr2026_path():
    """The white lane's tr2026_path.py (the oct07 path), loaded by file so that lane's modules stay off sys.path."""
    spec = importlib.util.spec_from_file_location("tr2026_path", FISCAL / "white_replacement_2026_09_28/tr2026_path.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main(case="sept29"):
    proxy = benefit_tax_proxy()
    for g, v in proxy.items():
        print(f"benefit-tax proxy {g:20s} rate {v['rate']:.5f} relative {v['relative_rate_proxy']:.4f} "
              f"calibrated {v['relative_rate_calibrated']:.4f}")
    rel = {"union": STORED["rel_union"], "nh_black": proxy["nh_black"]["relative_rate_calibrated"], "all_residents": 1.0}

    q = P.S.quotes()
    u_long = q["note151_eligible_share"]["value"]["end_of_projection"]
    p = P.frame()
    with zipfile.ZipFile(ZIP) as z:
        race = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "A_LINENO", "PEHSPNON", "PRDTRACE"])
    m = p[["PH_SEQ", "A_LINENO"]].merge(race, on=["PH_SEQ", "A_LINENO"], how="left", validate="one_to_one")
    if m.PEHSPNON.isna().any():
        raise SystemExit("[BLOCKED] pension-frame persons without a CPS race record")
    black = (m.PEHSPNON.eq(2) & m.PRDTRACE.eq(2)).to_numpy()
    mid = P.entry_midpoints()
    arrival_any = p.age - (2024.5 - p.PEINUSYR.map(mid))
    foreign = p.PRCITSHP.isin([4, 5]).to_numpy()
    prelim = P.S.scaled_factors().preliminary.to_numpy()
    if case == "oct07":             # the 2026 path, payable only; Part A under the path's patches
        TP = tr2026_path()
        TP.case_check(json.loads((FISCAL / "main_case_2026_10_07/derived/corrections.json").read_text())["meta"])
        econ, grid, taus, paths = TP.payable(P, prelim)
        grids, scens = {"payable": grid}, ("payable",)
        on_path = lambda: TP.on_path(P, paths)  # noqa: E731
    else:
        econ = P.L.Economy()
        P.GRID = [G, P.BASE]        # only the central run and Note 2025.7's own basis (the factor's normalizer)
        grids = {s: P.model_grid(econ, prelim, P.payable_path(econ) if s == "payable" else None) for s in P.SCENARIOS}
        share = P.tob_share_path() * (1 + P.hi_over_oasdi_tob()) * P.obbba_factor()
        taus = P.tob_timing(econ, prelim, share, runs=[(G, s) for s in P.SCENARIOS])
        scens, on_path = P.SCENARIOS, contextlib.nullcontext

    def frame_for(mask, entry_rule):
        f = p.copy()
        f["union"] = mask
        if entry_rule != "lane":            # the union keeps the lane's generations (Medicare take-up by generation)
            f["gen"] = np.where(mask, "B", "")
        if entry_rule == "lane":            # the pension lane's own rule (Mexico-born at arrival)
            arr = f.arrival_age
            imm = f.mexico_born.to_numpy() & arr.notna().to_numpy()
        elif entry_rule == "immigrants_at_arrival":
            arr = arrival_any
            imm = foreign & arr.notna().to_numpy()
        else:                               # everyone at 21
            arr = arrival_any
            imm = np.zeros(len(f), bool)
        f["entry"] = np.where(imm, arr.fillna(21), 21.0)
        f["start"] = np.where(imm, np.maximum(arr.fillna(21), 21), 21).astype(int)
        return f

    runs = {("union", "lane"): frame_for(p.union.to_numpy(), "lane"),
            ("nh_black", "immigrants_at_arrival"): frame_for(black, "immigrants_at_arrival"),
            ("nh_black", "all_at_21"): frame_for(black, "all_at_21"),
            ("all_residents", "immigrants_at_arrival"): frame_for(np.ones(len(p), bool), "immigrants_at_arrival")}
    res = {}
    for (name, rule), frame in runs.items():
        qq = frame[frame.union & (frame.tax_oasdi > 0)].reset_index(drop=True)
        with on_path():
            o = oasdi_ratio(qq, grids, u_long, taus, scens)
            a = {s: part_a(frame[frame.union].copy(), econ, u_long, s) for s in scens}
        res[(name, rule)] = (o, a)
        sched = f" scheduled {o['scheduled']['ratio']:.6f}" if "scheduled" in o else ""
        print(f"{name} ({rule}): persons {frame.w[frame.union].sum() / 1e6:.2f}M; OASDI accrual per tax dollar payable "
              f"{o['payable']['ratio']:.6f}{sched}; timing {o['payable']['timing']:.6f}; "
              f"Part A payable {a['payable']['accrual_bn']:.3f}bn on HI tax {a['payable']['hi_tax_bn']:.3f}bn")
    o, a = res[("union", "lane")]
    if case == "oct07":
        row = TP.union_row()
        for k, got, col in (("OASDI accrual per tax dollar", o["payable"]["ratio"], "per_tax_dollar"),
                            ("timing", o["payable"]["timing"], "timing"),
                            ("Part A accrual", a["payable"]["accrual_bn"], "part_a_bn"),
                            ("HI tax", a["payable"]["hi_tax_bn"], "hi_tax_bn")):
            if abs(got - float(row[col])) > 5e-9 * max(1.0, abs(float(row[col]))):
                raise SystemExit(f"[BLOCKED] the union's {k} {got} does not reproduce {TP.ARM}'s {col} {row[col]}")
        print(f"[gate] the union's ratio, timing and Part A accrual reproduce {TP.ARM}'s union row of arms.csv")
    else:
        for k, got in (("payable", o["payable"]["ratio"]), ("scheduled", o["scheduled"]["ratio"]),
                       ("part_a", a["payable"]["accrual_bn"]), ("timing", o["payable"]["timing"])):
            if abs(got - STORED[k]) > 1e-5 * max(1, abs(STORED[k])):
                raise SystemExit(f"[BLOCKED] the union's {k} does not reproduce the pension lane: {got} vs {STORED[k]}")
        print("[gate] union ratios, Part A accrual and benefit-tax timing reproduce the pension lane")

    rows = []
    for (name, rule), (o, a) in res.items():
        for scen in scens:
            r = rel[name]
            rows.append({"group": name, "entry_rule": rule, "scenario": scen,
                         "oasdi_per_tax_dollar": f"{o[scen]['ratio']:.6f}",
                         "benefit_tax_timing": f"{o[scen]['timing']:.6f}", "relative_benefit_tax_rate": f"{r:.6f}",
                         "future_share": f"{r * o[scen]['timing']:.6f}",
                         "oasdi_per_tax_dollar_net": f"{o[scen]['ratio'] * (1 - r * o[scen]['timing']):.6f}",
                         "part_a_per_hi_tax_dollar": f"{a[scen]['accrual_bn'] / a[scen]['hi_tax_bn']:.6f}",
                         "cps_oasdi_tax_bn": f"{o[scen]['tax_bn']:.4f}", "cps_hi_tax_bn": f"{a[scen]['hi_tax_bn']:.4f}",
                         "part_a_accrual_bn": f"{a[scen]['accrual_bn']:.4f}",
                         "p_qualify_65plus": f"{a[scen]['p_qualify']:.6f}"})
    with open(DER / ("accrual_ratios_oct07.csv" if case == "oct07" else "accrual_ratios.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)
    if case == "oct07":
        print(pd.DataFrame(rows)[["group", "entry_rule", "scenario", "oasdi_per_tax_dollar", "oasdi_per_tax_dollar_net",
                                  "part_a_per_hi_tax_dollar", "p_qualify_65plus"]].to_string(index=False))
        return
    with open(DER / "benefit_tax_proxy.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=["group", "benefits_bn", "benefit_tax_bn", "rate", "relative_rate_proxy",
                                           "relative_rate_calibrated"], lineterminator="\n")
        wr.writeheader()
        for g, v in proxy.items():
            wr.writerow({"group": g, **{k: f"{x:.6f}" for k, x in v.items()}})
    print(pd.DataFrame(rows)[["group", "entry_rule", "scenario", "oasdi_per_tax_dollar", "oasdi_per_tax_dollar_net",
                              "part_a_per_hi_tax_dollar", "p_qualify_65plus"]].to_string(index=False))


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--case", default="sept29", choices=["sept29", "oct07"],
                    help="sept29 (default: the 2025 reports, which the sept29 and oct05 cases read) or oct07 (the 2026 path)")
    main(ap.parse_args().case)
