"""The legal-status calibration arm, step 2: the pension accrual's status-dependent inputs on each arm.

The case's pension switch (candidate v4 item "pension", pension4 "payable_net") reads four numbers from
pension_accrual_2026_09_28/derived/summary.json at 9ea1beb:
  ratio_net        the OASDI accrual per dollar of the group's on-books OASDI tax, net of the tax on benefits; the
                   case multiplies it by the set model's OASDI receipts, which the status stack already moves;
  part_a_accrual   the Part A accrual of the group's covered worker-years ($bn, fixed by the set's part_a_rule);
  se_oasdi_share   the OASDI part of the group's self-employment tax, which the case adds to those receipts;
  the tax on 2024 benefits, which no status input touches.
Status enters the first three: an unauthorized Mexico-born worker-year is on the books at the case's central share
(0.526) and credited with 10% of its accrual (Note 151's long-run eligible share), and the unauthorized 65+ leave the
denominator of the probability of qualifying for Part A. This script recomputes them on the pension lane's own frame
(frame(), imported read-only; published CPS weights, as that lane) with each arm's flag: the movers of calibrate.py
(derived/movers.csv) at their theta, everyone else at the adopted flag. A fractional theta splits a person's
worker-year: 1 - theta on the books and credited in full, theta at the on-books share and the 10% credit.

The OASDI ratio is the lane's central_accrual at its central settings (the lane's model grid restricted to the two
runs the central reads, (new_issue, general) and the normalizing base (tf, general)); Part A repeats hi_accrual's
central run (new_issue rates, payable, general mortality, no spouse credit).

Gates (each stops with [BLOCKED] before anything is written): every mover is in the lane's frame, in the group,
Mexico-born, with the adopted flag the CPS lane gives it; with the adopted flag the four numbers equal summary.json at
9ea1beb (ratios 1e-12, Part A 1e-9 $bn).
Writes derived/pension.json. Run from the repository root after calibrate.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/status_calibration_2026_09_30/pension.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import hashlib  # noqa: E402
import json  # noqa: E402
import subprocess  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
OUT = HERE / "derived"
PENSION = FISCAL / "pension_accrual_2026_09_28"
sys.path.insert(0, str(PENSION))

import pension_accrual as pa  # noqa: E402

PENSION_COMMIT = "9ea1beb"  # candidate v4's PENSION_COMMIT: the summary the case reads
SUMMARY = "infra/immigration-fiscal/pension_accrual_2026_09_28/derived/summary.json"
GENS = ["G1", "G2", "G3plus"]


def blocked(msg: str):
    raise SystemExit(f"[BLOCKED] {msg}")


def pinned() -> dict:
    buf = subprocess.run(["git", "-C", str(ROOT), "show", f"{PENSION_COMMIT}:{SUMMARY}"], check=True,
                         capture_output=True).stdout
    return json.loads(buf)


def main() -> None:
    J = pinned()
    key = hashlib.sha256(b"".join(Path(f).read_bytes() for f in (pa.ss.__file__, pa.ss.ext.__file__, pa.ca.__file__)))
    if not (pa.CACHE / f"stage_{key.hexdigest()[:16]}.parquet").exists():
        blocked("the pension lane's stage cache is missing; its frame() would write into that lane")
    p = pa.frame()
    s_mex = p.attrs["s_mex"]
    u_long = pa.S.quotes()["note151_eligible_share"]["value"]["end_of_projection"]
    rel = J["benefit_tax"]["relative_rate"]
    cen = pa.CENTRAL
    if (cen["scenario"], cen["rate"], cen["mortality"], cen["unauthorized"], cen["spouse"]) != \
            ("payable", "new_issue", "general", "note151_long_run", False) or J["central"]["scenario"] != "payable":
        blocked("the pension lane's central is not the one the case reads")

    # Each arm's theta on the lane's frame.
    movers = pd.read_csv(OUT / "movers.csv")
    arms = list(dict.fromkeys(pd.read_csv(OUT / "arms.csv").arm))
    idx = pd.Series(np.arange(len(p)), index=pd.MultiIndex.from_arrays([p.PH_SEQ.to_numpy(), p.A_LINENO.to_numpy()]))
    if idx.index.duplicated().any():
        blocked("PH_SEQ + A_LINENO is not unique in the pension frame")
    adopted = p.unauth.to_numpy().astype(float)
    thetas = {}
    for arm in arms:
        th = adopted.copy()
        mv = movers[movers.arm == arm]
        rows = idx.reindex(pd.MultiIndex.from_arrays([mv.PH_SEQ.to_numpy(), mv.A_LINENO.to_numpy()])).to_numpy()
        if np.isnan(rows).any():
            blocked(f"{arm}: {int(np.isnan(rows).sum())} movers are not in the pension lane's frame")
        rows = rows.astype(int)
        if not (p.union.to_numpy()[rows].all() and p.mexico_born.to_numpy()[rows].all()):
            blocked(f"{arm}: a mover outside the pension lane's group or not Mexico-born")
        if not np.array_equal(adopted[rows], mv.adopted.to_numpy()):
            blocked(f"{arm}: a mover's adopted flag differs between the CPS lane and the pension lane")
        th[rows] = mv.theta.to_numpy()
        thetas[arm] = th

    # OASDI: per-person accrual at the central settings for a legal worker-year, and its tax-on-benefits timing.
    econ = pa.L.Economy()
    prelim = pa.S.scaled_factors().preliminary.to_numpy()
    g = (cen["rate"], cen["mortality"])
    pa.GRID = [pa.BASE, g]  # the two runs model_factor reads at the central; each cell is computed on its own
    grids = {"payable": pa.model_grid(econ, prelim, pa.payable_path(econ))}
    share = pa.tob_share_path() * (1 + pa.hi_over_oasdi_tob()) * pa.obbba_factor()
    if pa.BT_CENTRAL["bt_path"] != "obbba":
        blocked("the central tax-on-benefits path is not the 2025 tax law's")
    tau = pa.tob_timing(econ, prelim, share, runs=[(g, "payable")])
    sel = (p.union & (p.tax_oasdi > 0)).to_numpy()
    q = p[sel].reset_index(drop=True)
    fam = pa.ss.family_vector(q, "observed_family")
    base = (q.oasdi_wage + q.oasdi_se).to_numpy()
    acc_legal, tob = pa.central_accrual(q.assign(unauth=False, tax_oasdi=base), grids, u_long, tau, fam)
    wq = q.w.to_numpy()

    # Part A: hi_accrual's central run, the flag entering the on-books share, the credit and P(qualify).
    u = p[p.union].reset_index(drop=True)
    wu = u.w.to_numpy()
    covered = (u.tax_hi > 0).to_numpy()
    age, gen = u.age.to_numpy(), u.gen.to_numpy()
    cov = {}
    for gg in GENS:
        m = gen == gg
        wt = pd.Series(wu[m]).groupby(age[m]).sum()
        num = pd.Series(covered[m] * wu[m]).groupby(age[m]).sum()
        cov[gg] = (num / wt).reindex(range(0, 91)).fillna(0.0).to_numpy()
    start = np.where(u.mexico_born & u.arrival_age.notna(), np.maximum(u.arrival_age.fillna(21), 21), 21).astype(int)
    n_years = np.array([cov[gg][st:65].sum() for gg, st in zip(gen, start)])
    value = pa.part_a_pv(age, u.sex.to_numpy(), econ, cen["rate"], cen["scenario"], cen["mortality"])
    mcare = (u.MCARE == 1).to_numpy()
    elig = covered & (age < 65) & (n_years > 0)

    out, gate = {}, {}
    for arm, th in thetas.items():
        tq, tu = th[sel], th[p.union.to_numpy()]
        on_q = 1.0 - tq + tq * s_mex
        acc = acc_legal * (1.0 - tq + tq * s_mex * u_long)
        tax = base * on_q
        ratio = float((wq * acc).sum() / (wq * tax).sum())
        fs = rel * float((wq * acc * tob).sum() / (wq * acc).sum())
        pq = np.zeros(len(u))
        for gg in GENS:
            m = (gen == gg) & (age >= 65)
            wl = wu[m] * (1.0 - tu[m])
            pq[gen == gg] = float((wl * mcare[m]).sum() / wl.sum())
        base_a = np.where(elig, pq * value / np.maximum(n_years, 1e-9), 0.0)
        part_a = float((wu * base_a * (1.0 - tu + tu * s_mex * u_long)).sum() / 1e9)
        on_u = 1.0 - tu + tu * s_mex
        se_o = float((wu * u.oasdi_se.to_numpy() * on_u).sum())
        se_h = float((wu * u.hi_se.to_numpy() * on_u).sum())
        unauth_tax = float((wq * base * tq * s_mex).sum() / (wq * tax).sum())
        out[arm] = dict(accrual_per_tax_dollar=ratio, future_share=fs, ratio_net=ratio * (1 - fs), part_a_accrual_bn=part_a,
                        se_oasdi_share=se_o / (se_o + se_h), oasdi_tax_bn=float((wq * tax).sum() / 1e9),
                        unauthorized_share_of_oasdi_tax=unauth_tax, p_qualify_g1=float(pq[gen == "G1"][0]))
    a, cd = out["adopted"], J["central_decomposition"]["low"]
    checks = {"accrual_per_tax_dollar": (a["accrual_per_tax_dollar"], cd["accrual_per_tax_dollar"], 1e-12),
              "future_share": (a["future_share"], J["benefit_tax"]["future_share_group"], 1e-12),
              "ratio_net": (a["ratio_net"], J["ratio_net"], 1e-12),
              "part_a_accrual_bn": (a["part_a_accrual_bn"], cd["part_a_accrual_bn"], 1e-9),
              "se_oasdi_share": (a["se_oasdi_share"], J["case_components_attrs"]["se_oasdi_share"], 1e-12)}
    for k, (got, want, tol) in checks.items():
        gate[k] = dict(recomputed=got, summary_9ea1beb=want, difference=got - want)
        print(f"[gate] adopted flag, {k}: {got!r} against {want!r} at {PENSION_COMMIT} (difference {got - want:.1e})", flush=True)
        if abs(got - want) > tol:
            blocked(f"the adopted flag does not reproduce the pension lane's {k}")
    for arm, r in out.items():
        r.update({f"change_{k}": r[k] - a[k] for k in ["ratio_net", "part_a_accrual_bn", "se_oasdi_share"]})
    meta = dict(source=f"{SUMMARY} at {PENSION_COMMIT}", s_mex=s_mex, credit_unauthorized=u_long, relative_rate=rel,
                weights="the pension lane's frame (published CPS weights)", gate=gate)
    (OUT / "pension.json").write_text(json.dumps({"meta": meta, "arms": out}, indent=1, sort_keys=True) + "\n")
    print(pd.DataFrame(out).T.to_string(), flush=True)


if __name__ == "__main__":
    main()
