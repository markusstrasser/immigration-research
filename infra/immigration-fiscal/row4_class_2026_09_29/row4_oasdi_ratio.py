"""The pension switch's OASDI ratio (accrual per dollar of OASDI tax, net of the tax on benefits) on row 4's weights.

v4's Social Security line is ratio_net x the group's OASDI receipts (main_case_candidate_v4_2026_09_29/package.cjs:115).
The receipts are the case's (row 4); ratio_net = the union's accrual per tax dollar x (1 - relative rate x timing), all
summed over the pension lane's frame at the published weights. This reruns the lane's central per-person accrual
(pension_accrual.central_accrual, imported read-only; the model grid built for the central run and the normalizing base
only) and sums it at the published weights (gates: summary.json's gross ratio, future share, ratio_net and SE OASDI
share) and at row 4's. ratio_net here holds the lane's relative rate (benefit_tax.json, published weights) in both;
price_rekeys.cjs replaces it with the row-4 rate from derived/row4_benefit_tax.json.
Writes derived/row4_oasdi_ratio.json. Run from the repository root after row4_parta.py:
  OPENBLAS_NUM_THREADS=1 UV_OFFLINE=1 uv run --no-project python3 infra/immigration-fiscal/row4_class_2026_09_29/row4_oasdi_ratio.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import csv  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import zipfile  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
sys.path.insert(0, str(FISCAL / "pension_accrual_2026_09_28"))
import pension_accrual as PA  # noqa: E402

FAILS = []


def gate(label, ok, detail=""):
    print(f"GATE {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


key = hashlib.sha256(b"".join(Path(f).read_bytes() for f in (PA.ss.__file__, PA.ss.ext.__file__, PA.ca.__file__))).hexdigest()[:16]
gate("pension stage cache present (no rebuild)", (PA.CACHE / f"stage_{key}.parquet").exists(), key)
if FAILS:
    print("[BLOCKED] the pension stage cache is missing; nothing written", flush=True)
    sys.exit(1)
FAC = json.loads((OUT / "row4_parta.json").read_text())["factors"]
COUNTS = {r["count"]: r for r in csv.DictReader(open(FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv"))}
N_ROW4 = float(COUNTS["union|all"]["row4"])
SUM = json.loads((FISCAL / "pension_accrual_2026_09_28/derived/summary.json").read_text())
cd = SUM["central_decomposition"]["low"]
cn = SUM["central_decomposition_net"]["low"]
p = PA.frame()
with zipfile.ZipFile(FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip") as z:
    hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"]).rename(columns={"H_SEQ": "PH_SEQ"})
st = p[["PH_SEQ"]].merge(hh, on="PH_SEQ", how="left", validate="many_to_one").GESTFIPS.to_numpy()
gate("every person has a state", not np.isnan(st.astype(float)).any())
mb = (p.PENATVTY.to_numpy() == 303) & ~np.isin(st, [6, 48])
f = np.ones(len(p))
f[mb & (p.PRCITSHP.to_numpy() == 4)] = FAC["natz"]
f[mb & (p.PRCITSHP.to_numpy() == 5)] = FAC["noncit"]
p["f"] = f
u = p.union.to_numpy()
gate("row-4 union on the pension frame", abs((p.w.to_numpy() * f)[u].sum() - N_ROW4) < 1.0, f"{(p.w.to_numpy() * f)[u].sum():.6f}")

econ = PA.L.Economy()
prelim = PA.S.scaled_factors().preliminary.to_numpy()
q = PA.S.quotes()
u_long = q["note151_eligible_share"]["value"]["end_of_projection"]
g = (PA.CENTRAL["rate"], PA.CENTRAL["mortality"])
PA.GRID = [g, PA.BASE]          # only the central run and the normalizing base are read
grids = {"payable": PA.model_grid(econ, prelim, PA.payable_path(econ))}
share = PA.tob_share_path() * (1 + PA.hi_over_oasdi_tob()) * PA.obbba_factor()
taus = PA.tob_timing(econ, prelim, share, runs=[(g, "payable")])
qu = p[p.union & (p.tax_oasdi > 0)].reset_index(drop=True)
acc, tob = PA.central_accrual(qu, grids, u_long, taus, PA.ss.family_vector(qu, "observed_family"))
tax = qu.tax_oasdi.to_numpy()
bt = json.loads((FISCAL / "pension_accrual_2026_09_28/derived/benefit_tax.json").read_text())
rel = bt["results"][PA.BT_CENTRAL["bt_mapping"]]["groups"]["union"]["relative_rate"][0]
out = {"relative_rate_union": rel}
for name, w in (("published", qu.w.to_numpy()), ("row4", qu.w.to_numpy() * qu.f.to_numpy())):
    ratio = float((w * acc).sum() / (w * tax).sum())
    timing = float((w * acc * tob).sum() / (w * acc).sum())
    fs = rel * timing
    out[name] = dict(ratio_gross=ratio, timing=timing, future_share=fs, ratio_net=ratio * (1 - fs),
                     oasdi_tax_bn=float((w * tax).sum() / 1e9), accrual_bn=float((w * acc).sum() / 1e9))
    print(f"{name}: gross ratio {ratio:.9f}, timing {timing:.9f}, future share {fs:.9f}, net ratio {ratio * (1 - fs):.9f}", flush=True)
gate("published gross ratio reproduces summary.json", abs(out["published"]["ratio_gross"] - cd["accrual_per_tax_dollar"]) < 1e-9,
     f"{out['published']['ratio_gross']:.12f} vs {cd['accrual_per_tax_dollar']:.12f}")
gate("published future share reproduces summary.json", abs(out["published"]["future_share"] - cn["future_share"]) < 1e-9,
     f"{out['published']['future_share']:.12f} vs {cn['future_share']:.12f}")
gate("published net ratio reproduces ratio_net", abs(out["published"]["ratio_net"] - SUM["ratio_net"]) < 1e-9)
# The self-employment split the accrual base uses (case_components: OASDI share of the group's SE tax).
for name, w in (("published", p.w.to_numpy()), ("row4", p.w.to_numpy() * f)):
    wu = w[u]
    so = float((wu * (p.oasdi_se * p.onbooks).to_numpy()[u]).sum())
    sh = float((wu * (p.hi_se * p.onbooks).to_numpy()[u]).sum())
    out[name]["se_oasdi_share"] = so / (so + sh)
gate("published SE OASDI share reproduces summary.json", abs(out["published"]["se_oasdi_share"] - SUM["case_components_attrs"]["se_oasdi_share"]) < 1e-12)
out["gates_failed"] = FAILS
if FAILS:
    print(f"[BLOCKED] {len(FAILS)} gate(s) failed; nothing written", flush=True)
    sys.exit(1)
(OUT / "row4_oasdi_ratio.json").write_text(json.dumps(out, indent=1) + "\n")
