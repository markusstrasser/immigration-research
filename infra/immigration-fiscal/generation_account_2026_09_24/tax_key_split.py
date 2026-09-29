"""v4 case (sept29): the IRS-matched federal income-tax key (the adopted case's item 3) split by generation.

tax_key_heldout_2026_09_28/heldout.py moves the union's share of the federal income-tax key: it rakes the key's
CBO-group x AGI-bin cells to CBO's group shares and IRS 2023's bin shares (R), holding the union's share inside each
cell (theta = V / X), so the union's share changes by sum(R theta) - sum(V) (translation_inputs.json share_change
irs_2023_raked_with_cbo_groups; the package multiplies it by the national line and the union's stack factor). A
generation's share inside a cell is its own dollars over the cell's, theta_g = V_g / X, and its change is
sum(R theta_g) - sum(V_g): the same raked cells, the generation's dollars in each. V is the sum of the V_g, so the
changes add to the union's exactly. heldout.py's helpers are imported read-only (with its frame, the benchmark lane's,
bound to its cache) and its aggregation and raking are re-run here unchanged, with generation weights inside the
union (frame.assignments of the lane V4_LANE_DIR names, as v4_inputs.py; merged on PH_SEQ and PPPOS as
external_split.py merges them).
Gates (exit 1, nothing written): the generation weights partition the benchmark frame's union; the union's change
reproduces translation_inputs.json for both allocations (1e-15); under each convention the generations add to it
(1e-15).
Output: tax_key_by_generation.json in the lane's frame.OUT. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl --with xlrd python3 \
    infra/immigration-fiscal/generation_account_2026_09_24/tax_key_split.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import importlib.util  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
TAX_LANE = HERE.parent / "tax_key_heldout_2026_09_28"
# heldout.py first: it binds `frame` to the benchmark lane's module; this lane's frame is loaded by path under
# another name, so the two modules called frame do not collide.
_hs = importlib.util.spec_from_file_location("tax_heldout", TAX_LANE / "heldout.py")
H = importlib.util.module_from_spec(_hs)
_hs.loader.exec_module(H)
LANE = Path(os.environ.get("V4_LANE_DIR", str(HERE))).resolve()
_fs = importlib.util.spec_from_file_location("v4_lane_frame", LANE / "frame.py")
F = importlib.util.module_from_spec(_fs)
_fs.loader.exec_module(F)

VARIANT = "irs_2023_raked_with_cbo_groups"
ALLOCS = ("personal", "shared")
FAILS = []


def gate(label, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def main():
    f, cbo_arm = H.f, H.cbo_arm
    d = f.load()
    civ, target = f.masks(d)
    W = f.weights(d)
    vp = d.FEDTAX_BC.to_numpy(float)
    ids = d.SPM_ID.to_numpy()
    vec = {"personal": vp, "shared": f.unit_equal(vp, ids)}

    gd = F.load()
    gciv, gunion, gens = F.masks(gd)
    omega, _, _ = F.assignments(gd, gciv, gunion, gens)
    cols = {f"{conv}{j}": omega[conv][:, j] for conv in omega for j in range(len(F.GENS))}
    m = d[["PH_SEQ", "PPPOS"]].merge(gd[["PH_SEQ", "PPPOS"]].assign(**cols), on=["PH_SEQ", "PPPOS"], how="left",
                                     validate="one_to_one")
    om = {conv: {g: m[f"{conv}{j}"].fillna(0.0).to_numpy(float) for j, g in enumerate(F.GENS)} for conv in omega}
    for conv in om:
        total = sum(om[conv].values())
        gate(f"({conv}) the generation weights partition the benchmark frame's union", np.allclose(total[target], 1)
             and not total[~target].any())

    irs23 = H.irs_table(2023)
    edges = H.edges_from_labels(irs23["labels"])
    I23 = irs23["shares"]
    g, _ = cbo_arm.groups(d)
    groups = list(f.GROUPS)
    shares = pd.read_csv(H.BENCH / "derived/cbo_group_shares.csv").query("spec == @H.SPEC").set_index("group")
    cbo = {j: float(shares.loc[j, "cbo_share"]) for j in groups}
    b = H.band_of(d.AGI.to_numpy(float), edges)
    codes, _ = pd.factorize(ids)
    size = np.bincount(codes).astype(float)

    def aggregates(a):
        """heldout.py aggregates(), plus each generation's Ub (its weights inside the union)."""
        Mb = np.zeros((len(d), 19))
        for k in range(19):
            x = vp * (b == k)
            Mb[:, k] = x if a == "personal" else (np.bincount(codes, weights=x) / size)[codes]
        out = {}
        for j in groups:
            mj = civ & (g == j)
            mt = mj & target
            out[j] = {"T": vec[a][mj] @ W[mj], "Tb": Mb[mj].T @ W[mj], "Ub": Mb[mt].T @ W[mt],
                      "Ug": {conv: {x: Mb[mt].T @ (W[mt] * om[conv][x][mt][:, None]) for x in F.GENS} for conv in om}}
        return out

    pos = [j for j in groups if cbo[j] > 0]

    def rake_cols(x):
        p = H.pool(x)
        return np.concatenate([p[:2].sum(axis=0, keepdims=True), p[2:]])

    def raked_change(a, A):
        """heldout.py raked_change(), and each generation's change in the same raked cells."""
        X = np.stack([cbo[j] * rake_cols(A[j]["Tb"]) / A[j]["T"] for j in pos])
        V = np.stack([cbo[j] * rake_cols(A[j]["Ub"]) / A[j]["T"] for j in pos])
        theta = np.divide(V, X, out=np.zeros_like(V), where=X > 0)
        rows = np.array([cbo[j] for j in pos])[:, None]
        colsum = rake_cols(I23)[:, None]
        R = X.copy()
        for it in range(20000):
            R *= (colsum / R.sum(axis=0))[None]
            R *= (rows / R.sum(axis=1))[:, None]
            if max(np.abs(R.sum(axis=0) - colsum).max(), np.abs(R.sum(axis=1) - rows).max()) < 1e-12:
                break
        else:
            raise SystemExit(f"[BLOCKED] raking did not converge ({a})")
        union = (R * theta).sum(axis=(0, 1)) - V.sum(axis=(0, 1))
        by = {}
        for conv in om:
            by[conv] = {}
            for x in F.GENS:
                Vg = np.stack([cbo[j] * rake_cols(A[j]["Ug"][conv][x]) / A[j]["T"] for j in pos])
                tg = np.divide(Vg, X, out=np.zeros_like(Vg), where=X > 0)
                by[conv][x] = (R * tg).sum(axis=(0, 1)) - Vg.sum(axis=(0, 1))
        return union, by, it + 1

    stored = json.loads((TAX_LANE / "derived/translation_inputs.json").read_text())
    national = stored["national_bn"]
    out = {"union": {}, **{conv: {x: {} for x in F.GENS} for conv in om}}
    iterations = {}
    for a in ALLOCS:
        union, by, its = raked_change(a, aggregates(a))
        iterations[a] = its
        want = stored["share_change"][VARIANT][a]
        gate(f"{a}: the union's change reproduces translation_inputs.json {VARIANT}", abs(float(union[0]) - want) < 1e-15,
             f"{float(union[0]):.15e} vs {want:.15e} ({national * want:+.4f}bn before the stack factor)")
        out["union"][a] = float(union[0])
        for conv in om:
            s = sum(float(by[conv][x][0]) for x in F.GENS)
            gate(f"({conv}) {a}: the generations add to the union's change", abs(s - float(union[0])) < 1e-15,
                 "; ".join(f"{x} {national * float(by[conv][x][0]):+.4f}bn" for x in F.GENS))
            for x in F.GENS:
                out[conv][x][a] = float(by[conv][x][0])
    if FAILS:
        print(f"✗ {len(FAILS)} gate(s) failed, nothing written: {FAILS}")
        sys.exit(1)
    out["meta"] = {"source": "generation_account_2026_09_24/tax_key_split.py", "variant": VARIANT, "line": stored["line"],
                   "national_bn": national, "frame": str(Path(F.__file__).relative_to(F.ROOT)), "generations": F.GENS,
                   "raking_iterations": iterations,
                   "layout": "share change of the national line before the stack factor: union, then convention -> generation "
                             "-> allocation; the package books national x change x the union's stack factor"}
    path = F.OUT / "tax_key_by_generation.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(f"  wrote {path.relative_to(F.ROOT)}")
    print("  ✓ all tax-key split gates passed")


if __name__ == "__main__":
    main()
