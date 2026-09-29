"""Social Security and Medicare Part A accrual per tax dollar for the Indian-origin group and the India-born (the
sept29 re-key's pension rule at each group's own ratios).

The Black lane's accrual_black.py is imported read-only and its functions run unchanged: the pension lane
(pension_accrual_2026_09_28) at its central settings, every foreign-born member's career starting at arrival (PEINUSYR
midpoints), everyone else's at 21; the arm with every member at 21 beside. Groups on the pension frame, matched to the
CPS on PH_SEQ and A_LINENO:
  indian_origin  India-born (PENATVTY 210, PRCITSHP 4-5) or native with an India-born parent (PEFNTVTY/PEMNTVTY 210)
  india_born     the first part alone
The pension lane models unauthorized status for the Mexico-born only, so every Indian-origin member is on the books
[INFERENCE: an upper bound on the group's accrual; Pew and MPI put unauthorized India-born at a few hundred thousand].

The relative benefit-tax rate is not measured for the group: the Black lane's statutory proxy (section 86 on tax-unit
income other than benefits, the unit's 2024 bracket rate) is computed here for the nation, the union and both groups,
and each group's rate is its proxy relative rate scaled by the union's measured / proxy ratio, as the Black lane does
[INFERENCE].

Gates ([BLOCKED]): the union's OASDI payable and scheduled ratios, Part A accrual and benefit-tax timing reproduce the
pension lane (accrual_black.STORED); the union's proxy relative rate reproduces the Black lane's benefit_tax_proxy.csv.
Outputs: derived/accrual_ratios.csv, derived/benefit_tax_proxy.csv. Run from the repository root (about 3 min):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/indian_full_account_2026_09_29/accrual_indian.py
"""
from __future__ import annotations

import csv
import importlib.util
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True   # read-only imports from other lanes: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
DER = LANE / "derived"
_spec = importlib.util.spec_from_file_location("accrual_black", FISCAL / "black_comparator_rough_2026_09_28/accrual_black.py")
A = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A)
P, ZIP, US, G = A.P, A.ZIP, A.US, A.G
INDIA = 210


def cps_masks(d):
    native = d.PRCITSHP.isin([1, 2, 3])
    pus = d.PEFNTVTY.isin(US) & d.PEMNTVTY.isin(US)
    g1 = (d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(INDIA))
    g2 = native & (d.PEFNTVTY.eq(INDIA) | d.PEMNTVTY.eq(INDIA))
    union = ((d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)) | (native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)))
             | (native & pus & d.PRDTHSP.eq(1)))
    return {"indian_origin": (g1 | g2).to_numpy(), "india_born": g1.to_numpy(), "union": union.to_numpy()}


def benefit_tax_proxy():
    """accrual_black.benefit_tax_proxy's statutory proxy on this lane's groups (the same code path, other masks)."""
    cols = ["PH_SEQ", "TAX_ID", "MARSUPWT", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY",
            "PRDTHSP", "SS_VAL", "PTOTVAL", "TAX_INC", "FILESTAT"]
    with zipfile.ZipFile(ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=cols)
    w = (d.MARSUPWT / 100 * (d.PRPERTYP.eq(2) | d.A_AGE.lt(15))).to_numpy(float)
    groups = {"nation": np.ones(len(d), bool), **cps_masks(d)}
    u = d.groupby(["PH_SEQ", "TAX_ID"])
    ss = d.SS_VAL.clip(lower=0).to_numpy(float)
    ss_u = u.SS_VAL.transform(lambda s: s.clip(lower=0).sum()).to_numpy(float)
    other = np.maximum(u.PTOTVAL.transform("sum").to_numpy(float) - ss_u, 0.0)
    joint = u.FILESTAT.transform("min").isin([1, 2, 3]).to_numpy()
    t1 = np.where(joint, A.THRESHOLDS["joint"][0], A.THRESHOLDS["single"][0])
    t2 = np.where(joint, A.THRESHOLDS["joint"][1], A.THRESHOLDS["single"][1])
    pi = other + 0.5 * ss_u
    taxable = np.where(pi <= t1, 0.0, np.where(pi <= t2, np.minimum(0.5 * ss_u, 0.5 * (pi - t1)),
                       np.minimum(0.85 * ss_u, 0.85 * (pi - t2) + np.minimum(0.5 * ss_u, 0.5 * (t2 - t1)))))
    ti = np.maximum(u.TAX_INC.transform("sum").to_numpy(float), 0.0)
    rate = np.where(ti > 0, A.bracket_rate(ti, joint), np.where(taxable > 0, 0.10, 0.0))
    own = np.divide(ss, ss_u, out=np.zeros(len(d)), where=ss_u > 0)
    btax = taxable * rate * own
    out = {g: dict(benefits_bn=float((w * ss)[m].sum() / 1e9), benefit_tax_bn=float((w * btax)[m].sum() / 1e9),
                   sample_with_benefits=float(((ss > 0) & m & (w > 0)).sum()))
           for g, m in groups.items()}
    for g in out:
        out[g]["rate"] = out[g]["benefit_tax_bn"] / out[g]["benefits_bn"]
    for g in out:
        out[g]["relative_rate_proxy"] = out[g]["rate"] / out["nation"]["rate"]
    scale = A.STORED["rel_union"] / out["union"]["relative_rate_proxy"]
    for g in out:
        out[g]["relative_rate_calibrated"] = out[g]["relative_rate_proxy"] * scale
    ref = pd.read_csv(FISCAL / "black_comparator_rough_2026_09_28/derived/benefit_tax_proxy.csv").set_index("group")
    if abs(out["union"]["relative_rate_proxy"] - float(ref.loc["union", "relative_rate_proxy"])) > 1e-6:
        raise SystemExit(f"[BLOCKED] the union's proxy {out['union']['relative_rate_proxy']:.6f} does not reproduce the "
                         f"Black lane's {ref.loc['union', 'relative_rate_proxy']}")
    print("[gate] the union's benefit-tax proxy reproduces the Black lane's benefit_tax_proxy.csv")
    return out


def main():
    proxy = benefit_tax_proxy()
    for g, v in proxy.items():
        print(f"benefit-tax proxy {g:15s} rate {v['rate']:.5f} relative {v['relative_rate_proxy']:.4f} calibrated "
              f"{v['relative_rate_calibrated']:.4f} (persons with benefits in sample {v['sample_with_benefits']:.0f})")
    rel = {"union": A.STORED["rel_union"], "indian_origin": proxy["indian_origin"]["relative_rate_calibrated"],
           "india_born": proxy["india_born"]["relative_rate_calibrated"]}

    q = P.S.quotes()
    u_long = q["note151_eligible_share"]["value"]["end_of_projection"]
    p = P.frame()
    with zipfile.ZipFile(ZIP) as z:
        cps = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "A_LINENO", "PRCITSHP", "PENATVTY", "PEFNTVTY",
                                                          "PEMNTVTY", "PRDTHSP"])
    m = p[["PH_SEQ", "A_LINENO"]].merge(cps, on=["PH_SEQ", "A_LINENO"], how="left", validate="one_to_one",
                                        suffixes=("_p", ""))
    if m.PENATVTY.isna().any():
        raise SystemExit("[BLOCKED] pension-frame persons without a CPS birthplace record")
    masks = cps_masks(m)
    mid = P.entry_midpoints()
    arrival_any = p.age - (2024.5 - p.PEINUSYR.map(mid))
    foreign = p.PRCITSHP.isin([4, 5]).to_numpy()
    econ = P.L.Economy()
    prelim = P.S.scaled_factors().preliminary.to_numpy()
    P.GRID = [G, P.BASE]
    grids = {s: P.model_grid(econ, prelim, P.payable_path(econ) if s == "payable" else None) for s in P.SCENARIOS}
    share = P.tob_share_path() * (1 + P.hi_over_oasdi_tob()) * P.obbba_factor()
    taus = P.tob_timing(econ, prelim, share, runs=[(G, s) for s in P.SCENARIOS])

    def frame_for(mask, entry_rule):
        """accrual_black.main's frame_for."""
        f = p.copy()
        f["union"] = mask
        if entry_rule != "lane":
            f["gen"] = np.where(mask, "B", "")
        if entry_rule == "lane":
            arr = f.arrival_age
            imm = f.mexico_born.to_numpy() & arr.notna().to_numpy()
        elif entry_rule == "immigrants_at_arrival":
            arr = arrival_any
            imm = foreign & arr.notna().to_numpy()
        else:
            arr = arrival_any
            imm = np.zeros(len(f), bool)
        f["entry"] = np.where(imm, arr.fillna(21), 21.0)
        f["start"] = np.where(imm, np.maximum(arr.fillna(21), 21), 21).astype(int)
        return f

    runs = {("union", "lane"): frame_for(p.union.to_numpy(), "lane")}
    for g in ("indian_origin", "india_born"):
        runs[(g, "immigrants_at_arrival")] = frame_for(masks[g], "immigrants_at_arrival")
        runs[(g, "all_at_21")] = frame_for(masks[g], "all_at_21")
    res = {}
    for (name, rule), fr in runs.items():
        qq = fr[fr.union & (fr.tax_oasdi > 0)].reset_index(drop=True)
        o = A.oasdi_ratio(qq, grids, u_long, taus)
        a = {s: A.part_a(fr[fr.union].copy(), econ, u_long, s) for s in P.SCENARIOS}
        res[(name, rule)] = (o, a, int(len(qq)))
        print(f"{name} ({rule}): persons {fr.w[fr.union].sum() / 1e6:.3f}M, taxpayers in sample {len(qq)}; OASDI accrual "
              f"per tax dollar payable {o['payable']['ratio']:.6f} scheduled {o['scheduled']['ratio']:.6f}; Part A payable "
              f"{a['payable']['accrual_bn']:.3f}bn on HI tax {a['payable']['hi_tax_bn']:.3f}bn")
    o, a, _ = res[("union", "lane")]
    for k, got in (("payable", o["payable"]["ratio"]), ("scheduled", o["scheduled"]["ratio"]),
                   ("part_a", a["payable"]["accrual_bn"]), ("timing", o["payable"]["timing"])):
        if abs(got - A.STORED[k]) > 1e-5 * max(1, abs(A.STORED[k])):
            raise SystemExit(f"[BLOCKED] the union's {k} does not reproduce the pension lane: {got} vs {A.STORED[k]}")
    print("[gate] union ratios, Part A accrual and benefit-tax timing reproduce the pension lane")
    rows = []
    for (name, rule), (o, a, n) in res.items():
        for scen in P.SCENARIOS:
            r = rel[name]
            rows.append({"group": name, "entry_rule": rule, "scenario": scen,
                         "oasdi_per_tax_dollar": f"{o[scen]['ratio']:.6f}",
                         "benefit_tax_timing": f"{o[scen]['timing']:.6f}", "relative_benefit_tax_rate": f"{r:.6f}",
                         "future_share": f"{r * o[scen]['timing']:.6f}",
                         "oasdi_per_tax_dollar_net": f"{o[scen]['ratio'] * (1 - r * o[scen]['timing']):.6f}",
                         "part_a_per_hi_tax_dollar": f"{a[scen]['accrual_bn'] / a[scen]['hi_tax_bn']:.6f}",
                         "cps_oasdi_tax_bn": f"{o[scen]['tax_bn']:.4f}", "cps_hi_tax_bn": f"{a[scen]['hi_tax_bn']:.4f}",
                         "part_a_accrual_bn": f"{a[scen]['accrual_bn']:.4f}",
                         "p_qualify_65plus": f"{a[scen]['p_qualify']:.6f}", "sample_taxpayers": n})
    DER.mkdir(exist_ok=True)
    with open(DER / "accrual_ratios.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)
    with open(DER / "benefit_tax_proxy.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=["group", "benefits_bn", "benefit_tax_bn", "sample_with_benefits", "rate",
                                           "relative_rate_proxy", "relative_rate_calibrated"], lineterminator="\n")
        wr.writeheader()
        for g, v in proxy.items():
            wr.writerow({"group": g, **{k: f"{x:.6f}" for k, x in v.items()}})
    print(pd.DataFrame(rows)[["group", "entry_rule", "scenario", "oasdi_per_tax_dollar", "oasdi_per_tax_dollar_net",
                              "part_a_per_hi_tax_dollar", "p_qualify_65plus"]].to_string(index=False))


if __name__ == "__main__":
    main()
