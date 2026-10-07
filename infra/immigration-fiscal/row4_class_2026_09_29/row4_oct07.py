"""The row-4 class on main case v6 (oct07): the pension switch's inputs on audit row 4's weights, by generation.

v6's Social Security and Medicare lines carry item pension_tr2026, the Trustees-2026 lane's arm
all_2026_inputs_separate_funds (pension_tr2026_2026_10_06/pension_tr2026.py main(), run_arm on Lane()). Lane.p is
pension_accrual.frame() at the published ASEC weights (union 40,896,574), and run_arm sums each person's accrual over
lane.q.w (the OASDI ratio) and lane.p.w (Part A, hi_accrual). Part 1 reruns that arm and the lane's control (the
pension lane's central, v4's pension block) through the lane's own functions, imported read-only, once at the
published weights and once with w scaled by row 4's two cell factors (Mexico-born naturalized / noncitizen outside CA
and TX, derived/row4_parta.json), as row4_parta.py and row4_oasdi_ratio.py do on v4.

Part 2 is row4_benefit_tax.py's computation (benefit_tax.py's census_income run, its functions imported read-only),
reported by generation at both weight sets: each generation's relative benefit-tax rate (its rate over the nation's,
benefit_tax.py:182-189) and benefit tax by allocation (what generation_account_2026_09_24/v4_split.cjs reads), the
national rate and key, and the union's 2024 benefits. benefit_tax is imported only after part 1 has run: its import
appends fields to the PERSON list of extend_ledger, a module both parts share.

Gates (exit 1, nothing written): the pension stage cache exists (no rebuild); the union counts
(population_basis_2026_09_29/derived/frame_counts.csv; published 1e-3, row 4 one person); the published control
reproduces the pension lane's summary.json (ratio_net, Part A, per tax dollar by generation; 1e-12 relative) and the
Trustees lane's control; the published arm reproduces the Trustees lane's summary.json beside entry (1e-12 relative);
the row-4 control reproduces this lane's v4 row-4 Part A, G1's, and the gross OASDI ratio, timing and tax (1e-9); G2
and G3+ are the same at both weights (exact); the published benefit-tax values reproduce benefit_tax.json (each
generation's relative rate and benefits, benefit tax by allocation, the national key; 1e-9) and summary.json's
current_receipt_bn (1e-9); the row-4 receipts and union relative rate reproduce derived/row4_benefit_tax.json (1e-12).
Writes derived/row4_oct07_inputs.json, which row4_oct07.cjs prices. Run from the repository root after the v4 scripts
(it reads their row4_parta.json, row4_oasdi_ratio.json and row4_benefit_tax.json):
  OPENBLAS_NUM_THREADS=1 UV_OFFLINE=1 uv run --no-project --with "taxcalc==6.8.2" python3 \
      infra/immigration-fiscal/row4_class_2026_09_29/row4_oct07.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import copy  # noqa: E402
import csv  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import resource  # noqa: E402
import zipfile  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
TR = FISCAL / "pension_tr2026_2026_10_06"
ARM = "all_2026_inputs_separate_funds"
FAILS = []


def gate(label, ok, detail=""):
    print(f"GATE {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def blocked():
    if FAILS:
        print(f"[BLOCKED] {len(FAILS)} gate(s) failed; nothing written", flush=True)
        sys.exit(1)


def rel_near(a, b, tol):
    return abs(a - b) <= tol * max(1.0, abs(b))


R4A = json.loads((OUT / "row4_parta.json").read_text())
R4O = json.loads((OUT / "row4_oasdi_ratio.json").read_text())
R4B = json.loads((OUT / "row4_benefit_tax.json").read_text())
FAC = R4A["factors"]
COUNTS = {r["count"]: r for r in csv.DictReader(open(FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv"))}
N_PUB, N_ROW4 = float(COUNTS["union|all"]["published"]), float(COUNTS["union|all"]["row4"])


def pension() -> dict:
    """Part 1: the Trustees arm and the lane's control, at the published weights and at row 4's."""
    sys.path.insert(0, str(TR))
    import pension_tr2026 as PT  # the Trustees lane, read-only (puts the pension lane on sys.path)

    PA, L, groups = PT.PA, PT.L, PT.GROUPS
    key = hashlib.sha256(b"".join(Path(f).read_bytes() for f in (PA.ss.__file__, PA.ss.ext.__file__, PA.ca.__file__))).hexdigest()[:16]
    gate("pension stage cache present (no rebuild)", (PA.CACHE / f"stage_{key}.parquet").exists(), key)
    blocked()
    sum_pa = json.loads((PA.OUT / "summary.json").read_text())
    sum_tr = json.loads((TR / "derived/summary.json").read_text())
    PT.T.quotes()
    lane = PT.Lane()
    with zipfile.ZipFile(FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip") as z:
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"]).rename(columns={"H_SEQ": "PH_SEQ"})

    def row4_factor(frame):
        st = frame[["PH_SEQ"]].merge(hh, on="PH_SEQ", how="left", validate="many_to_one").GESTFIPS.to_numpy()
        if np.isnan(st.astype(float)).any():
            gate("every person has a state", False)
        mb = (frame.PENATVTY.to_numpy() == 303) & ~np.isin(st, [6, 48])
        f = np.ones(len(frame))
        f[mb & (frame.PRCITSHP.to_numpy() == 4)] = FAC["natz"]
        f[mb & (frame.PRCITSHP.to_numpy() == 5)] = FAC["noncit"]
        return f

    fp, fq = row4_factor(lane.p), row4_factor(lane.q)
    w, u = lane.p.w.to_numpy(), lane.p.union.to_numpy()
    gate("union at published weights on the pension frame", abs(w[u].sum() - N_PUB) < 1e-3, f"{w[u].sum():.6f}")
    gate("row-4 union on the pension frame", abs((w * fp)[u].sum() - N_ROW4) < 1.0, f"{(w * fp)[u].sum():.6f}")
    lane4 = copy.copy(lane)
    lane4.p = lane.p.assign(w=w * fp)
    lane4.q = lane.q.assign(w=lane.q.w.to_numpy() * fq)
    gate("q's factor is p's on the same persons", np.array_equal(
        lane4.q.w.to_numpy(), lane4.p[lane.p.union & (lane.p.tax_oasdi > 0)].reset_index(drop=True).w.to_numpy()))

    econ, prelim = lane.econ, lane.prelim
    paths, _ = PT.build_paths(econ)
    grid_lane = PT.grid(econ, prelim, paths["oasdi_lane_2025"], [PT.G, PT.BASE])
    grid_t25 = PT.grid(econ, prelim, paths["oasdi_2025"], [PT.G, PT.BASE])

    def brief(a):
        return dict(groups={g: dict(a["groups"][g]) for g in groups}, future_share_group=a["future_share_group"],
                    ratio_net=a["ratio_net"], part_a_bn=a["part_a_bn"])

    # The control as main() runs it (hi_full only adds Part A rates beside the central row); the arm as main() builds
    # all_2026_inputs_separate_funds: the 2026 economy, mortality and HI costs patched in, the survival cache cleared.
    res = {"control": {}, "arm": {}}
    for name, ln in (("published", lane), ("row4", lane4)):
        res["control"][name] = brief(PT.run_arm(ln, grid_lane, paths["oasdi_lane_2025"], None))
    mort = PT.T.quotes()["tr2026_mortality_decline"]["value"]
    ea = PT.economy_2026(rates=True, wages=True, parameters=True)
    L.survival.cache_clear()
    with PT.patched(L, "_decline", lambda: (mort["65plus"], mort["total"])), PT.patched(PA, "hi_cost_path", PT.hi_cost_path_tr2026):
        g_arm = PT.hybrid(PT.grid(ea, prelim, paths["separate_2026"], [PT.G]), grid_t25)
        for name, ln in (("published", lane), ("row4", lane4)):
            res["arm"][name] = brief(PT.run_arm(ln, g_arm, paths["separate_2026"], paths["hi_2026"], econ=ea,
                                                share=PT.tob_share_tr2026()))
        L.survival.cache_clear()
    L.survival.cache_clear()

    c0, a0, c4, a4 = res["control"]["published"], res["arm"]["published"], res["control"]["row4"], res["arm"]["row4"]
    gate("published control: ratio_net is the pension lane's", rel_near(c0["ratio_net"], sum_pa["ratio_net"], 1e-12), f"{c0['ratio_net']:.15f}")
    gate("published control: Part A is the pension lane's",
         rel_near(c0["part_a_bn"], sum_pa["central_decomposition"]["low"]["part_a_accrual_bn"], 1e-12), f"{c0['part_a_bn']:.12f}")
    per = sum_pa["oasdi_per_tax_dollar_central_by_generation"]
    gate("published control: per tax dollar by generation is the pension lane's",
         all(rel_near(c0["groups"][g]["per_tax_dollar"], per[g], 1e-12) for g in groups))
    b = sum_tr["beside"][ARM]
    for k, v in (("ratio_net", a0["ratio_net"]), ("part_a_bn", a0["part_a_bn"]),
                 ("per_tax_dollar", a0["groups"]["union"]["per_tax_dollar"]), ("future_share_group", a0["future_share_group"]),
                 ("g3plus_net_own_rate", a0["groups"]["G3plus"]["net_own_rate"]),
                 ("g3plus_part_a_per_hi_tax_dollar", a0["groups"]["G3plus"]["part_a_per_hi_tax_dollar"])):
        gate(f"published arm: {k} is the Trustees lane's {ARM}", rel_near(v, b[k], 1e-12), f"{v:.15f} vs {b[k]:.15f}")
    gate("published control: the Trustees lane's control", rel_near(c0["ratio_net"], sum_tr["arms"]["control"]["ratio_net"], 1e-12)
         and rel_near(c0["part_a_bn"], sum_tr["arms"]["control"]["part_a_bn"], 1e-12))
    gate("row-4 control: union Part A is row4_parta.json's", abs(c4["part_a_bn"] - R4A["central"]["union"]["row4_bn"]) < 1e-9,
         f"{c4['part_a_bn']:.12f} vs {R4A['central']['union']['row4_bn']:.12f}")
    gate("row-4 control: G1 Part A is row4_parta.json's", abs(c4["groups"]["G1"]["part_a_bn"] - R4A["central"]["G1"]["row4_bn"]) < 1e-9)
    gate("row-4 control: gross ratio, timing and OASDI tax are row4_oasdi_ratio.json's",
         abs(c4["groups"]["union"]["per_tax_dollar"] - R4O["row4"]["ratio_gross"]) < 1e-9
         and abs(c4["groups"]["union"]["timing"] - R4O["row4"]["timing"]) < 1e-9
         and abs(c4["groups"]["union"]["tax_bn"] - R4O["row4"]["oasdi_tax_bn"]) < 1e-9,
         f"{c4['groups']['union']['per_tax_dollar']:.12f} / {c4['groups']['union']['timing']:.12f} / {c4['groups']['union']['tax_bn']:.9f}")
    for arm, x0, x4 in (("control", c0, c4), ("arm", a0, a4)):
        same = all(x0["groups"][g][k] == x4["groups"][g][k] for g in ("G2", "G3plus")
                   for k in ("per_tax_dollar", "timing", "part_a_bn", "hi_tax_bn", "tax_bn"))
        gate(f"{arm}: G2 and G3+ are the same at both weights (exact)", same)
    for name, x in res.items():
        for wt in ("published", "row4"):
            g = x[wt]["groups"]
            print(f"{name:8s} {wt:9s} ratio_net (published rate) {x[wt]['ratio_net']:.9f}; per $ {g['union']['per_tax_dollar']:.9f}; "
                  f"timing {g['union']['timing']:.9f}; Part A {x[wt]['part_a_bn']:.6f} (G1 {g['G1']['part_a_bn']:.6f})", flush=True)
    return dict(arm=ARM, lane_rel={g: float(v) for g, v in lane.rel.items()}, factors=FAC, results=res,
                union_counts=dict(published=float(w[u].sum()), row4=float((w * fp)[u].sum())))


def benefit_tax() -> dict:
    """Part 2: the benefit-tax inputs by generation and allocation, at the published weights and at row 4's."""
    sys.path.insert(0, str(FISCAL / "pension_accrual_2026_09_28"))
    import benefit_tax as B  # the pension lane's benefit-tax run, read-only

    btj = json.loads((FISCAL / "pension_accrual_2026_09_28/derived/benefit_tax.json").read_text())
    res = btj["results"]["census_income"]
    sum_bt = json.loads((FISCAL / "pension_accrual_2026_09_28/derived/summary.json").read_text())["benefit_tax"]
    national_fit = sum_bt["national_income_tax_bn"]  # the case's federal income tax line, national (model.json)
    T, U, ext, TC = B.T, B.U, B.ext, B.TC
    for f_ in ("PENATVTY", "PRCITSHP"):
        if f_ not in ext.base.PERSON:
            ext.base.PERSON.append(f_)
    state = ext.build(argparse.Namespace(cps_zip=T.CPS_ZIP))
    d, W = state["d"], state["person_weights"]
    n = len(d)
    civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    masks = {g: state["group"][c] & civ for g, c in B.TARGETS.items()}
    masks["union"] = masks["G1"] | masks["G2"] | masks["G3plus"]
    union = masks["union"]
    p, _ = T.person_table(d)
    n_ret = int(p.ret_unit.max()) + 1
    ret = p.ret_unit.to_numpy()
    carry = B.carriers(d, p)
    idx, n_units = state["index"], state["n_units"]

    def personal(unit_value):
        out = np.zeros(n)
        out[carry.to_numpy()] = unit_value[carry.index.to_numpy()]
        return out

    def shared(person_value):
        return ext.allocate(np.bincount(idx, weights=person_value, minlength=n_units), idx, np.ones(n, bool), n_units)

    census_key = {"personal": d.FEDTAX_BC.to_numpy(float)}
    census_key["shared"] = shared(census_key["personal"])
    runs = {}
    for with_benefits in (True, False):
        frame = U.build_frame(p, B.incomes(d, "census_income", with_benefits), n_ret, eic_child=p.eic_child.to_numpy())
        runs[with_benefits] = TC.run(frame)
    before = {k: r["c09200"] - r["niit"] for k, r in runs.items()}
    key = {"personal": personal(before[True] - before[False])}
    key["shared"] = shared(key["personal"])
    after = {k: r["iitax"] - r["niit"] for k, r in runs.items()}
    d_after = after[True] - after[False]
    filer = (p.ret_role <= 1).to_numpy()
    ss = d.SS_VAL.to_numpy(float)
    ss_filed = np.where(filer, ss, 0.0)
    unit_ss = np.bincount(ret, weights=ss_filed, minlength=n_ret)
    by_benefit = np.divide(ss_filed, unit_ss[ret], out=np.zeros(n), where=unit_ss[ret] > 0)
    bt = d_after[ret] * by_benefit

    w0 = W[:, 0]
    mb = d.PENATVTY.eq(303).to_numpy() & ~d.GESTFIPS.isin([6, 48]).to_numpy()
    f = np.ones(n)
    f[mb & d.PRCITSHP.eq(4).to_numpy()] = FAC["natz"]
    f[mb & d.PRCITSHP.eq(5).to_numpy()] = FAC["noncit"]
    w4 = w0 * f
    gate("published union count", abs(w0[union].sum() - N_PUB) < 1e-3, f"{w0[union].sum():.6f}")
    gate("row-4 union count", abs(w4[union].sum() - N_ROW4) < 1.0, f"{w4[union].sum():.6f}")
    out = {}
    for name, wt in (("published", w0), ("row4", w4)):
        nat_rate = float(bt[civ] @ wt[civ]) / float(ss[civ] @ wt[civ])
        o = {"national_rate": nat_rate, "groups": {}, "alloc": {}}
        for g, m in masks.items():
            b_, s_ = float(bt[m] @ wt[m]), float(ss[m] @ wt[m])
            o["groups"][g] = dict(benefits_bn=s_ / 1e9, benefit_tax_bn=b_ / 1e9, rate=b_ / s_, relative_rate=b_ / s_ / nat_rate)
        for alloc, end in (("shared", "low"), ("personal", "high")):
            g_ = float(key[alloc][union] @ wt[union]) / 1e9
            n_ = float(census_key[alloc][civ] @ wt[civ]) / 1e9
            o["alloc"][alloc] = dict(end=end, group_benefit_tax_bn=g_, national_key_census_bn=n_, receipt_bn=national_fit * g_ / n_,
                                     by_generation_benefit_tax_bn={g: float(key[alloc][masks[g]] @ wt[masks[g]]) / 1e9 for g in B.TARGETS})
        out[name] = o
    p0, p4 = out["published"], out["row4"]
    for g in ("union", "G1", "G2", "G3plus"):
        gate(f"published relative rate {g} reproduces benefit_tax.json",
             abs(p0["groups"][g]["relative_rate"] - res["groups"][g]["relative_rate"][0]) < 1e-9, f"{p0['groups'][g]['relative_rate']:.12f}")
        gate(f"published benefits {g} reproduce benefit_tax.json", abs(p0["groups"][g]["benefits_bn"] - res["groups"][g]["benefits_bn"][0]) < 1e-9)
    for alloc, end in (("shared", "low"), ("personal", "high")):
        k = res["key"][alloc]
        gate(f"{alloc}: published benefit tax by generation reproduces benefit_tax.json",
             all(abs(p0["alloc"][alloc]["by_generation_benefit_tax_bn"][g] - k["by_generation_benefit_tax_bn"][g]) < 1e-9 for g in B.TARGETS))
        gate(f"{alloc}: published national key reproduces benefit_tax.json",
             abs(p0["alloc"][alloc]["national_key_census_bn"] - k["national_key_census_bn"]) < 1e-9)
        gate(f"{alloc}: published receipt reproduces summary.json current_receipt_bn[{end}]",
             abs(p0["alloc"][alloc]["receipt_bn"] - sum_bt["current_receipt_bn"][end]) < 1e-9)
        gate(f"{alloc}: row-4 receipt reproduces row4_benefit_tax.json", abs(p4["alloc"][alloc]["receipt_bn"] - R4B[alloc]["receipt_row4_bn"]) < 1e-12,
             f"{p4['alloc'][alloc]['receipt_bn']:.12f}")
    gate("row-4 union relative rate reproduces row4_benefit_tax.json", abs(p4["groups"]["union"]["relative_rate"] - R4B["relative_rate_row4"]) < 1e-12)
    gate("G2 and G3+ benefit tax and benefits are the same at both weights (exact)", all(
        p0["groups"][g][k] == p4["groups"][g][k] for g in ("G2", "G3plus") for k in ("benefits_bn", "benefit_tax_bn")))
    for g in ("union", "G1", "G2", "G3plus"):
        print(f"{g:7s} relative rate {p0['groups'][g]['relative_rate']:.9f} -> {p4['groups'][g]['relative_rate']:.9f}; benefits "
              f"{p0['groups'][g]['benefits_bn']:.6f} -> {p4['groups'][g]['benefits_bn']:.6f}", flush=True)
    print(f"national rate {p0['national_rate']:.12f} -> {p4['national_rate']:.12f}", flush=True)
    return dict(weights=out)


out = dict(pension=pension(), benefit_tax=benefit_tax(), gates_failed=FAILS)
blocked()
(OUT / "row4_oct07_inputs.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
print(f"[written] {(OUT / 'row4_oct07_inputs.json').relative_to(FISCAL.parent.parent)}; "
      f"peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB", flush=True)
