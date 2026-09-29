"""The pension switch's Part A accrual on audit row 4's weights.

v4's Medicare line is the pension lane's Part A accrual ($41.137128bn, pension_accrual_2026_09_28/derived/summary.json
central_decomposition.low.part_a_accrual_bn) plus the case's Parts B and D. The accrual is the lane's own total over its
CPS frame (pension_accrual.hi_accrual, weights p.w, union 40,896,574: the published ASEC weights). This reruns
hi_accrual, imported read-only, with p.w scaled by row 4's two cell factors (Mexico-born naturalized / noncitizen
outside CA+TX to their ACS 2024 levels, combine_onbooks_lane.weight_arms, full-sample column), and reports kappa =
published accrual / row-4 accrual.

Gates: the stage cache exists (no rebuild, nothing written outside this lane); the union counts reproduce
population_basis_2026_09_29/derived/frame_counts.csv (published 1e-3; row 4 1e-3 on the CPS frame, 1 person on the
pension frame); the published run reproduces the lane's central union accrual (summary.json, 1e-9).
Writes derived/row4_parta.json, whose factors the other row4_*.py scripts read. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 UV_OFFLINE=1 uv run --no-project python3 infra/immigration-fiscal/row4_class_2026_09_29/row4_parta.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import csv  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
FAILS = []


def gate(label, ok, detail=""):
    print(f"GATE {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def blocked():
    if FAILS:
        print(f"[BLOCKED] {len(FAILS)} gate(s) failed; nothing written", flush=True)
        sys.exit(1)


COUNTS = {r["count"]: r for r in csv.DictReader(open(FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv"))}
N_PUB, N_ROW4 = float(COUNTS["union|all"]["published"]), float(COUNTS["union|all"]["row4"])
SUM = json.loads((FISCAL / "pension_accrual_2026_09_28/derived/summary.json").read_text())
PART_A_PUB = SUM["central_decomposition"]["low"]["part_a_accrual_bn"]

# Row 4's factors, as profiles_sept29.py builds them.
sys.path.insert(0, str(FISCAL / "main_case_decomposition_2026_09_29"))
import profiles as PR  # noqa: E402

F, L = PR.F, PR.L
d = F.load()
civ, union, _ = F.masks(d)
W = d[F.REPS].to_numpy(float)
arms, info = L.weight_arms(d, W, L.acs_cells())
w4 = arms["row4"][:, 0]
del arms
n4 = float(w4[union].sum())
gate("row-4 union count on the CPS frame", abs(n4 - N_ROW4) < 1e-3, f"{n4:.6f}")
fac = {"natz": info["factor_natz"], "noncit": info["factor_noncit"]}
print("row-4 factors", fac, flush=True)
state = d[["PH_SEQ", "GESTFIPS"]].drop_duplicates()

# The pension lane's frame, without rebuilding its stage.
sys.path.insert(0, str(FISCAL / "pension_accrual_2026_09_28"))
import pension_accrual as PA  # noqa: E402

key = hashlib.sha256(b"".join(Path(f).read_bytes() for f in (PA.ss.__file__, PA.ss.ext.__file__, PA.ca.__file__))).hexdigest()[:16]
gate("pension stage cache present (no rebuild)", (PA.CACHE / f"stage_{key}.parquet").exists(), key)
blocked()
p = PA.frame()
m = p[["PH_SEQ"]].merge(state, on="PH_SEQ", how="left", validate="many_to_one")
gate("every pension-frame person has a state", not m.GESTFIPS.isna().any())
st = m.GESTFIPS.to_numpy()
mb = (p.PENATVTY.to_numpy() == 303) & ~np.isin(st, L.CA_TX)
f = np.ones(len(p))
f[mb & (p.PRCITSHP.to_numpy() == 4)] = fac["natz"]
f[mb & (p.PRCITSHP.to_numpy() == 5)] = fac["noncit"]
u = p.union.to_numpy()
gate("pension frame union at published weights", abs(p.w.to_numpy()[u].sum() - N_PUB) < 1e-3, f"{p.w.to_numpy()[u].sum():.6f}")
n4p = float((p.w.to_numpy() * f)[u].sum())
gate("row-4 union count on the pension frame", abs(n4p - N_ROW4) < 1.0, f"{n4p:.6f}")

q = PA.S.quotes()
u_long = q["note151_eligible_share"]["value"]["end_of_projection"]
u_2000 = q["note151_eligible_share"]["value"]["age62_in_2000"]
econ = PA.L.Economy()
CEN = dict(rate="new_issue", scenario="payable", mortality="general", spouse=False, unauthorized="note151_long_run")


def central(hi):
    s = hi
    for k, v in CEN.items():
        s = s[s[k] == v]
    return s.set_index("group")


hi_pub, info_pub = PA.hi_accrual(p, econ, u_long, u_2000)
c_pub = central(hi_pub)
gate(f"published run reproduces the lane's central Part A accrual {PART_A_PUB:.9f}",
     abs(c_pub.loc["union", "accrual_bn"] - PART_A_PUB) < 1e-9, f"{c_pub.loc['union', 'accrual_bn']:.9f}")
p4 = p.copy()
p4["w"] = p.w.to_numpy() * f
hi_4, info_4 = PA.hi_accrual(p4, econ, u_long, u_2000)
c4 = central(hi_4)
out = {"factors": fac, "row4_union_pension_frame": n4p, "central": {}}
for g in ["union", "G1", "G2", "G3plus"]:
    a, b = float(c_pub.loc[g, "accrual_bn"]), float(c4.loc[g, "accrual_bn"])
    out["central"][g] = dict(published_bn=a, row4_bn=b, kappa=a / b if b else None,
                             covered_workers_published_m=float(c_pub.loc[g, "covered_workers_m"]),
                             covered_workers_row4_m=float(c4.loc[g, "covered_workers_m"]))
    print(f"{g}: Part A accrual published {a:.6f} row 4 {b:.6f} change {b - a:+.6f} kappa {a / b:.9f}; covered workers "
          f"{c_pub.loc[g, 'covered_workers_m']:.4f}M -> {c4.loc[g, 'covered_workers_m']:.4f}M", flush=True)
# Weight-only reading: the published run's per-worker terms, only the total re-weighted (pq and covered years held).
out["info_published"] = {k: v for k, v in info_pub.items() if k.startswith("p_qualify") or k == "expected_covered_years"}
out["info_row4"] = {k: v for k, v in info_4.items() if k.startswith("p_qualify") or k == "expected_covered_years"}
out["gates_failed"] = FAILS
blocked()
OUT.mkdir(exist_ok=True)
(OUT / "row4_parta.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
