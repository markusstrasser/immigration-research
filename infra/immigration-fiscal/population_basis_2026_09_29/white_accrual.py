"""The union's Social Security and Part A accrual per tax dollar on audit row 4's weights, for white_count.py.

white_replacement_2026_09_28/accrual_white.py prices the replacement on accrual with each group's accrual per tax
dollar from the pension lane (pension_accrual_2026_09_28) on the published CPS weights. Row 4 reweights only
Mexico-born people outside California and Texas, so the white group's ratios stand and the union's move with its
composition. Here the pension lane and accrual_white.py are imported read-only (module-level definitions only;
neither main() runs) and the union's ratios are recomputed on both weight sets at the lane's central settings.

Guard: the pension lane's stage cache for its current code must exist (building it would write into that lane).
Gates (exit 1, nothing written): the published weights reproduce the white lane's accrual_ratios.csv union rows
(1e-6) and the pension lane's stored union population; the row-4 weights remove derived/frame_counts.csv's
1,184,081 people from the union (2 persons).
Writes derived/white_accrual_ratios.csv, in accrual_ratios.csv's columns with a `weights` column added.
Run from the repository root after frame_counts.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --offline python3 infra/immigration-fiscal/population_basis_2026_09_29/white_accrual.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import csv  # noqa: E402
import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import zipfile  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
WR = FISCAL / "white_replacement_2026_09_28"
ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
OUT = HERE / "derived" / "white_accrual_ratios.csv"
FIELDS = ["group", "weights", "scenario", "oasdi_per_tax_dollar", "benefit_tax_timing", "part_a_per_hi_tax_dollar",
          "cps_oasdi_tax_bn", "cps_hi_tax_bn", "part_a_accrual_bn", "union_persons"]
FAILS: list[str] = []
sys.path.insert(0, str(FISCAL / "pension_accrual_2026_09_28"))
import pension_accrual as P  # noqa: E402
sys.path.insert(0, str(FISCAL / "generation_account_2026_09_24"))
import frame as F  # noqa: E402  (puts the CPS lane on sys.path)
import combine_onbooks_lane as L  # noqa: E402


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_csv(path):
    with path.open() as handle:
        return list(csv.DictReader(handle))


def ratios(A, p, grids, u_long, taus, econ):
    """accrual_white.main's union ratios (lines 96-100) for the frame p."""
    qq = p[p.union & (p.tax_oasdi > 0)].reset_index(drop=True)
    o = A.oasdi_ratio(qq, grids, u_long, taus)
    a = {s: A.part_a(p[p.union].copy(), econ, u_long, s) for s in P.SCENARIOS}
    return o, a


def main():
    # Guard: P.frame() builds and writes its stage cache when the cache for the current code is missing.
    key = hashlib.sha256(b"".join(Path(f).read_bytes() for f in (P.ss.__file__, P.ss.ext.__file__, P.ca.__file__)))
    cache = P.CACHE / f"stage_{key.hexdigest()[:16]}.parquet"
    if not cache.exists():
        raise SystemExit(f"[BLOCKED] the pension lane's stage cache {cache.name} is missing; building it would write "
                         "into that lane")
    A = load("accrual_white", WR / "accrual_white.py")
    print("[pension lane, central settings]", flush=True)
    q = P.S.quotes()
    u_long = q["note151_eligible_share"]["value"]["end_of_projection"]
    p = P.frame()
    econ = P.L.Economy()
    prelim = P.S.scaled_factors().preliminary.to_numpy()
    P.GRID = [A.G, P.BASE]      # as accrual_white.main: the central run and Note 2025.7's own basis
    grids = {s: P.model_grid(econ, prelim, P.payable_path(econ) if s == "payable" else None) for s in P.SCENARIOS}
    share = P.tob_share_path() * (1 + P.hi_over_oasdi_tob()) * P.obbba_factor()
    taus = P.tob_timing(econ, prelim, share, runs=[(A.G, s) for s in P.SCENARIOS])

    print("[row 4 weights]", flush=True)
    d = F.load()
    civ, union, gens = F.masks(d)
    W = d[F.REPS[:2]].to_numpy(float)
    arms, info = L.weight_arms(d, W, L.acs_cells())
    del arms, d, W
    with zipfile.ZipFile(ZIP) as z:
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"]).rename(columns={"H_SEQ": "PH_SEQ"})
    st = p[["PH_SEQ"]].merge(hh, on="PH_SEQ", how="left", validate="many_to_one").GESTFIPS
    if st.isna().any():
        raise SystemExit("[BLOCKED] pension-frame persons without a household state")
    outside = p.PENATVTY.eq(303).to_numpy() & ~np.isin(st.to_numpy(), L.CA_TX)
    p4 = p.copy()
    w4 = p.w.to_numpy(float).copy()
    w4[outside & p.PRCITSHP.eq(4).to_numpy()] *= info["factor_natz"]
    w4[outside & p.PRCITSHP.eq(5).to_numpy()] *= info["factor_noncit"]
    p4["w"] = w4
    counts = {r["count"]: r for r in read_csv(HERE / "derived" / "frame_counts.csv")}
    n_pub, n4 = float(counts["union|all"]["published"]), float(counts["union|all"]["row4"])
    u = p.union.to_numpy()
    gate("the pension frame's union is the stored union population",
         abs(float(p.w[u].sum()) - P.STORED_UNION["population"]) < 1e-3, f"{float(p.w[u].sum()):,.2f}")
    gate("row 4 removes frame_counts.csv's people from the pension frame's union",
         abs(float(p.w[u].sum() - w4[u].sum()) - (n_pub - n4)) < 2, f"{float(p.w[u].sum() - w4[u].sum()):,.1f}")

    published = {(r["group"], r["scenario"]): r for r in read_csv(WR / "derived" / "accrual_ratios.csv")}
    rows = []
    for label, frame in (("published", p), ("row4", p4)):
        print(f"[union ratios, {label} weights]", flush=True)
        o, a = ratios(A, frame, grids, u_long, taus, econ)
        for s in P.SCENARIOS:
            row = dict(group="union", weights=label, scenario=s, oasdi_per_tax_dollar=o[s]["ratio"],
                       benefit_tax_timing=o[s]["timing"],
                       part_a_per_hi_tax_dollar=a[s]["accrual_bn"] / a[s]["hi_tax_bn"], cps_oasdi_tax_bn=o[s]["tax_bn"],
                       cps_hi_tax_bn=a[s]["hi_tax_bn"], part_a_accrual_bn=a[s]["accrual_bn"],
                       union_persons=float(frame.w[frame.union].sum()))
            rows.append(row)
            if label == "published":
                ref = published[("union", s)]
                for k in ("oasdi_per_tax_dollar", "benefit_tax_timing", "part_a_per_hi_tax_dollar"):
                    gate(f"published weights reproduce accrual_ratios.csv: union {s} {k}",
                         abs(row[k] - float(ref[k])) < 1e-6, f"{row[k]:.6f} vs {ref[k]}")
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as handle:
        out = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        out.writeheader()
        for r in rows:
            out.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in r.items()})
    for r in rows:
        print(f"  {r['weights']:9s} {r['scenario']:9s} OASDI per tax dollar {r['oasdi_per_tax_dollar']:.6f} timing "
              f"{r['benefit_tax_timing']:.6f} Part A per HI dollar {r['part_a_per_hi_tax_dollar']:.6f} "
              f"(OASDI tax {r['cps_oasdi_tax_bn']:.3f}bn, persons {r['union_persons']:,.0f})")
    print(f"  wrote {len(rows)} rows -> {OUT.relative_to(FISCAL)}")


if __name__ == "__main__":
    main()
