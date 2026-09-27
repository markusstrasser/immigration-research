"""Gates for the generation carry-over lane. Run after analyze_*.py, disconfirm.py and summarize.py."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
D = HERE / "derived"
FAIL = []


def check(ok, msg):
    print(("  ✓ " if ok else "  ✗ ") + msg)
    if not ok:
        FAIL.append(msg)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# 1. CPS 2025 G3/G4+ counts reproduce the split lane before any year was added.
audit = json.loads((D / "cps_audit_CPS_ASEC_2022_2025.json").read_text())
ref = pd.read_csv(HERE.parent / "generation_split_2026_09_20/derived/cps_generation_split.csv").query(
    "arm == 'reported_linkage' and age == 'all'").set_index("generation").people
for k, exp in [("G3_Mexico_GP_observed", 2.870e6), ("G4plus_all_US_GP_observed", 2.073e6)]:
    got = audit["gate_2025"][k]
    check(abs(got - ref[k]) < 1 and round(got / 1e6, 3) == exp / 1e6, f"CPS2025 {k} {got:,.0f} = split lane {ref[k]:,.0f} ({exp/1e6:.3f}m)")

# 2. Adopted-account ratios are computed from the CSV, not retyped.
acc = pd.read_csv(HERE.parent / "generation_account_2026_09_24/derived/generation_results.csv")
co = pd.read_csv(D / "carryover.csv")
aa = co[co.source.str.startswith("adopted_account_")]
check(len(aa) == 8, "eight adopted-account ratio rows (2 conventions x 2 ends x 2 steps)")
for r in aa.itertuples():
    conv = r.frame.split()[1]
    band = r.frame.rsplit(", ", 1)[1].split()[0]
    v = acc[acc.convention.eq(conv) & acc.band_end.eq(band)].set_index("generation").per_adult_usd
    a, b = r.generation.split("->")
    check(np.isclose(r.rho, v[b] / v[a], rtol=1e-12), f"adopted {conv}/{band} {r.generation} rho {r.rho:.4f}")

# 3. Every published NLSY97 number used is printed on its cited PDF page.
pages = (HERE / "_cache/dp12704.txt").read_text().split("\f")
s = _load("carry_sum", HERE / "summarize.py")


def on_page(val, page, fmt="{:.2f}"):
    txt = pages[page - 1]
    cands = {fmt.format(val), fmt.format(val).lstrip("0").replace("-0.", "-."), f"{val:.3f}", f"{val:.3f}".replace("0.", ".", 1),
             f"{val:,.0f}" if float(val).is_integer() else "__"}
    return any(re.search(r"(?<![\d.])" + re.escape(c) + r"(?![\d])", txt) for c in cands)


bad = []
for m, gens in s.NLSY_T2.items():
    for g, (v, se, n) in gens.items():
        for x in (v, se):
            if not on_page(x, 45):
                bad.append(("T2", m, g, x))
for (m, cite), gens in s.NLSY_REG.items():
    page = int(re.search(r"PDF p\.(\d+)", cite).group(1))
    for g, (b, se) in gens.items():
        for x in (b, se):
            if not (on_page(x, page, "{:.3f}") or on_page(x, page)):
                bad.append((cite[:25], g, x))
for g, pair in s.NLSY_T5.items():
    for v, se in pair:
        for x in (v, se):
            if not on_page(x, 48):
                bad.append(("T5", g, x))
for g, (v, se) in s.NLSY_T6_DELTA.items():
    for x in (v, se):
        if not on_page(x, 49):
            bad.append(("T6", g, x))
check(on_page(.28, 49) and on_page(.02, 49), "Table 6 parental coefficients .28 (.02) on p.49")
for g, (v, se, n) in s.NLSY_T12.items():
    for x in (v, se):
        if not on_page(x, 56):
            bad.append(("T12", g, x))
for k, dct in s.NLSY_T13.items():
    for m in ("educ_years", "ba_plus"):
        if not on_page(dct[m], 57):
            bad.append(("T13", k, dct[m]))
check(not bad, f"all NLSY97 table numbers found on their cited PDF pages ({'none missing' if not bad else bad})")

# 4. Deliverable CSVs carry the required columns and LF line endings.
for f in ["gaps_by_generation.csv", "carryover.csv", "attrition_bounds.csv", "projection.csv"]:
    t = pd.read_csv(D / f)
    check({"source", "measure", "generation", "n", "se"} <= set(t.columns), f"{f} has source/measure/generation/n/se")
    check(b"\r\n" not in (D / f).read_bytes(), f"{f} uses LF line endings")

# 5. Reweighting reproduces the group's cell distribution (synthetic).
cps = _load("carry_cps", HERE / "analyze_cps.py")
rng = np.random.default_rng(0)
cg, cr = rng.integers(0, 5, 300), rng.integers(0, 5, 2000)
wg, wr = rng.uniform(.5, 2, (300, 3)), rng.uniform(.5, 2, (2000, 3))
out, unc = cps.reweight(cg, wg, cr, wr)
for r in range(3):
    sg = np.bincount(cg, weights=wg[:, r], minlength=5)
    so = np.bincount(cr, weights=out[:, r], minlength=5)
    check(np.allclose(sg / sg.sum(), so / so.sum()) and unc == 0, f"reweight replicate {r} matches group cell shares")

# 6. Pooled CPS frames: co-resident observed G3/G4+ never appear in the population frame.
g = pd.read_csv(D / "cps_gaps_CPS_ASEC_2022_2025.csv")
check(not g[g.frame.eq("pop")].generation.isin(["G3_obs", "G4plus_obs"]).any(), "observed G3/G4+ only in co-resident frames")
check(g[g.frame.eq("cores_both") & g.generation.eq("G4plus_obs") & g.measure.eq("ba_plus")].n.iloc[0] == 302,
      "cores_both G4+ BA n = 302 (all G4+ require both parents)")

print(f"\n{'FAILED: ' + str(len(FAIL)) if FAIL else 'all gates pass'}")
raise SystemExit(1 if FAIL else 0)
