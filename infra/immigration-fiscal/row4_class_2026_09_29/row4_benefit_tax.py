"""The pension switch's benefit-tax receipt on audit row 4's weights.

v4 removes from federal income tax the tax the group's 2024 Social Security benefits carry: $2.0912bn (shared, spec
48) / $1.8169bn (personal, spec 11), the pension lane's current_receipt_bn = national FIT x the group's benefit tax /
the national Census FEDTAX_BC key, both summed at the CPS ASEC 2025 published weights (benefit_tax.py, units line).
This reruns benefit_tax.py's census_income computation, its functions imported read-only (nothing written outside this
lane), and sums the same person vectors at the published weights (gates: benefit_tax.json's group benefit tax and
national key, and summary.json's current_receipt_bn, 1e-9) and at row 4's weights (Mexico-born naturalized /
noncitizen outside CA+TX times weight_arms' factors, read from derived/row4_parta.json). It also reports the relative
rate (the group's benefit tax after credits per benefit dollar over the nation's) at both weight sets; the OASDI
ratio's future share uses it (price_rekeys.cjs).
Writes derived/row4_benefit_tax.json. Run from the repository root after row4_parta.py:
  OPENBLAS_NUM_THREADS=1 UV_OFFLINE=1 uv run --no-project --with "taxcalc==6.8.2" python3 \
      infra/immigration-fiscal/row4_class_2026_09_29/row4_benefit_tax.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import csv  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
sys.path.insert(0, str(FISCAL / "pension_accrual_2026_09_28"))
import benefit_tax as B  # noqa: E402

FAILS = []


def gate(label, ok, detail=""):
    print(f"GATE {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


FAC = json.loads((OUT / "row4_parta.json").read_text())["factors"]
BTJ = json.loads((FISCAL / "pension_accrual_2026_09_28/derived/benefit_tax.json").read_text())
REF = BTJ["results"]["census_income"]["key"]
SUM_BT = json.loads((FISCAL / "pension_accrual_2026_09_28/derived/summary.json").read_text())["benefit_tax"]
NATIONAL_FIT = SUM_BT["national_income_tax_bn"]  # the case's federal income tax line, national (model.json)
COUNTS = {r["count"]: r for r in csv.DictReader(open(FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv"))}
N_PUB, N_ROW4 = float(COUNTS["union|all"]["published"]), float(COUNTS["union|all"]["row4"])
T, U, ext, TC = B.T, B.U, B.ext, B.TC
for _f in ("PENATVTY", "PRCITSHP"):
    if _f not in ext.base.PERSON:
        ext.base.PERSON.append(_f)
state = ext.build(argparse.Namespace(cps_zip=T.CPS_ZIP))
d, W = state["d"], state["person_weights"]
n = len(d)
civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
masks = {g: state["group"][c] & civ for g, c in B.TARGETS.items()}
union = masks["G1"] | masks["G2"] | masks["G3plus"]
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
d_before = before[True] - before[False]
key = {"personal": personal(d_before)}
key["shared"] = shared(key["personal"])

w0 = W[:, 0]
catx = d.GESTFIPS.isin([6, 48]).to_numpy()
mb = d.PENATVTY.eq(303).to_numpy() & ~catx
f = np.ones(n)
f[mb & d.PRCITSHP.eq(4).to_numpy()] = FAC["natz"]
f[mb & d.PRCITSHP.eq(5).to_numpy()] = FAC["noncit"]
w4 = w0 * f
gate("published union count", abs(w0[union].sum() - N_PUB) < 1e-3, f"{w0[union].sum():.6f}")
gate("row-4 union count", abs(w4[union].sum() - N_ROW4) < 1.0, f"{w4[union].sum():.6f}")
out = {}
for alloc, end in (("shared", "low"), ("personal", "high")):
    g0, n0 = float(key[alloc][union] @ w0[union]) / 1e9, float(census_key[alloc][civ] @ w0[civ]) / 1e9
    g4, n4 = float(key[alloc][union] @ w4[union]) / 1e9, float(census_key[alloc][civ] @ w4[civ]) / 1e9
    gate(f"{alloc}: published group benefit tax reproduces benefit_tax.json", abs(g0 - REF[alloc]["group_benefit_tax_bn"][0]) < 1e-9, f"{g0:.9f}")
    gate(f"{alloc}: published national key reproduces benefit_tax.json", abs(n0 - REF[alloc]["national_key_census_bn"]) < 1e-9, f"{n0:.6f}")
    r0, r4 = NATIONAL_FIT * g0 / n0, NATIONAL_FIT * g4 / n4
    gate(f"{alloc}: published receipt reproduces summary.json current_receipt_bn[{end}]",
         abs(r0 - SUM_BT["current_receipt_bn"][end]) < 1e-9, f"{r0:.9f}")
    out[alloc] = dict(end=end, group_published_bn=g0, group_row4_bn=g4, national_key_published_bn=n0, national_key_row4_bn=n4,
                      receipt_published_bn=r0, receipt_row4_bn=r4, kappa=r0 / r4)
    print(f"{alloc} ({end}): benefit-tax receipt published {r0:.6f} row 4 {r4:.6f} change {r4 - r0:+.6f} kappa {r0 / r4:.9f}", flush=True)
# The relative rate the accrual's future share uses: the group's benefit tax after credits over its benefits, over the
# nation's (benefit_tax.py: bt = d_after[ret] x by_benefit), at both weight sets.
after = {k: r["iitax"] - r["niit"] for k, r in runs.items()}
d_after = after[True] - after[False]
filer = (p.ret_role <= 1).to_numpy()
ss = d.SS_VAL.to_numpy(float)
ss_filed = np.where(filer, ss, 0.0)
unit_ss = np.bincount(ret, weights=ss_filed, minlength=n_ret)
by_benefit = np.divide(ss_filed, unit_ss[ret], out=np.zeros(n), where=unit_ss[ret] > 0)
bt = d_after[ret] * by_benefit
REL = BTJ["results"]["census_income"]["groups"]["union"]["relative_rate"][0]
for name, w in (("published", w0), ("row4", w4)):
    rate_g = float(bt[union] @ w[union]) / float(ss[union] @ w[union])
    rate_n = float(bt[civ] @ w[civ]) / float(ss[civ] @ w[civ])
    out[f"relative_rate_{name}"] = rate_g / rate_n
    print(f"relative rate ({name}): {rate_g / rate_n:.9f}", flush=True)
gate("published relative rate reproduces benefit_tax.json", abs(out["relative_rate_published"] - REL) < 1e-9, f"{REL:.9f}")
out["gates_failed"] = FAILS
if FAILS:
    print(f"[BLOCKED] {len(FAILS)} gate(s) failed; nothing written", flush=True)
    sys.exit(1)
(OUT / "row4_benefit_tax.json").write_text(json.dumps(out, indent=1) + "\n")
